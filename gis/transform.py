import numpy as np
import torch
import torchvision.transforms as T
from utils.logger import get_logger

logger = get_logger("gis.transform")

class GISTransformer:
    """
    Handles pixel normalization and CRS transformations.
    Strictly uses ImageNet Mean/Std as dictated by the CER v2 to preserve SegFormer weights.
    """
    def __init__(self):
        # ImageNet statistics for pre-trained weights
        self.mean = [0.485, 0.456, 0.406]
        self.std = [0.229, 0.224, 0.225]
        
        # PyTorch vision transform pipeline
        self.normalize = T.Normalize(mean=self.mean, std=self.std)

    def to_model_tensor(self, tile_data: np.ndarray) -> torch.Tensor:
        """
        Converts a raw numpy array (C, H, W) from rasterio into a normalized PyTorch tensor ready for the AI model.
        """
        # 1. Convert to float32 (ensuring contiguous memory layout)
        tensor = torch.from_numpy(np.ascontiguousarray(tile_data)).float()
        
        # 2. Scale 8-bit integers (0-255) to (0.0 - 1.0) if not already float
        # Note: If the GeoTIFF is 16-bit, custom scaling is required before this step.
        if tensor.max() > 1.0:
            tensor = tensor / 255.0
            
        # 3. Ensure we only take the first 3 channels (RGB). Discard Alpha or Near-Infrared if present.
        if tensor.shape[0] > 3:
            tensor = tensor[:3, :, :]
        elif tensor.shape[0] < 3:
            logger.error("Input tile has less than 3 channels. SegFormer requires RGB.")
            raise ValueError("Input tile requires 3 channels (RGB).")
            
        # 4. Apply ImageNet Normalization
        normalized_tensor = self.normalize(tensor)
        
        return normalized_tensor
