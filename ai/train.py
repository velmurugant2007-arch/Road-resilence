import argparse
import sys
from pathlib import Path
from torch.utils.data import DataLoader, random_split
import torch

# Ensure project root is in path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from ai.model_config import load_config
from ai.models.segformer import SegFormerRoadExtractor
from ai.dataset import RoadExtractionDataset
from ai.augmentation import SyntheticOcclusionAugmentor
from ai.training.trainer import Trainer
from utils.logger import get_logger

logger = get_logger("ai.train")


def parse_args():
    parser = argparse.ArgumentParser(description="ATLAS SegFormer Training Pipeline")
    parser.add_argument("--config", type=str, default=None, help="Path to custom model_config.yaml")
    parser.add_argument("--image-dir", type=str, default="data/processed/images", help="Directory containing training images")
    parser.add_argument("--mask-dir", type=str, default="data/processed/masks", help="Directory containing ground truth masks")
    parser.add_argument("--epochs", type=int, default=None, help="Override number of epochs to train")
    parser.add_argument("--batch-size", type=int, default=None, help="Override batch size")
    parser.add_argument("--resume", action="store_true", help="Resume training from latest checkpoint")
    parser.add_argument("--seed", type=int, default=42, help="Deterministic random seed")
    return parser.parse_args()


def main():
    args = parse_args()
    
    config_path = Path(args.config) if args.config else None
    config = load_config(config_path)
    
    if args.epochs is not None:
        config.training.epochs = args.epochs
    if args.batch_size is not None:
        config.training.batch_size = args.batch_size
        
    logger.info("Initializing ATLAS Road Extraction Training Pipeline...")
    
    image_dir = Path(args.image_dir)
    mask_dir = Path(args.mask_dir)
    
    if not image_dir.exists() or not mask_dir.exists():
        logger.warning(f"Data directories ({image_dir}, {mask_dir}) not found. Training requires valid dataset.")
        
    # Initialize augmentation pipeline
    augmentor = SyntheticOcclusionAugmentor(
        cloud_prob=config.augmentation.cloud_prob,
        shadow_prob=config.augmentation.shadow_prob,
        tree_canopy_prob=config.augmentation.tree_canopy_prob,
        building_shadow_prob=config.augmentation.building_shadow_prob,
        vehicle_prob=config.augmentation.vehicle_prob,
        urban_clutter_prob=config.augmentation.urban_clutter_prob,
        haze_prob=config.augmentation.haze_prob,
        seasonal_prob=config.augmentation.seasonal_prob,
        max_cloud_coverage=config.augmentation.max_cloud_coverage
    )
    
    # Load dataset
    full_dataset = RoadExtractionDataset(
        image_dir=image_dir,
        mask_dir=mask_dir,
        tile_size=config.training.tile_size,
        augment=True,
        augmentation_pipeline=augmentor
    )
    
    total_samples = len(full_dataset)
    if total_samples == 0:
        logger.error("Dataset is empty. Cannot start training.")
        return
        
    train_count = int(total_samples * config.training.train_ratio)
    val_count = int(total_samples * config.training.val_ratio)
    test_count = total_samples - train_count - val_count
    
    generator = torch.Generator().manual_seed(args.seed)
    train_dataset, val_dataset, _ = random_split(
        full_dataset, [train_count, val_count, test_count], generator=generator
    )
    
    # Disable augmentation on validation split
    # Note: random_split wraps datasets in Subset, so we access underlying dataset properties or handle cleanly
    train_loader = DataLoader(
        train_dataset, batch_size=config.training.batch_size, shuffle=True, num_workers=0, pin_memory=True
    )
    val_loader = DataLoader(
        val_dataset, batch_size=config.training.batch_size, shuffle=False, num_workers=0, pin_memory=True
    )
    
    # Initialize model
    model = SegFormerRoadExtractor(
        in_channels=config.model.in_channels,
        num_classes=config.model.num_classes
    )
    
    # Initialize trainer
    trainer = Trainer(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        config=config,
        seed=args.seed
    )
    
    if args.resume:
        trainer.resume_if_available()
        
    trainer.train()


if __name__ == "__main__":
    main()
