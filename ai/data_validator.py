from torch.utils.data import DataLoader, random_split
from pathlib import Path
from typing import Tuple
from ai.dataset import RoadExtractionDataset
from ai.augmentation import SyntheticOcclusionAugmentor
from utils.logger import get_logger

logger = get_logger("ai.data_validator")


def create_dataloaders(
    image_dir: Path | str,
    mask_dir: Path | str,
    batch_size: int = 4,
    tile_size: int = 512,
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
    num_workers: int = 0,
) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """
    Creates Train / Validation / Test dataloaders with proper splits.
    
    Architecture Traceability (dataset_strategy.md, Section 2):
        - Training (70%): Augmented with synthetic clouds/shadows.
        - Validation (15%): No augmentation, used for hyperparameter tuning.
        - Testing (15%): No augmentation, geographically isolated ideally.
    """
    # Full dataset WITHOUT augmentation for splitting
    full_dataset = RoadExtractionDataset(
        image_dir=image_dir,
        mask_dir=mask_dir,
        tile_size=tile_size,
        augment=False,
    )
    
    total = len(full_dataset)
    train_size = int(total * train_ratio)
    val_size = int(total * val_ratio)
    test_size = total - train_size - val_size
    
    train_subset, val_subset, test_subset = random_split(
        full_dataset, [train_size, val_size, test_size]
    )
    
    # Create augmented training dataset
    augmentor = SyntheticOcclusionAugmentor()
    train_dataset = RoadExtractionDataset(
        image_dir=image_dir,
        mask_dir=mask_dir,
        tile_size=tile_size,
        augment=True,
        augmentation_pipeline=augmentor,
    )
    # Restrict to train indices
    train_dataset_subset = torch.utils.data.Subset(train_dataset, train_subset.indices)
    
    train_loader = DataLoader(
        train_dataset_subset, batch_size=batch_size, shuffle=True, num_workers=num_workers
    )
    val_loader = DataLoader(
        val_subset, batch_size=batch_size, shuffle=False, num_workers=num_workers
    )
    test_loader = DataLoader(
        test_subset, batch_size=batch_size, shuffle=False, num_workers=num_workers
    )
    
    logger.info(f"Splits — Train: {train_size}, Val: {val_size}, Test: {test_size}")
    
    return train_loader, val_loader, test_loader


def validate_dataloader(loader: DataLoader, expected_channels: int = 3) -> dict:
    """
    Runs a single-batch sanity check on a DataLoader.
    Returns a validation report dict.
    """
    batch = next(iter(loader))
    images, masks = batch
    
    report = {
        "batch_size": images.shape[0],
        "image_shape": list(images.shape),
        "mask_shape": list(masks.shape),
        "image_dtype": str(images.dtype),
        "mask_dtype": str(masks.dtype),
        "image_min": float(images.min()),
        "image_max": float(images.max()),
        "mask_unique_values": sorted(masks.unique().tolist()),
        "channels_correct": images.shape[1] == expected_channels,
        "mask_binary": set(masks.unique().tolist()).issubset({0.0, 1.0}),
    }
    
    all_pass = report["channels_correct"] and report["mask_binary"]
    report["status"] = "PASS" if all_pass else "FAIL"
    
    logger.info(f"DataLoader Validation: {report['status']}")
    return report
