import numpy as np
from utils.logger import get_logger

logger = get_logger("ai.augmentation")


class SyntheticOcclusionAugmentor:
    """
    Generates synthetic clouds and shadows over satellite imagery during training.
    
    Engineering Justification (dataset_strategy.md, Section 3):
        We lack real-world paired data where roads under dense clouds have
        verified ground truth masks. Instead, we overlay synthetic occlusions
        on clear imagery while keeping the ground truth mask INTACT.
        This forces the model to learn to predict roads it cannot see,
        using global context from the visible portions of the tile.
    
    ISRO Alignment:
        FR-02: Maintain connectivity under occlusions.
        HR-01: Topological priority — the model must learn continuity, not just pixels.
    """
    
    def __init__(
        self,
        cloud_probability: float = 0.5,
        shadow_probability: float = 0.3,
        max_cloud_coverage: float = 0.4,
        geometric_flip: bool = True,
        geometric_rotate: bool = True,
    ):
        self.cloud_probability = cloud_probability
        self.shadow_probability = shadow_probability
        self.max_cloud_coverage = max_cloud_coverage
        self.geometric_flip = geometric_flip
        self.geometric_rotate = geometric_rotate
    
    def _generate_perlin_cloud(self, h: int, w: int) -> np.ndarray:
        """
        Generates a smooth, natural-looking cloud mask using multi-octave noise.
        Returns a float mask in [0, 1] where 1 = fully opaque cloud.
        """
        # Multi-scale noise approximation (cheaper than true Perlin)
        cloud = np.zeros((h, w), dtype=np.float32)
        for scale in [4, 8, 16, 32]:
            noise = np.random.randn(h // scale + 1, w // scale + 1).astype(np.float32)
            # Bilinear upsample to full resolution
            from scipy.ndimage import zoom
            upsampled = zoom(noise, (h / (h // scale + 1), w / (w // scale + 1)), order=1)
            # Crop to exact size (zoom can produce off-by-one)
            upsampled = upsampled[:h, :w]
            cloud += upsampled
        
        # Normalize to [0, 1]
        cloud = (cloud - cloud.min()) / (cloud.max() - cloud.min() + 1e-8)
        
        # Threshold to create discrete cloud regions
        coverage_threshold = 1.0 - self.max_cloud_coverage
        cloud = np.where(cloud > coverage_threshold, cloud, 0.0)
        
        return cloud
    
    def _apply_cloud(self, image: np.ndarray) -> np.ndarray:
        """
        Overlays a synthetic white cloud onto the image.
        The cloud is alpha-blended so edges appear natural.
        """
        _, h, w = image.shape
        cloud_mask = self._generate_perlin_cloud(h, w)
        
        # Blend: cloudy pixels become white (255)
        for c in range(image.shape[0]):
            image[c] = (image[c] * (1 - cloud_mask) + 255 * cloud_mask).astype(image.dtype)
        
        return image
    
    def _apply_shadow(self, image: np.ndarray) -> np.ndarray:
        """
        Overlays a synthetic dark shadow shifted from the cloud position.
        Simulates the physical effect of sunlight being blocked.
        """
        _, h, w = image.shape
        shadow_mask = self._generate_perlin_cloud(h, w)
        
        # Shift shadow relative to "sun angle" (simplified as a fixed pixel offset)
        shift_x, shift_y = np.random.randint(10, 30), np.random.randint(10, 30)
        shadow_mask = np.roll(shadow_mask, shift_x, axis=1)
        shadow_mask = np.roll(shadow_mask, shift_y, axis=0)
        
        # Darken: shadow pixels lose 60% brightness
        for c in range(image.shape[0]):
            image[c] = (image[c] * (1 - 0.6 * shadow_mask)).astype(image.dtype)
        
        return image
    
    def _apply_geometric(self, image: np.ndarray, mask: np.ndarray):
        """
        Random flips and 90-degree rotations.
        Applied identically to both image and mask to preserve alignment.
        """
        if self.geometric_flip and np.random.random() > 0.5:
            image = np.flip(image, axis=2).copy()  # Horizontal flip
            mask = np.flip(mask, axis=2).copy()
        
        if self.geometric_flip and np.random.random() > 0.5:
            image = np.flip(image, axis=1).copy()  # Vertical flip
            mask = np.flip(mask, axis=1).copy()
        
        if self.geometric_rotate:
            k = np.random.randint(0, 4)  # 0, 90, 180, or 270 degrees
            image = np.rot90(image, k, axes=(1, 2)).copy()
            mask = np.rot90(mask, k, axes=(1, 2)).copy()
        
        return image, mask
    
    def apply(self, image: np.ndarray, mask: np.ndarray):
        """
        Main entry point. Applies augmentations to the image while
        keeping the ground truth mask UNTOUCHED (critical for topology learning).
        """
        # Cloud injection (image only, mask stays clean)
        if np.random.random() < self.cloud_probability:
            image = self._apply_cloud(image)
        
        # Shadow injection (image only)
        if np.random.random() < self.shadow_probability:
            image = self._apply_shadow(image)
        
        # Geometric transforms (both image and mask, identically)
        image, mask = self._apply_geometric(image, mask)
        
        return image, mask
