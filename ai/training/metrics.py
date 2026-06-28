import torch
import torch.nn as nn
from typing import Dict
from ai.loss.soft_skeleton import SoftSkeletonize
from utils.logger import get_logger

logger = get_logger("ai.training.metrics")


class RoadMetrics(nn.Module):
    """
    Evaluates segmentation performance across pixel-level and topological metrics.
    
    Metrics:
        - IoU (Intersection over Union / Jaccard Index)
        - Dice Score (F1 score for spatial overlap)
        - Precision
        - Recall
        - F1 Score
        - Connectivity Ratio (Topology Sensitivity via Skeleton Overlap)
        
    ISRO Alignment:
        FR-02 & HR-01: Verifies that road network topological continuity is maintained.
    """
    
    def __init__(self, threshold: float = 0.5, skeleton_iterations: int = 10, smooth: float = 1e-6):
        super().__init__()
        self.threshold = threshold
        self.smooth = smooth
        self.skeletonizer = SoftSkeletonize(num_iterations=skeleton_iterations)
    
    @torch.no_grad()
    def forward(self, logits: torch.Tensor, targets: torch.Tensor) -> Dict[str, float]:
        """
        Args:
            logits: Raw model outputs (B, 1, H, W).
            targets: Ground truth binary masks (B, 1, H, W) in {0, 1}.
            
        Returns:
            Dictionary mapping metric names to float values.
        """
        probs = torch.sigmoid(logits)
        preds = (probs >= self.threshold).float()
        
        # Flatten spatial dimensions
        preds_flat = preds.view(-1)
        targets_flat = targets.view(-1)
        
        tp = (preds_flat * targets_flat).sum()
        fp = (preds_flat * (1.0 - targets_flat)).sum()
        fn = ((1.0 - preds_flat) * targets_flat).sum()
        
        # Pixel metrics
        precision = (tp + self.smooth) / (tp + fp + self.smooth)
        recall = (tp + self.smooth) / (tp + fn + self.smooth)
        f1 = (2.0 * precision * recall) / (precision + recall + self.smooth)
        
        iou = (tp + self.smooth) / (tp + fp + fn + self.smooth)
        dice = (2.0 * tp + self.smooth) / (2.0 * tp + fp + fn + self.smooth)
        
        # Topological Connectivity Ratio (Skeleton Recall / Topology Sensitivity)
        # Measures what fraction of the ground truth road centerlines are preserved
        skel_target = self.skeletonizer(targets)
        connectivity_ratio = ((skel_target * probs).sum() + self.smooth) / (skel_target.sum() + self.smooth)
        
        return {
            "iou": float(iou.item()),
            "dice": float(dice.item()),
            "precision": float(precision.item()),
            "recall": float(recall.item()),
            "f1": float(f1.item()),
            "connectivity_ratio": float(connectivity_ratio.item()),
        }
