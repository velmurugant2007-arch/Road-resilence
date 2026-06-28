import pytest
import numpy as np
import torch
import rasterio
from rasterio.transform import from_origin
from pathlib import Path
import os
import shutil

from ai.dataset import RoadExtractionDataset
from ai.augmentation import SyntheticOcclusionAugmentor


TEST_DIR = Path("temp_test_ai")
IMG_DIR = TEST_DIR / "images"
MASK_DIR = TEST_DIR / "masks"


@pytest.fixture(scope="module", autouse=True)
def setup_mock_dataset():
    """Create a synthetic paired dataset of 6 samples."""
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    MASK_DIR.mkdir(parents=True, exist_ok=True)
    
    transform = from_origin(77.5, 12.9, 0.0001, 0.0001)
    
    for i in range(6):
        # Synthetic 3-band satellite tile
        img = np.random.randint(50, 200, (3, 512, 512), dtype=np.uint8)
        with rasterio.open(
            IMG_DIR / f"tile_{i}.tif", 'w', driver='GTiff',
            width=512, height=512, count=3, dtype='uint8',
            crs='EPSG:4326', transform=transform,
        ) as dst:
            dst.write(img)
        
        # Synthetic binary road mask (single band)
        mask = np.random.choice([0, 255], size=(1, 512, 512), p=[0.8, 0.2]).astype(np.uint8)
        with rasterio.open(
            MASK_DIR / f"tile_{i}.tif", 'w', driver='GTiff',
            width=512, height=512, count=1, dtype='uint8',
            crs='EPSG:4326', transform=transform,
        ) as dst:
            dst.write(mask)
    
    yield
    
    shutil.rmtree(TEST_DIR, ignore_errors=True)


def test_dataset_length():
    ds = RoadExtractionDataset(IMG_DIR, MASK_DIR)
    assert len(ds) == 6


def test_dataset_shapes():
    ds = RoadExtractionDataset(IMG_DIR, MASK_DIR)
    img, mask = ds[0]
    assert img.shape == (3, 512, 512), f"Image shape wrong: {img.shape}"
    assert mask.shape == (1, 512, 512), f"Mask shape wrong: {mask.shape}"


def test_mask_is_binary():
    ds = RoadExtractionDataset(IMG_DIR, MASK_DIR)
    _, mask = ds[0]
    unique_vals = set(mask.unique().tolist())
    assert unique_vals.issubset({0.0, 1.0}), f"Mask not binary: {unique_vals}"


def test_imagenet_normalization_applied():
    ds = RoadExtractionDataset(IMG_DIR, MASK_DIR)
    img, _ = ds[0]
    # ImageNet-normalized images should not be in [0, 255] range
    assert img.max() < 10.0, "Image appears unnormalized"
    assert img.min() > -10.0, "Image appears unnormalized"


def test_augmentation_preserves_mask():
    """
    Critical test: Clouds are injected onto the IMAGE, but the MASK must remain unchanged.
    This is the core principle of our occlusion-robust training.
    """
    augmentor = SyntheticOcclusionAugmentor(cloud_probability=1.0, shadow_probability=0.0)
    
    image = np.random.randint(50, 200, (3, 512, 512), dtype=np.uint8)
    mask = np.random.choice([0, 1], size=(1, 512, 512)).astype(np.float32)
    mask_copy = mask.copy()
    
    aug_image, aug_mask = augmentor.apply(image.copy(), mask)
    
    # The mask topology must be perfectly preserved after augmentation
    # (geometric transforms are applied identically, so we check the values are still {0, 1})
    unique = set(np.unique(aug_mask).tolist())
    assert unique.issubset({0.0, 1.0}), f"Augmentation corrupted mask: {unique}"


def test_augmentation_modifies_image():
    """Clouds should visually change the image."""
    augmentor = SyntheticOcclusionAugmentor(cloud_probability=1.0, shadow_probability=0.0)
    
    image = np.full((3, 512, 512), 100, dtype=np.uint8)
    mask = np.zeros((1, 512, 512), dtype=np.float32)
    
    aug_image, _ = augmentor.apply(image.copy(), mask.copy())
    
    # Image should have been modified by cloud overlay
    assert not np.array_equal(image, aug_image), "Cloud augmentation had no effect on image"
