import torch
import torch.nn as nn
from utils.logger import get_logger

logger = get_logger("ai.loss.bce")


class WeightedBCELoss(nn.Module):
    """
    Binary Cross-Entropy Loss with optional positive-class weighting.
    
    Roads typically occupy <10% of satellite imagery pixels, creating severe
    class imbalance. pos_weight upweights the road class to counter this.
    
    ISRO Alignment:
        Directly addresses dataset_strategy.md class imbalance concern.
    """
    
    def __init__(self, pos_weight: float = 1.0):
        super().__init__()
        self.pos_weight = torch.tensor([pos_weight])
    
    def forward(self, logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        """
        Args:
            logits: Raw model output (B, 1, H, W). No sigmoid needed — BCE with logits.
            targets: Binary ground truth (B, 1, H, W) in {0, 1}.
        """
        pw = self.pos_weight.to(logits.device)
        return nn.functional.binary_cross_entropy_with_logits(
            logits, targets, pos_weight=pw
        )
