import numpy as np
from scipy.ndimage import zoom, gaussian_filter
from utils.logger import get_logger

logger = get_logger("ai.augmentation")


class SyntheticOcclusionAugmentor:
    """
    Multi-type synthetic occlusion generator for satellite road extraction training.
    
    Supports probabilistic composition of multiple occlusion types per sample,
    simulating realistic urban satellite imagery degradation.
    
    Engineering Justification (dataset_strategy.md, Section 3):
        Real paired data (occluded image + clean road mask) does not exist.
        We overlay synthetic occlusions on clear imagery while keeping the
        ground truth mask INTACT, forcing the model to learn continuity
        from global context.
    
    ISRO Alignment:
        FR-02: Maintain connectivity under occlusions.
        HR-01: Topological priority — model must learn continuity, not pixels.
    """
    
    def __init__(
        self,
        cloud_prob: float = 0.4,
        shadow_prob: float = 0.3,
        tree_canopy_prob: float = 0.25,
        building_shadow_prob: float = 0.2,
        vehicle_prob: float = 0.15,
        urban_clutter_prob: float = 0.15,
        haze_prob: float = 0.2,
        seasonal_prob: float = 0.2,
        max_cloud_coverage: float = 0.4,
        geometric_flip: bool = True,
        geometric_rotate: bool = True,
    ):
        self.occlusion_config = {
            "cloud": cloud_prob,
            "shadow": shadow_prob,
            "tree_canopy": tree_canopy_prob,
            "building_shadow": building_shadow_prob,
            "vehicle": vehicle_prob,
            "urban_clutter": urban_clutter_prob,
            "haze": haze_prob,
            "seasonal": seasonal_prob,
        }
        self.max_cloud_coverage = max_cloud_coverage
        self.geometric_flip = geometric_flip
        self.geometric_rotate = geometric_rotate

    # ── Noise Generators ──────────────────────────────────────────────

    def _smooth_noise(self, h: int, w: int, scales: list = None) -> np.ndarray:
        """Multi-octave smooth noise in [0, 1]."""
        if scales is None:
            scales = [4, 8, 16, 32]
        result = np.zeros((h, w), dtype=np.float32)
        for s in scales:
            noise = np.random.randn(h // s + 1, w // s + 1).astype(np.float32)
            up = zoom(noise, (h / (h // s + 1), w / (w // s + 1)), order=1)[:h, :w]
            result += up
        mn, mx = result.min(), result.max()
        return (result - mn) / (mx - mn + 1e-8)

    def _random_rectangles(self, h: int, w: int, count: int, size_range: tuple) -> np.ndarray:
        """Generate a mask of random rectangles (buildings, vehicles, etc.)."""
        mask = np.zeros((h, w), dtype=np.float32)
        for _ in range(count):
            rh = np.random.randint(*size_range)
            rw = np.random.randint(*size_range)
            ry = np.random.randint(0, max(1, h - rh))
            rx = np.random.randint(0, max(1, w - rw))
            mask[ry:ry + rh, rx:rx + rw] = np.random.uniform(0.5, 1.0)
        return mask

    # ── Occlusion Types ───────────────────────────────────────────────

    def _apply_cloud(self, image: np.ndarray) -> np.ndarray:
        """White cloud overlay with natural edges."""
        _, h, w = image.shape
        cloud = self._smooth_noise(h, w)
        threshold = 1.0 - self.max_cloud_coverage
        cloud = np.where(cloud > threshold, cloud, 0.0)
        for c in range(image.shape[0]):
            image[c] = (image[c] * (1 - cloud) + 255 * cloud).astype(image.dtype)
        return image

    def _apply_shadow(self, image: np.ndarray) -> np.ndarray:
        """Cloud shadow shifted by simulated sun angle."""
        _, h, w = image.shape
        shadow = self._smooth_noise(h, w)
        threshold = 1.0 - self.max_cloud_coverage
        shadow = np.where(shadow > threshold, shadow, 0.0)
        sx, sy = np.random.randint(10, 30), np.random.randint(10, 30)
        shadow = np.roll(np.roll(shadow, sx, axis=1), sy, axis=0)
        darkening = np.random.uniform(0.4, 0.7)
        for c in range(image.shape[0]):
            image[c] = (image[c] * (1 - darkening * shadow)).astype(image.dtype)
        return image

    def _apply_tree_canopy(self, image: np.ndarray) -> np.ndarray:
        """Irregular green-tinted blobs simulating dense tree cover over roads."""
        _, h, w = image.shape
        canopy = self._smooth_noise(h, w, scales=[8, 16, 32])
        canopy = np.where(canopy > 0.65, canopy, 0.0)
        canopy = gaussian_filter(canopy, sigma=3)
        # Green-tinted overlay
        green_tint = np.array([30, 80, 20], dtype=np.float32).reshape(3, 1, 1)
        for c in range(min(3, image.shape[0])):
            image[c] = (image[c] * (1 - 0.6 * canopy) + green_tint[c] * canopy).astype(image.dtype)
        return image

    def _apply_building_shadow(self, image: np.ndarray) -> np.ndarray:
        """Sharp-edged rectangular shadows from tall buildings."""
        _, h, w = image.shape
        shadow = self._random_rectangles(h, w, count=np.random.randint(3, 8), size_range=(20, 80))
        # Shift to simulate projection
        sx = np.random.randint(5, 20)
        shadow = np.roll(shadow, sx, axis=1)
        shadow = gaussian_filter(shadow, sigma=1)
        for c in range(image.shape[0]):
            image[c] = (image[c] * (1 - 0.5 * shadow)).astype(image.dtype)
        return image

    def _apply_vehicle(self, image: np.ndarray) -> np.ndarray:
        """Small bright rectangles simulating vehicles parked on roads."""
        _, h, w = image.shape
        vehicles = self._random_rectangles(h, w, count=np.random.randint(5, 20), size_range=(3, 10))
        colors = np.random.randint(100, 250, size=(3,), dtype=np.uint8)
        for c in range(min(3, image.shape[0])):
            image[c] = np.where(vehicles > 0.5, colors[c], image[c]).astype(image.dtype)
        return image

    def _apply_urban_clutter(self, image: np.ndarray) -> np.ndarray:
        """Mixed noise: construction zones, market stalls, rubble."""
        _, h, w = image.shape
        clutter = self._random_rectangles(h, w, count=np.random.randint(5, 15), size_range=(10, 40))
        noise_texture = np.random.randint(50, 180, (h, w), dtype=np.uint8).astype(np.float32)
        for c in range(image.shape[0]):
            image[c] = np.where(clutter > 0.3, noise_texture * 0.7 + image[c] * 0.3, image[c]).astype(image.dtype)
        return image

    def _apply_haze(self, image: np.ndarray) -> np.ndarray:
        """Uniform atmospheric haze reducing contrast."""
        _, h, w = image.shape
        intensity = np.random.uniform(0.15, 0.4)
        haze_color = np.random.randint(180, 230)
        for c in range(image.shape[0]):
            image[c] = (image[c] * (1 - intensity) + haze_color * intensity).astype(image.dtype)
        return image

    def _apply_seasonal(self, image: np.ndarray) -> np.ndarray:
        """Seasonal illumination shift (warm summer / cool winter tones)."""
        season = np.random.choice(["summer", "winter", "monsoon"])
        shifts = {
            "summer": np.array([1.1, 1.05, 0.9]),
            "winter": np.array([0.9, 0.95, 1.1]),
            "monsoon": np.array([0.85, 0.9, 0.95]),
        }
        scale = shifts[season]
        for c in range(min(3, image.shape[0])):
            image[c] = np.clip(image[c] * scale[c], 0, 255).astype(image.dtype)
        return image

    # ── Geometric Transforms ──────────────────────────────────────────

    def _apply_geometric(self, image: np.ndarray, mask: np.ndarray):
        """Random flips and 90° rotations applied identically to image and mask."""
        if self.geometric_flip and np.random.random() > 0.5:
            image = np.flip(image, axis=2).copy()
            mask = np.flip(mask, axis=2).copy()
        if self.geometric_flip and np.random.random() > 0.5:
            image = np.flip(image, axis=1).copy()
            mask = np.flip(mask, axis=1).copy()
        if self.geometric_rotate:
            k = np.random.randint(0, 4)
            image = np.rot90(image, k, axes=(1, 2)).copy()
            mask = np.rot90(mask, k, axes=(1, 2)).copy()
        return image, mask

    # ── Main Entry Point ──────────────────────────────────────────────

    def apply(self, image: np.ndarray, mask: np.ndarray):
        """
        Probabilistically composes multiple occlusion types per sample.
        Each type is independently rolled against its probability.
        The mask is NEVER modified by occlusions (only by geometric transforms).
        """
        dispatch = {
            "cloud": self._apply_cloud,
            "shadow": self._apply_shadow,
            "tree_canopy": self._apply_tree_canopy,
            "building_shadow": self._apply_building_shadow,
            "vehicle": self._apply_vehicle,
            "urban_clutter": self._apply_urban_clutter,
            "haze": self._apply_haze,
            "seasonal": self._apply_seasonal,
        }

        applied = []
        for name, prob in self.occlusion_config.items():
            if np.random.random() < prob:
                image = dispatch[name](image)
                applied.append(name)

        # Geometric transforms affect both image AND mask identically
        image, mask = self._apply_geometric(image, mask)

        if applied:
            logger.debug(f"Augmentations applied: {', '.join(applied)}")

        return image, mask
