import torch
import torch.nn as nn
from utils.logger import get_logger

logger = get_logger("ai.loss.dice")


class DiceLoss(nn.Module):
    """
    Dice Loss for binary segmentation.
    
    Measures the overlap between prediction and ground truth as a set similarity.
    Handles class imbalance better than BCE by normalizing by the union.
    
    Architecture Traceability:
        - mathematical_design.md Section 1
        - Used as one component of the hybrid loss
    
    Formula:
        Dice = 2 * |P ∩ G| / (|P| + |G|)
        DiceLoss = 1 - Dice
    """
    
    def __init__(self, smooth: float = 1.0):
        super().__init__()
        self.smooth = smooth
    
    def forward(self, logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        """
        Args:
            logits: Raw model output (B, 1, H, W). Sigmoid is applied internally.
            targets: Binary ground truth (B, 1, H, W) in {0, 1}.
        Returns:
            Scalar loss value.
        """
        probs = torch.sigmoid(logits)
        
        # Flatten spatial dimensions
        probs_flat = probs.view(probs.size(0), -1)
        targets_flat = targets.view(targets.size(0), -1)
        
        intersection = (probs_flat * targets_flat).sum(dim=1)
        union = probs_flat.sum(dim=1) + targets_flat.sum(dim=1)
        
        dice = (2.0 * intersection + self.smooth) / (union + self.smooth)
        
        return 1.0 - dice.mean()
