import torch
import torch.nn as nn
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from ai.models.segformer import SegFormerRoadExtractor
from ai.model_config import InferenceConfig
from gis.transform import GISTransformer
from utils.logger import get_logger

logger = get_logger("ai.inference")


@dataclass
class InferenceResult:
    """
    Dual output as required by the architecture:
    - probability_map: Raw softmax/sigmoid confidence (float32, 0.0-1.0)
      → Primary input for Graph Healing Hybrid Cost Function
    - binary_mask: Thresholded road mask (uint8, 0 or 1)
      → Input for Skeletonization and Vectorization
    """
    probability_map: np.ndarray   # (H, W) float32 in [0, 1]
    binary_mask: np.ndarray       # (H, W) uint8 in {0, 1}


class RoadInferencePipeline:
    """
    Production inference pipeline for road extraction.
    
    Architecture Traceability:
        - Defined in: low_level_architecture.md (Module 2)
        - Outputs: Probability mask + Binary mask
        - Confidence map feeds into Graph Healing (mathematical_design.md Section 3)
    
    ISRO Alignment:
        FR-02: Semantic segmentation under occlusions.
        FR-03: Confidence map indicating occlusion severity.
    """
    
    def __init__(
        self,
        model: SegFormerRoadExtractor,
        config: Optional[InferenceConfig] = None,
        device: str = "cpu",
    ):
        self.model = model.to(device)
        self.model.eval()
        self.device = device
        self.config = config or InferenceConfig()
        self.transformer = GISTransformer()
        
        logger.info(f"Inference pipeline initialized on {device}. "
                     f"Threshold={self.config.confidence_threshold}")
    
    @torch.no_grad()
    def predict_tile(self, tile_np: np.ndarray) -> InferenceResult:
        """
        Run inference on a single tile (C, H, W) numpy array.
        
        Args:
            tile_np: Raw rasterio output (C, H, W), uint8 or float.
        
        Returns:
            InferenceResult with probability_map and binary_mask.
        """
        # Normalize using ImageNet stats
        tensor = self.transformer.to_model_tensor(tile_np)
        # Add batch dimension
        tensor = tensor.unsqueeze(0).to(self.device)
        
        # Forward pass (AMP-compatible)
        with torch.amp.autocast(device_type=self.device if self.device != "cpu" else "cpu", enabled=self.device != "cpu"):
            logits = self.model(tensor)
        
        # Sigmoid to get probabilities
        probs = torch.sigmoid(logits).squeeze(0).squeeze(0)  # (H, W)
        probability_map = probs.cpu().numpy().astype(np.float32)
        
        # Threshold for binary mask
        binary_mask = (probability_map >= self.config.confidence_threshold).astype(np.uint8)
        
        return InferenceResult(
            probability_map=probability_map,
            binary_mask=binary_mask,
        )
    
    @torch.no_grad()
    def predict_batch(self, tiles: list[np.ndarray]) -> list[InferenceResult]:
        """
        Batched inference for throughput. Each tile is (C, H, W).
        """
        tensors = [self.transformer.to_model_tensor(t) for t in tiles]
        batch = torch.stack(tensors).to(self.device)
        
        with torch.amp.autocast(device_type=self.device if self.device != "cpu" else "cpu", enabled=self.device != "cpu"):
            logits = self.model(batch)
        
        probs = torch.sigmoid(logits).cpu().numpy()
        
        results = []
        for i in range(probs.shape[0]):
            prob_map = probs[i, 0].astype(np.float32)
            bin_mask = (prob_map >= self.config.confidence_threshold).astype(np.uint8)
            results.append(InferenceResult(probability_map=prob_map, binary_mask=bin_mask))
        
        return results

    @classmethod
    def from_checkpoint(cls, checkpoint_path: str | Path, device: str = "cpu", config: Optional[InferenceConfig] = None):
        """Factory method: load model from a saved checkpoint file."""
        data = torch.load(checkpoint_path, map_location=device)
        model = SegFormerRoadExtractor()
        model.load_state_dict(data["model_state_dict"])
        logger.info(f"Model loaded from checkpoint: {checkpoint_path}")
        return cls(model=model, config=config, device=device)
