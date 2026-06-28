import torch
import torch.nn as nn
from ai.loss.soft_skeleton import SoftSkeletonize
from utils.logger import get_logger

logger = get_logger("ai.loss.cldice")


class CLDiceLoss(nn.Module):
    """
    centerline-Dice Loss (clDice) for topology-preserving segmentation.
    
    Standard Dice measures pixel overlap. clDice measures SKELETON overlap.
    A prediction can have 95% Dice but 0% clDice if it produces thick blobs
    with broken centerlines.
    
    This loss forces the model to prioritize unbroken thin road structures
    over thick, pixel-accurate but topologically fragmented masks.
    
    Architecture Traceability:
        - mathematical_design.md Section 1
        - ai_architecture.md Section 3
    
    Formula:
        T_prec = |S_P ∩ G| / |S_P|  (skeleton of prediction intersected with GT)
        T_sens = |S_G ∩ P| / |S_G|  (skeleton of GT intersected with prediction)
        clDice = 2 * T_prec * T_sens / (T_prec + T_sens)
        Loss = 1 - clDice
    """
    
    def __init__(self, num_iterations: int = 10, smooth: float = 1.0):
        super().__init__()
        self.skeletonizer = SoftSkeletonize(num_iterations=num_iterations)
        self.smooth = smooth
    
    def forward(self, logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        """
        Args:
            logits: Raw model output (B, 1, H, W). Sigmoid applied internally.
            targets: Binary ground truth (B, 1, H, W) in {0, 1}.
        Returns:
            Scalar clDice loss.
        """
        probs = torch.sigmoid(logits)
        
        # Compute soft skeletons
        skel_pred = self.skeletonizer(probs)
        skel_target = self.skeletonizer(targets)
        
        # Topology Precision: skeleton of prediction covered by ground truth
        t_prec_num = (skel_pred * targets).sum()
        t_prec_den = skel_pred.sum()
        t_prec = (t_prec_num + self.smooth) / (t_prec_den + self.smooth)
        
        # Topology Sensitivity: skeleton of GT covered by prediction
        t_sens_num = (skel_target * probs).sum()
        t_sens_den = skel_target.sum()
        t_sens = (t_sens_num + self.smooth) / (t_sens_den + self.smooth)
        
        # Harmonic mean
        cldice = 2.0 * (t_prec * t_sens) / (t_prec + t_sens + 1e-8)
        
        return 1.0 - cldice
