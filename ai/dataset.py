import torch
from torch.utils.data import Dataset
from pathlib import Path
from typing import Tuple, Optional
import numpy as np
import rasterio
from gis.transform import GISTransformer
from utils.logger import get_logger

logger = get_logger("ai.dataset")


class RoadExtractionDataset(Dataset):
    """
    PyTorch Dataset for satellite road extraction.
    
    Loads paired satellite imagery and ground truth road masks.
    Applies synthetic cloud/shadow augmentations during training
    to teach the model occlusion robustness.
    
    ISRO Alignment:
        FR-02: Semantic segmentation maintaining connectivity under occlusions.
        HR-01: Topological priority — ground truth masks preserve road connectivity.
    
    Architecture Traceability:
        - Defined in: ai_architecture.md (Section 3)
        - Loss compatibility: Masks are binary {0, 1} for Dice/clDice computation.
        - Normalization: ImageNet Mean/Std via GISTransformer (CER v2 Fix #4).
    """
    
    def __init__(
        self,
        image_dir: Path | str,
        mask_dir: Path | str,
        tile_size: int = 512,
        augment: bool = False,
        augmentation_pipeline: Optional["SyntheticOcclusionAugmentor"] = None,
    ):
        self.image_dir = Path(image_dir)
        self.mask_dir = Path(mask_dir)
        self.tile_size = tile_size
        self.augment = augment
        self.augmentor = augmentation_pipeline
        self.transformer = GISTransformer()
        
        # Discover paired files
        self.image_paths = sorted(self.image_dir.glob("*.tif")) + sorted(self.image_dir.glob("*.png"))
        self.mask_paths = sorted(self.mask_dir.glob("*.tif")) + sorted(self.mask_dir.glob("*.png"))
        
        if len(self.image_paths) != len(self.mask_paths):
            logger.error(
                f"Image/Mask count mismatch: {len(self.image_paths)} images vs {len(self.mask_paths)} masks"
            )
            raise ValueError("Image and mask directories must contain the same number of files.")
        
        if len(self.image_paths) == 0:
            logger.warning(f"No images found in {self.image_dir}. Dataset is empty.")
            
        logger.info(f"RoadExtractionDataset initialized with {len(self.image_paths)} samples. Augmentation: {augment}")
    
    def __len__(self) -> int:
        return len(self.image_paths)
    
    def _load_image(self, path: Path) -> np.ndarray:
        """Load image as numpy array (C, H, W)."""
        with rasterio.open(path) as src:
            data = src.read()  # Shape: (C, H, W)
        return data
    
    def _load_mask(self, path: Path) -> np.ndarray:
        """Load mask as single-channel binary numpy array (1, H, W)."""
        with rasterio.open(path) as src:
            data = src.read(1)  # Read only band 1
        # Binarize: anything > 0 is road
        mask = (data > 0).astype(np.float32)
        return mask[np.newaxis, :, :]  # Add channel dim -> (1, H, W)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        image_np = self._load_image(self.image_paths[idx])
        mask_np = self._load_mask(self.mask_paths[idx])
        
        # Apply synthetic occlusion augmentations (clouds/shadows) during training
        if self.augment and self.augmentor is not None:
            image_np, mask_np = self.augmentor.apply(image_np, mask_np)
        
        # Normalize image using ImageNet stats (CER v2 requirement)
        image_tensor = self.transformer.to_model_tensor(image_np)
        
        # Mask remains a raw binary tensor — ensure contiguous memory
        mask_tensor = torch.from_numpy(np.ascontiguousarray(mask_np)).float()
        
        return image_tensor, mask_tensor
