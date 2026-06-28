import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from typing import Tuple, Dict
from ai.training.metrics import RoadMetrics
from utils.logger import get_logger

logger = get_logger("ai.training.validation")


class Validator:
    """
    Executes validation evaluation after every training epoch.
    Computes averaged loss components and topological metrics without backprop.
    """
    def __init__(self, loss_fn: nn.Module, metrics_fn: RoadMetrics, device: torch.device, amp_enabled: bool = True):
        self.loss_fn = loss_fn
        self.metrics_fn = metrics_fn
        self.device = device
        self.amp_enabled = amp_enabled
        
    @torch.no_grad()
    def validate(self, model: nn.Module, val_loader: DataLoader) -> Tuple[Dict[str, float], Dict[str, float]]:
        """
        Runs validation over the entire val_loader.
        
        Returns:
            Tuple of (avg_losses, avg_metrics) dictionaries.
        """
        model.eval()
        
        total_batches = len(val_loader)
        if total_batches == 0:
            return {}, {}
            
        accum_losses = {"total": 0.0, "bce": 0.0, "dice": 0.0, "cldice": 0.0}
        accum_metrics = {"iou": 0.0, "dice": 0.0, "precision": 0.0, "recall": 0.0, "f1": 0.0, "connectivity_ratio": 0.0}
        
        for images, masks in val_loader:
            images = images.to(self.device)
            masks = masks.to(self.device)
            
            with torch.amp.autocast(device_type=self.device.type, enabled=self.amp_enabled):
                logits = model(images)
                loss_dict = self.loss_fn(logits, masks)
                
            metrics_dict = self.metrics_fn(logits, masks)
            
            for k in accum_losses.keys():
                if k in loss_dict:
                    val = loss_dict[k].item() if isinstance(loss_dict[k], torch.Tensor) else loss_dict[k]
                    accum_losses[k] += val
                    
            for k in accum_metrics.keys():
                if k in metrics_dict:
                    accum_metrics[k] += metrics_dict[k]
                    
        # Average across all batches
        avg_losses = {k: v / total_batches for k, v in accum_losses.items()}
        avg_metrics = {k: v / total_batches for k, v in accum_metrics.items()}
        
        return avg_losses, avg_metrics
