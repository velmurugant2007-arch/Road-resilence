import torch
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
from ai.loss.soft_skeleton import SoftSkeletonize
from utils.logger import get_logger

logger = get_logger("ai.loss.visualize")


def visualize_skeleton_debug(
    prediction: torch.Tensor,
    ground_truth: torch.Tensor,
    output_path: Path | str,
    num_iterations: int = 10,
    sample_index: int = 0,
):
    """
    Generates a 4-panel debug visualization:
        1. Prediction (sigmoid applied)
        2. Soft Skeleton of Prediction
        3. Soft Skeleton of Ground Truth
        4. Difference (highlights topology mismatches)
    
    This is essential for debugging whether the clDice loss is 
    correctly penalizing topological breaks.
    
    Args:
        prediction: Raw logits (B, 1, H, W).
        ground_truth: Binary mask (B, 1, H, W).
        output_path: Where to save the PNG.
        num_iterations: Soft skeleton iterations.
        sample_index: Which batch sample to visualize.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    skeletonizer = SoftSkeletonize(num_iterations=num_iterations)
    
    with torch.no_grad():
        probs = torch.sigmoid(prediction)
        skel_pred = skeletonizer(probs)
        skel_gt = skeletonizer(ground_truth)
        difference = torch.abs(skel_pred - skel_gt)
    
    # Extract single sample
    pred_np = probs[sample_index, 0].cpu().numpy()
    skel_pred_np = skel_pred[sample_index, 0].cpu().numpy()
    skel_gt_np = skel_gt[sample_index, 0].cpu().numpy()
    diff_np = difference[sample_index, 0].cpu().numpy()
    
    fig, axes = plt.subplots(1, 4, figsize=(24, 6))
    
    axes[0].imshow(pred_np, cmap='gray')
    axes[0].set_title("Prediction (Sigmoid)", fontsize=14, fontweight='bold')
    axes[0].axis('off')
    
    axes[1].imshow(skel_pred_np, cmap='hot')
    axes[1].set_title("Soft Skeleton (Prediction)", fontsize=14, fontweight='bold')
    axes[1].axis('off')
    
    axes[2].imshow(skel_gt_np, cmap='hot')
    axes[2].set_title("Soft Skeleton (Ground Truth)", fontsize=14, fontweight='bold')
    axes[2].axis('off')
    
    axes[3].imshow(diff_np, cmap='RdYlGn_r')
    axes[3].set_title("Difference (Topology Errors)", fontsize=14, fontweight='bold')
    axes[3].axis('off')
    
    plt.suptitle("clDice Skeleton Debug Visualization", fontsize=16)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Skeleton debug visualization saved to {output_path}")


def visualize_loss_components(
    loss_history: dict,
    output_path: Path | str,
):
    """
    Plots the training curves for each individual loss component.
    
    Args:
        loss_history: dict with keys "total", "bce", "dice", "cldice",
                      each mapping to a list of per-epoch values.
        output_path: Where to save the PNG.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    components = [
        ("total", "Total Loss", "tab:blue"),
        ("bce", "BCE Loss", "tab:orange"),
        ("dice", "Dice Loss", "tab:green"),
        ("cldice", "clDice Loss", "tab:red"),
    ]
    
    for ax, (key, title, color) in zip(axes.flat, components):
        if key in loss_history and loss_history[key]:
            ax.plot(loss_history[key], color=color, linewidth=2)
            ax.set_title(title, fontsize=14, fontweight='bold')
            ax.set_xlabel("Epoch")
            ax.set_ylabel("Loss")
            ax.grid(True, alpha=0.3)
    
    plt.suptitle("Training Loss Components", fontsize=16)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Loss component plot saved to {output_path}")
