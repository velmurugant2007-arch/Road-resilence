import torch
from pathlib import Path
from dataclasses import dataclass
from utils.logger import get_logger

logger = get_logger("ai.checkpoint")


@dataclass
class CheckpointState:
    """Everything needed to resume training exactly where we left off."""
    epoch: int
    model_state_dict: dict
    optimizer_state_dict: dict
    scheduler_state_dict: dict | None
    scaler_state_dict: dict | None  # AMP GradScaler
    best_metric: float
    config: dict


class CheckpointManager:
    """
    Manages model checkpoints: best, latest, and resume-from-crash.
    
    Engineering Justification:
        Hackathon training runs on unstable Colab sessions that can
        disconnect at any time. Without checkpoint resume, we lose
        hours of GPU time. This manager guarantees zero-loss recovery.
    """
    
    def __init__(self, save_dir: Path | str, monitor_metric: str = "val_cldice", monitor_mode: str = "max"):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.monitor_metric = monitor_metric
        self.monitor_mode = monitor_mode
        
        if monitor_mode == "max":
            self.best_value = float("-inf")
        else:
            self.best_value = float("inf")
    
    def _is_improvement(self, current: float) -> bool:
        if self.monitor_mode == "max":
            return current > self.best_value
        return current < self.best_value
    
    def save_latest(self, state: CheckpointState):
        """Save the latest checkpoint (overwritten every epoch)."""
        path = self.save_dir / "latest.pt"
        torch.save({
            "epoch": state.epoch,
            "model_state_dict": state.model_state_dict,
            "optimizer_state_dict": state.optimizer_state_dict,
            "scheduler_state_dict": state.scheduler_state_dict,
            "scaler_state_dict": state.scaler_state_dict,
            "best_metric": state.best_metric,
            "config": state.config,
        }, path)
        logger.debug(f"Latest checkpoint saved at epoch {state.epoch}")
    
    def save_best(self, state: CheckpointState, current_metric: float) -> bool:
        """Save the best checkpoint if the monitored metric improved."""
        if self._is_improvement(current_metric):
            self.best_value = current_metric
            path = self.save_dir / "best.pt"
            torch.save({
                "epoch": state.epoch,
                "model_state_dict": state.model_state_dict,
                "optimizer_state_dict": state.optimizer_state_dict,
                "scheduler_state_dict": state.scheduler_state_dict,
                "scaler_state_dict": state.scaler_state_dict,
                "best_metric": current_metric,
                "config": state.config,
            }, path)
            logger.info(f"New best model! {self.monitor_metric}={current_metric:.4f} at epoch {state.epoch}")
            return True
        return False
    
    def load(self, checkpoint_type: str = "latest") -> dict | None:
        """
        Load a checkpoint. checkpoint_type: 'latest' or 'best'.
        Returns None if no checkpoint exists (fresh training start).
        """
        path = self.save_dir / f"{checkpoint_type}.pt"
        if not path.exists():
            logger.info(f"No {checkpoint_type} checkpoint found. Starting fresh.")
            return None
        
        data = torch.load(path, map_location="cpu")
        logger.info(f"Loaded {checkpoint_type} checkpoint from epoch {data['epoch']}")
        return data
    
    def resume_training(self, model, optimizer, scheduler=None, scaler=None) -> int:
        """
        Attempts to resume from the latest checkpoint.
        Returns the starting epoch (0 if no checkpoint found).
        """
        data = self.load("latest")
        if data is None:
            return 0
        
        model.load_state_dict(data["model_state_dict"])
        optimizer.load_state_dict(data["optimizer_state_dict"])
        
        if scheduler is not None and data.get("scheduler_state_dict"):
            scheduler.load_state_dict(data["scheduler_state_dict"])
        
        if scaler is not None and data.get("scaler_state_dict"):
            scaler.load_state_dict(data["scaler_state_dict"])
        
        self.best_value = data.get("best_metric", self.best_value)
        start_epoch = data["epoch"] + 1
        
        logger.info(f"Resumed training from epoch {start_epoch}")
        return start_epoch
