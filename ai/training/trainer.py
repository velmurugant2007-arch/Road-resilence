import os
import random
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from pathlib import Path
from typing import Optional, Dict, Any

from ai.model_config import FullConfig
from ai.loss.combined import CombinedLoss
from ai.training.metrics import RoadMetrics
from ai.training.optimizer import build_optimizer
from ai.training.scheduler import build_scheduler
from ai.training.callbacks import EarlyStopping, CheckpointCallback
from ai.training.logger import TrainingLogger
from ai.training.validation import Validator
from ai.checkpoint import CheckpointManager
from utils.logger import get_logger

logger = get_logger("ai.training.trainer")


def set_deterministic_seed(seed: int = 42):
    """Ensures reproducible training across Kaggle and local environments."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    logger.info(f"Deterministic seed set to {seed}")


class Trainer:
    """
    Production-ready orchestrator for training SegFormer road extraction models.
    
    Handles AMP, gradient clipping, checkpoint resuming, epoch validation,
    early stopping, scheduler steps, per-loss logging, and fine-tuning transitions.
    """
    def __init__(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        val_loader: DataLoader,
        config: FullConfig,
        log_dir: Path | str = "logs/training",
        seed: int = 42
    ):
        set_deterministic_seed(seed)
        
        self.config = config
        self.train_loader = train_loader
        self.val_loader = val_loader
        
        # Automatic GPU/CPU detection
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Trainer initializing on device: {self.device}")
        
        self.model = model.to(self.device)
        self.amp_enabled = config.training.amp_enabled and self.device.type == "cuda"
        self.scaler = torch.cuda.amp.GradScaler(enabled=self.amp_enabled)
        
        # Loss & Metrics
        self.loss_fn = CombinedLoss(config.training.loss)
        self.metrics_fn = RoadMetrics(
            threshold=config.inference.confidence_threshold,
            skeleton_iterations=config.training.loss.soft_skeleton_iterations
        )
        
        # Optimizer & Scheduler
        self.optimizer = build_optimizer(self.model, config.training)
        self.scheduler = build_scheduler(self.optimizer, config.training)
        
        # Checkpoint Manager & Callbacks
        self.ckpt_manager = CheckpointManager(
            save_dir=config.checkpointing.save_dir,
            monitor_metric=config.checkpointing.monitor_metric,
            monitor_mode=config.checkpointing.monitor_mode
        )
        self.ckpt_callback = CheckpointCallback(self.ckpt_manager)
        self.early_stopping = EarlyStopping(patience=15, mode=config.checkpointing.monitor_mode)
        
        # Logging & Validation
        self.logger = TrainingLogger(log_dir=log_dir)
        self.validator = Validator(
            loss_fn=self.loss_fn,
            metrics_fn=self.metrics_fn,
            device=self.device,
            amp_enabled=self.amp_enabled
        )
        
        self.start_epoch = 0
        
    def resume_if_available(self):
        """Attempts to resume model, optimizer, scheduler, and scaler from latest checkpoint."""
        self.start_epoch = self.ckpt_manager.resume_training(
            self.model, self.optimizer, self.scheduler, self.scaler
        )
        
    def _train_epoch(self, epoch: int) -> Tuple[Dict[str, float], Dict[str, float]]:
        self.model.train()
        
        accum_losses = {"total": 0.0, "bce": 0.0, "dice": 0.0, "cldice": 0.0}
        accum_metrics = {"iou": 0.0, "dice": 0.0, "precision": 0.0, "recall": 0.0, "f1": 0.0, "connectivity_ratio": 0.0}
        total_batches = len(self.train_loader)
        
        if total_batches == 0:
            return {}, {}
            
        for batch_idx, (images, masks) in enumerate(self.train_loader):
            images = images.to(self.device)
            masks = masks.to(self.device)
            
            self.optimizer.zero_grad()
            
            with torch.amp.autocast(device_type=self.device.type, enabled=self.amp_enabled):
                logits = self.model(images)
                loss_dict = self.loss_fn(logits, masks)
                total_loss = loss_dict["total"]
                
            self.scaler.scale(total_loss).backward()
            
            # Gradient clipping
            if self.config.training.gradient_clip_max_norm > 0:
                self.scaler.unscale_(self.optimizer)
                torch.nn.utils.clip_grad_norm_(
                    self.model.parameters(), max_norm=self.config.training.gradient_clip_max_norm
                )
                
            self.scaler.step(self.optimizer)
            self.scaler.update()
            
            # Accumulate metrics (no grad for speed)
            with torch.no_grad():
                metrics_dict = self.metrics_fn(logits.detach(), masks)
                
            for k in accum_losses.keys():
                if k in loss_dict:
                    val = loss_dict[k].item() if isinstance(loss_dict[k], torch.Tensor) else loss_dict[k]
                    accum_losses[k] += val
            for k in accum_metrics.keys():
                if k in metrics_dict:
                    accum_metrics[k] += metrics_dict[k]
                    
        avg_losses = {k: v / total_batches for k, v in accum_losses.items()}
        avg_metrics = {k: v / total_batches for k, v in accum_metrics.items()}
        return avg_losses, avg_metrics

    def _check_finetune_transition(self, epoch: int):
        """Checks if training should transition to topological fine-tuning phase."""
        ft = self.config.training.finetune
        if ft.enabled and epoch == ft.start_epoch:
            logger.info(f"Epoch {epoch}: Transitioning to Topological Fine-Tuning Phase!")
            # Adjust learning rate
            for param_group in self.optimizer.param_groups:
                param_group["lr"] = ft.learning_rate
            logger.info(f"Adjusted optimizer LR to fine-tuning rate: {ft.learning_rate}")

    def train(self, max_epochs: Optional[int] = None):
        """Executes the complete training loop."""
        epochs_to_run = max_epochs or self.config.training.epochs
        
        logger.info(f"Starting training loop from epoch {self.start_epoch} to {epochs_to_run - 1}...")
        
        for epoch in range(self.start_epoch, epochs_to_run):
            self._check_finetune_transition(epoch)
            
            # Train Phase
            train_losses, train_metrics = self._train_epoch(epoch)
            current_lr = self.optimizer.param_groups[0]["lr"]
            self.logger.log_epoch(epoch, "train", train_losses, train_metrics, current_lr)
            
            # Validation Phase
            val_losses, val_metrics = self.validator.validate(self.model, self.val_loader)
            self.logger.log_epoch(epoch, "val", val_losses, val_metrics, current_lr)
            
            # Scheduler Step
            if isinstance(self.scheduler, torch.optim.lr_scheduler.ReduceLROnPlateau):
                monitor_val = val_metrics.get(self.config.checkpointing.monitor_metric, 0.0)
                self.scheduler.step(monitor_val)
            else:
                self.scheduler.step()
                
            # Checkpointing
            config_dict = {"epochs": epochs_to_run, "batch_size": self.config.training.batch_size}
            self.ckpt_callback(epoch, self.model, self.optimizer, self.scheduler, self.scaler, val_metrics, config_dict)
            
            # Early Stopping
            monitor_val = val_metrics.get(self.config.checkpointing.monitor_metric, 0.0)
            if self.early_stopping(monitor_val):
                break
                
        self.logger.close()
        logger.info("Training complete.")
