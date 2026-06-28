import numpy as np
from scipy.ndimage import label, sum as ndi_sum
from utils.logger import get_logger

logger = get_logger("graph.construction.skeletonize")


class RoadSkeletonizer:
    """
    Converts binary road segmentation masks into clean 1-pixel-wide topological centerlines.
    
    Implements the vectorized Zhang-Suen morphological thinning algorithm along with
    connected component filtering to remove noisy artifacts while strictly preserving
    junction topology and connectivity.
    
    Architecture Traceability:
        - Phase 7.4.1 (Skeletonization)
        - ISRO FR-02: Maintain connectivity under occlusions
        - ISRO HR-01: Topological priority over pixel accuracy
    """
    
    def __init__(self, min_component_size: int = 20, max_iterations: int = 500):
        """
        Args:
            min_component_size: Minimum pixel area for a connected road component.
                                Smaller components are discarded as noise.
            max_iterations: Safety limit for thinning loop iterations.
        """
        self.min_component_size = min_component_size
        self.max_iterations = max_iterations

    def remove_small_artifacts(self, mask: np.ndarray) -> np.ndarray:
        """
        Removes isolated foreground speckles smaller than `min_component_size`.
        
        Args:
            mask: Binary 2D numpy array (0 and 1).
            
        Returns:
            Cleaned binary mask.
        """
        if self.min_component_size <= 0:
            return mask
            
        binary_mask = (mask > 0).astype(np.uint8)
        labeled, num_features = label(binary_mask)
        
        if num_features == 0:
            return binary_mask
            
        component_sizes = ndi_sum(binary_mask, labeled, range(1, num_features + 1))
        component_sizes = np.asarray(component_sizes)
        
        # Identify labels that are smaller than threshold (labels are 1-indexed)
        too_small_labels = np.where(component_sizes < self.min_component_size)[0] + 1
        
        if len(too_small_labels) > 0:
            cleaned = binary_mask.copy()
            cleaned[np.isin(labeled, too_small_labels)] = 0
            logger.debug(f"Removed {len(too_small_labels)} small artifact components (< {self.min_component_size} px).")
            return cleaned
            
        return binary_mask

    def _zhang_suen_iteration(self, img: np.ndarray, sub_iter: int) -> np.ndarray:
        """
        Performs one sub-iteration of vectorized Zhang-Suen thinning.
        """
        # Pad image with zeros to safely extract 3x3 neighborhoods
        pad = np.pad(img, 1, mode="constant", constant_values=0)
        
        p2 = pad[:-2, 1:-1]
        p3 = pad[:-2, 2:]
        p4 = pad[1:-1, 2:]
        p5 = pad[2:, 2:]
        p6 = pad[2:, 1:-1]
        p7 = pad[2:, :-2]
        p8 = pad[1:-1, :-2]
        p9 = pad[:-2, :-2]
        
        # B(P1): Number of non-zero neighbors
        B = p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9
        
        # A(P1): Number of 0 -> 1 transitions in cyclic neighbor sequence
        A = (
            ((p2 == 0) & (p3 == 1)).astype(np.uint8) +
            ((p3 == 0) & (p4 == 1)).astype(np.uint8) +
            ((p4 == 0) & (p5 == 1)).astype(np.uint8) +
            ((p5 == 0) & (p6 == 1)).astype(np.uint8) +
            ((p6 == 0) & (p7 == 1)).astype(np.uint8) +
            ((p7 == 0) & (p8 == 1)).astype(np.uint8) +
            ((p8 == 0) & (p9 == 1)).astype(np.uint8) +
            ((p9 == 0) & (p2 == 1)).astype(np.uint8)
        )
        
        cond1 = (B >= 2) & (B <= 6)
        cond2 = (A == 1)
        
        if sub_iter == 0:
            cond3 = (p2 * p4 * p6 == 0)
            cond4 = (p4 * p6 * p8 == 0)
        else:
            cond3 = (p2 * p4 * p8 == 0)
            cond4 = (p2 * p6 * p8 == 0)
            
        to_remove = (img == 1) & cond1 & cond2 & cond3 & cond4
        return to_remove

    def skeletonize(self, mask: np.ndarray) -> np.ndarray:
        """
        Executes complete end-to-end skeletonization:
        1. Artifact removal (noise cleanup)
        2. Vectorized Zhang-Suen morphological thinning
        3. Post-thinning artifact cleanup
        
        Args:
            mask: Input binary mask (2D array, values >0 treated as road).
            
        Returns:
            1-pixel-wide binary skeleton mask (uint8, values 0 or 1).
        """
        if mask.ndim != 2:
            raise ValueError(f"Expected 2D binary mask, got shape {mask.shape}")
            
        img = self.remove_small_artifacts(mask)
        img = (img > 0).astype(np.uint8)
        
        if np.sum(img) == 0:
            logger.warning("Input mask is empty after artifact removal.")
            return img
            
        iterations = 0
        while iterations < self.max_iterations:
            # Sub-iteration 1
            remove1 = self._zhang_suen_iteration(img, 0)
            img[remove1] = 0
            
            # Sub-iteration 2
            remove2 = self._zhang_suen_iteration(img, 1)
            img[remove2] = 0
            
            if not np.any(remove1) and not np.any(remove2):
                break
                
            iterations += 1
            
        if iterations >= self.max_iterations:
            logger.warning(f"Zhang-Suen thinning reached max iterations ({self.max_iterations}).")
        else:
            logger.debug(f"Skeletonization converged in {iterations} iterations.")
            
        # Final cleanup of any single-pixel spurs or tiny isolated fragments
        skeleton = self.remove_small_artifacts(img)
        return skeleton
