import torch
from typing import Dict, Any
from ai.checkpoint import CheckpointManager, CheckpointState
from utils.logger import get_logger

logger = get_logger("ai.training.callbacks")


class EarlyStopping:
    """
    Early stopping callback to halt training when validation metric stops improving.
    Prevents overfitting and saves GPU hours during Kaggle / local runs.
    """
    def __init__(self, patience: int = 10, min_delta: float = 1e-4, mode: str = "max"):
        self.patience = patience
        self.min_delta = min_delta
        self.mode = mode
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        
    def __call__(self, current_score: float) -> bool:
        if self.best_score is None:
            self.best_score = current_score
            return False
            
        if self.mode == "max":
            improved = current_score > self.best_score + self.min_delta
        else:
            improved = current_score < self.best_score - self.min_delta
            
        if improved:
            self.best_score = current_score
            self.counter = 0
        else:
            self.counter += 1
            logger.info(f"EarlyStopping counter: {self.counter} out of {self.patience}")
            if self.counter >= self.patience:
                self.early_stop = True
                logger.warning("EarlyStopping triggered! Halting training.")
                
        return self.early_stop


class CheckpointCallback:
    """
    Callback wrapper around CheckpointManager for automatic saving during training loop.
    """
    def __init__(self, manager: CheckpointManager):
        self.manager = manager
        
    def __call__(
        self,
        epoch: int,
        model: torch.nn.Module,
        optimizer: torch.optim.Optimizer,
        scheduler: Any,
        scaler: Any,
        metrics: Dict[str, float],
        config_dict: dict
    ) -> bool:
        monitor_val = metrics.get(self.manager.monitor_metric, 0.0)
        
        state = CheckpointState(
            epoch=epoch,
            model_state_dict=model.state_dict(),
            optimizer_state_dict=optimizer.state_dict(),
            scheduler_state_dict=scheduler.state_dict() if scheduler else None,
            scaler_state_dict=scaler.state_dict() if scaler else None,
            best_metric=monitor_val,
            config=config_dict
        )
        
        # Save latest checkpoint every epoch
        self.manager.save_latest(state)
        
        # Save best checkpoint if metric improved
        is_best = self.manager.save_best(state, monitor_val)
        return is_best
