import numpy as np
from pathlib import Path
from scipy import ndimage
from utils.logger import get_logger

logger = get_logger("ai.dataset_stats")


def compute_dataset_statistics(image_dir: Path | str, mask_dir: Path | str) -> dict:
    """
    Generates pre-training dataset statistics for quality assurance.
    
    Returns a comprehensive report including:
        - Sample count
        - Road/background pixel ratio (class imbalance check)
        - Average brightness
        - Average connected components per mask
    """
    import rasterio

    image_dir = Path(image_dir)
    mask_dir = Path(mask_dir)
    
    image_paths = sorted(image_dir.glob("*.tif")) + sorted(image_dir.glob("*.png"))
    mask_paths = sorted(mask_dir.glob("*.tif")) + sorted(mask_dir.glob("*.png"))

    total_road_pixels = 0
    total_bg_pixels = 0
    brightness_values = []
    connected_components_counts = []

    for img_path, mask_path in zip(image_paths, mask_paths):
        # Image stats
        with rasterio.open(img_path) as src:
            img = src.read().astype(np.float32)
            brightness_values.append(img.mean())

        # Mask stats
        with rasterio.open(mask_path) as src:
            mask = src.read(1)
            binary = (mask > 0).astype(np.uint8)
            road_px = binary.sum()
            bg_px = binary.size - road_px
            total_road_pixels += road_px
            total_bg_pixels += bg_px

            # Connected components (topology indicator)
            labeled, num_features = ndimage.label(binary)
            connected_components_counts.append(num_features)

    total_pixels = total_road_pixels + total_bg_pixels
    road_ratio = total_road_pixels / max(total_pixels, 1)

    report = {
        "num_samples": len(image_paths),
        "total_road_pixels": int(total_road_pixels),
        "total_bg_pixels": int(total_bg_pixels),
        "road_pixel_ratio": round(float(road_ratio), 4),
        "bg_pixel_ratio": round(1.0 - float(road_ratio), 4),
        "avg_brightness": round(float(np.mean(brightness_values)), 2) if brightness_values else 0.0,
        "avg_connected_components": round(float(np.mean(connected_components_counts)), 2) if connected_components_counts else 0.0,
        "max_connected_components": int(max(connected_components_counts)) if connected_components_counts else 0,
        "min_connected_components": int(min(connected_components_counts)) if connected_components_counts else 0,
    }

    logger.info(f"Dataset Statistics: {report}")
    return report


def save_statistics_report(stats: dict, output_path: Path | str):
    """Writes a human-readable dataset summary report to markdown."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Dataset Statistics Report\n",
        f"**Samples**: {stats['num_samples']}\n",
        f"**Road Pixel Ratio**: {stats['road_pixel_ratio']:.2%}",
        f"**Background Pixel Ratio**: {stats['bg_pixel_ratio']:.2%}\n",
        f"**Average Brightness**: {stats['avg_brightness']}\n",
        f"**Avg Connected Components per Mask**: {stats['avg_connected_components']}",
        f"**Range**: [{stats['min_connected_components']}, {stats['max_connected_components']}]\n",
    ]

    if stats["road_pixel_ratio"] < 0.05:
        lines.append("> [!WARNING]\n> Severe class imbalance detected. Consider weighted loss or oversampling.\n")

    if stats["avg_connected_components"] > 50:
        lines.append("> [!WARNING]\n> High fragmentation in ground truth masks. Check mask quality.\n")

    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    logger.info(f"Statistics report saved to {output_path}")
