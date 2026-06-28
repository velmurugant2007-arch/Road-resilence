import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for headless environments
import matplotlib.pyplot as plt
import rasterio
from ai.augmentation import SyntheticOcclusionAugmentor
from utils.logger import get_logger

logger = get_logger("ai.augmentation_report")


def generate_augmentation_report(
    image_dir: Path | str,
    mask_dir: Path | str,
    output_dir: Path | str,
    num_samples: int = 4,
):
    """
    Generates a visual report:  Original → Augmented → Ground Truth Mask
    for a representative sample of the dataset.
    
    Saves individual comparison images to the output directory.
    """
    image_dir = Path(image_dir)
    mask_dir = Path(mask_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    image_paths = sorted(image_dir.glob("*.tif")) + sorted(image_dir.glob("*.png"))
    mask_paths = sorted(mask_dir.glob("*.tif")) + sorted(mask_dir.glob("*.png"))

    if len(image_paths) == 0:
        logger.warning("No images found for augmentation report.")
        return

    # Sample evenly across the dataset
    indices = np.linspace(0, len(image_paths) - 1, min(num_samples, len(image_paths)), dtype=int)
    augmentor = SyntheticOcclusionAugmentor()

    for i, idx in enumerate(indices):
        with rasterio.open(image_paths[idx]) as src:
            original = src.read()  # (C, H, W)
        with rasterio.open(mask_paths[idx]) as src:
            mask = src.read(1)  # (H, W)

        # Run augmentation
        aug_image, _ = augmentor.apply(original.copy(), mask[np.newaxis, :, :].astype(np.float32).copy())

        # Convert to displayable format (H, W, C) for matplotlib
        orig_rgb = np.transpose(original[:3], (1, 2, 0))
        aug_rgb = np.transpose(aug_image[:3], (1, 2, 0))

        # Clip to valid range
        orig_rgb = np.clip(orig_rgb, 0, 255).astype(np.uint8)
        aug_rgb = np.clip(aug_rgb, 0, 255).astype(np.uint8)

        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        axes[0].imshow(orig_rgb)
        axes[0].set_title("Original Image", fontsize=14, fontweight="bold")
        axes[0].axis("off")

        axes[1].imshow(aug_rgb)
        axes[1].set_title("Augmented Image", fontsize=14, fontweight="bold")
        axes[1].axis("off")

        axes[2].imshow(mask, cmap="gray")
        axes[2].set_title("Ground Truth Mask", fontsize=14, fontweight="bold")
        axes[2].axis("off")

        plt.suptitle(f"Sample {i + 1}: {image_paths[idx].name}", fontsize=16)
        plt.tight_layout()

        save_path = output_dir / f"augmentation_sample_{i + 1}.png"
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()

        logger.info(f"Augmentation report sample {i + 1} saved to {save_path}")

    logger.info(f"Augmentation report complete. {len(indices)} samples generated in {output_dir}")
