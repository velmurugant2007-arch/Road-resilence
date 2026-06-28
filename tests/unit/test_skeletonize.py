import unittest
import numpy as np
from scipy.ndimage import label
from graph.construction.skeletonize import RoadSkeletonizer


class TestRoadSkeletonizer(unittest.TestCase):
    """
    Unit test suite for Phase 7.4.1 (Skeletonization).
    Verifies artifact removal, Zhang-Suen thinning, and junction connectivity preservation.
    """

    def setUp(self):
        self.skeletonizer = RoadSkeletonizer(min_component_size=20, max_iterations=200)

    def test_artifact_removal(self):
        """Test that small isolated noise components (< min_component_size) are removed."""
        mask = np.zeros((100, 100), dtype=np.uint8)
        
        # Large road block (area 400 px) -> should remain
        mask[20:40, 20:40] = 1
        
        # Small noise speckle (area 4 px) -> should be removed
        mask[80:82, 80:82] = 1
        
        cleaned = self.skeletonizer.remove_small_artifacts(mask)
        
        # Large block should still be 1
        self.assertEqual(np.sum(cleaned[20:40, 20:40]), 400)
        # Small speckle should be 0
        self.assertEqual(np.sum(cleaned[80:82, 80:82]), 0)

    def test_skeletonize_straight_road(self):
        """Test that a thick road bar is thinned to a 1-pixel wide centerline."""
        mask = np.zeros((100, 100), dtype=np.uint8)
        # Horizontal road bar from col 10 to 90, row 40 to 50 (thickness 10)
        mask[40:50, 10:90] = 1
        
        skel = self.skeletonizer.skeletonize(mask)
        
        # Check that skeleton is non-empty
        self.assertGreater(np.sum(skel), 0)
        
        # Check that thickness along a vertical slice (e.g. col 50) is at most 2 pixels (ideally 1)
        col_50_thickness = np.sum(skel[:, 50])
        self.assertLessEqual(col_50_thickness, 2)
        self.assertGreaterEqual(col_50_thickness, 1)
        
        # Check connectivity: should remain 1 single connected component
        labeled, num_features = label(skel)
        self.assertEqual(num_features, 1, "Skeleton of a single road bar must remain 1 connected component.")

    def test_preserve_junction_topology(self):
        """Test that a T-junction or cross (+) intersection preserves connectivity after thinning."""
        mask = np.zeros((100, 100), dtype=np.uint8)
        
        # Horizontal bar (thickness 12)
        mask[44:56, 10:90] = 1
        # Vertical bar crossing it (thickness 12)
        mask[10:90, 44:56] = 1
        
        # Verify initial mask is 1 connected component
        _, init_features = label(mask)
        self.assertEqual(init_features, 1)
        
        skel = self.skeletonizer.skeletonize(mask)
        
        # Verify skeletonized cross is still 1 connected component (junction preserved!)
        _, skel_features = label(skel)
        self.assertEqual(skel_features, 1, "Junction topology broken during skeletonization!")
        
        # Verify Significant thinning occurred (pixel count should drop significantly)
        initial_area = np.sum(mask)
        skel_area = np.sum(skel)
        self.assertLess(skel_area, initial_area * 0.25, "Thinning did not reduce area sufficiently.")

    def test_empty_mask(self):
        """Test graceful handling of empty masks."""
        mask = np.zeros((50, 50), dtype=np.uint8)
        skel = self.skeletonizer.skeletonize(mask)
        self.assertEqual(np.sum(skel), 0)


if __name__ == "__main__":
    unittest.main()
