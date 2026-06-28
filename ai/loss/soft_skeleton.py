import torch
import torch.nn as nn
import torch.nn.functional as F
from utils.logger import get_logger

logger = get_logger("ai.loss.soft_skeleton")


class SoftSkeletonize(nn.Module):
    """
    Differentiable soft-skeletonization via iterative min-pooling and max-pooling.
    
    This is a STANDALONE REUSABLE MODULE — not embedded inside clDice.
    It can be used independently for visualization, debugging, or any
    downstream module that needs an approximate centerline.
    
    Engineering Justification (CER v2, Issue #1):
        Zhang-Suen thinning is a discrete, non-differentiable algorithm.
        It CANNOT be used inside a PyTorch training loop because gradients
        cannot flow through integer morphological operations.
        
        This module approximates skeletonization using continuous pooling
        operations, ensuring full gradient flow through the clDice loss
        back into the SegFormer encoder.
    
    Architecture Traceability:
        - mathematical_design.md Section 1 (Soft-Skeletonization)
        - ai_architecture.md Section 3 (Differentiable clDice)
    
    Algorithm:
        1. Erode the mask using min-pooling (shrinks boundaries).
        2. Dilate the eroded result using max-pooling (restores bulk).
        3. Subtract the opened (eroded→dilated) mask from the original.
           The residual is the thin boundary/skeleton.
        4. Repeat iteratively to progressively extract thinner structures.
        5. Accumulate all residuals into the final soft skeleton.
    """
    
    def __init__(self, num_iterations: int = 10):
        super().__init__()
        self.num_iterations = num_iterations
    
    def _soft_erode(self, x: torch.Tensor) -> torch.Tensor:
        """Min-pooling: shrinks foreground regions."""
        # Negate, max-pool, negate back = min-pool
        return -F.max_pool2d(-x, kernel_size=3, stride=1, padding=1)
    
    def _soft_dilate(self, x: torch.Tensor) -> torch.Tensor:
        """Max-pooling: expands foreground regions."""
        return F.max_pool2d(x, kernel_size=3, stride=1, padding=1)
    
    def _soft_open(self, x: torch.Tensor) -> torch.Tensor:
        """Morphological opening: erode then dilate (removes thin structures)."""
        return self._soft_dilate(self._soft_erode(x))
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Compute the soft skeleton of a probability mask.
        
        Args:
            x: Probability mask (B, 1, H, W) in [0, 1].
        
        Returns:
            Soft skeleton (B, 1, H, W) in [0, 1].
            Thin, continuous centerlines of the road mask.
        """
        skeleton = torch.zeros_like(x)
        current = x.clone()
        
        for _ in range(self.num_iterations):
            opened = self._soft_open(current)
            # The skeleton residual: what opening removes (thin structures)
            residual = torch.clamp(current - opened, min=0.0)
            skeleton = skeleton + residual
            # Erode for next iteration (progressively thinner)
            current = self._soft_erode(current)
        
        # Clamp to [0, 1]
        skeleton = torch.clamp(skeleton, 0.0, 1.0)
        
        return skeleton
