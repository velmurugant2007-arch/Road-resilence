import torch
import torch.nn as nn
from ai.loss.bce import WeightedBCELoss
from ai.loss.dice import DiceLoss
from ai.loss.cldice import CLDiceLoss
from ai.model_config import LossConfig
from utils.logger import get_logger

logger = get_logger("ai.loss.combined")


class CombinedLoss(nn.Module):
    """
    Configurable combined loss function for topology-aware road extraction.
    
    Supports any weighted combination of BCE, Dice, and clDice losses.
    Weights are driven by the centralized model_config.yaml.
    
    Each component is logged separately during training for diagnostics.
    
    Architecture Traceability:
        - mathematical_design.md Section 1: L_total = α * L_Dice + (1-α) * (1 - clDice)
        - model_config.yaml: loss.dice_weight, loss.cldice_weight
    """
    
    def __init__(self, config: LossConfig = None):
        super().__init__()
        if config is None:
            config = LossConfig()
        
        self.dice_weight = config.dice_weight
        self.cldice_weight = config.cldice_weight
        self.bce_weight = 1.0 - self.dice_weight - self.cldice_weight
        if self.bce_weight < 0:
            self.bce_weight = 0.0
        
        self.bce = WeightedBCELoss(pos_weight=2.0)
        self.dice = DiceLoss()
        self.cldice = CLDiceLoss(num_iterations=config.soft_skeleton_iterations)
        
        logger.info(
            f"CombinedLoss initialized — "
            f"BCE: {self.bce_weight:.2f}, "
            f"Dice: {self.dice_weight:.2f}, "
            f"clDice: {self.cldice_weight:.2f}"
        )
    
    def forward(self, logits: torch.Tensor, targets: torch.Tensor) -> dict:
        """
        Computes all loss components and returns them individually for logging.
        
        Args:
            logits: Raw model output (B, 1, H, W).
            targets: Binary ground truth (B, 1, H, W).
        
        Returns:
            dict with keys:
                "total": weighted combined loss (for backprop)
                "bce": BCE component value
                "dice": Dice component value
                "cldice": clDice component value
        """
        loss_bce = self.bce(logits, targets)
        loss_dice = self.dice(logits, targets)
        loss_cldice = self.cldice(logits, targets)
        
        total = (
            self.bce_weight * loss_bce
            + self.dice_weight * loss_dice
            + self.cldice_weight * loss_cldice
        )
        
        return {
            "total": total,
            "bce": loss_bce.detach(),
            "dice": loss_dice.detach(),
            "cldice": loss_cldice.detach(),
        }
