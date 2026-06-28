import unittest
import numpy as np
from pathlib import Path
import tempfile
import shutil
from graph.construction.vectorize import RoadVectorizer
from graph.construction.skeletonize import RoadSkeletonizer


class TestRoadVectorizer(unittest.TestCase):
    """
    Unit test and benchmark suite for Phase 7.4.2 (Vectorization).
    Verifies chain tracing, junction/endpoint detection, spur pruning,
    RDP simplification, connectivity preservation, and performance across scales.
    """

    def setUp(self):
        self.vectorizer = RoadVectorizer(min_spur_length=5, rdp_epsilon=2.0)
        self.skeletonizer = RoadSkeletonizer()
        self.temp_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_node_detection(self):
        """Test detection of junctions (deg >= 3) and endpoints (deg == 1)."""
        skel = np.zeros((30, 30), dtype=np.uint8)
        # Horizontal line row 15, cols 5 to 25
        skel[15, 5:26] = 1
        # Vertical branch downwards from row 15, col 15 to row 25
        skel[16:26, 15] = 1
        
        endpoints, junctions = self.vectorizer.detect_nodes(skel)
        
        # There should be 3 endpoints: (15, 5), (15, 25), (25, 15)
        self.assertEqual(np.sum(endpoints), 3)
        # There should be at least 1 junction at or around (15, 15)
        self.assertGreaterEqual(np.sum(junctions), 1)

    def test_spur_pruning(self):
        """Test that short dead-end spurs (< min_spur_length) are pruned."""
        skel = np.zeros((50, 50), dtype=np.uint8)
        # Main road line from left to right
        skel[25, 10:40] = 1
        # Short 3-pixel spur attached to row 25, col 20 pointing upwards
        skel[22:25, 20] = 1
        
        pruned = self.vectorizer.prune_spurs(skel)
        
        # The top endpoint of the spur (22, 20) should be removed
        self.assertEqual(pruned[22, 20], 0)
        # The main road left and right endpoints should remain
        self.assertEqual(pruned[25, 10], 1)
        self.assertEqual(pruned[25, 39], 1)

    def test_rdp_simplification(self):
        """Test Ramer-Douglas-Peucker simplification on a straight line with intermediate points."""
        points = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (10, 10)]
        simplified = self.vectorizer.ramer_douglas_peucker(points, epsilon=1.0)
        
        # A perfectly collinear sequence should be simplified to just start and end point
        self.assertEqual(len(simplified), 2)
        self.assertEqual(simplified[0], (0, 0))
        self.assertEqual(simplified[1], (10, 10))

    def test_vectorize_metrics_and_connectivity(self):
        """Test end-to-end vectorize pipeline metrics and connectivity verification."""
        mask = np.zeros((100, 100), dtype=np.uint8)
        # T-junction road mask
        mask[45:55, 10:90] = 1
        mask[55:90, 45:55] = 1
        
        skel = self.skeletonizer.skeletonize(mask)
        res = self.vectorizer.vectorize(skel)
        
        metrics = res["metrics"]
        self.assertEqual(metrics["connected_components"], 1)
        self.assertGreaterEqual(metrics["endpoint_count"], 3)
        self.assertGreaterEqual(metrics["polyline_count"], 1)
        self.assertTrue(metrics["connectivity_preserved"], "Connectivity broke after vectorization!")

    def test_visualization_generation(self):
        """Test output generation for Original Mask, Skeleton, and Vector Overlay."""
        mask = np.zeros((60, 60), dtype=np.uint8)
        mask[28:32, 10:50] = 1
        skel = self.skeletonizer.skeletonize(mask)
        res = self.vectorizer.vectorize(skel)
        
        out_file = self.temp_dir / "test_overlay.png"
        self.vectorizer.generate_visualizations(mask, skel, res["polylines"], out_file)
        self.assertTrue(out_file.exists())
        self.assertGreater(out_file.stat().st_size, 0)

    def test_benchmark_performance(self):
        """Benchmark vectorization performance across multiple image sizes."""
        sizes = [256, 512, 1024]
        for size in sizes:
            mask = np.zeros((size, size), dtype=np.uint8)
            # Create a grid of crossing roads
            for i in range(50, size, 100):
                mask[i-3:i+3, :] = 1
                mask[:, i-3:i+3] = 1
            
            skel = self.skeletonizer.skeletonize(mask)
            res = self.vectorizer.vectorize(skel)
            
            exec_time = res["metrics"]["execution_time_ms"]
            print(f"Benchmark {size}x{size}: {exec_time:.2f}ms | Polylines: {res['metrics']['polyline_count']}")
            # Ensure execution completes in under 2000ms even for 1024x1024 grid
            self.assertLess(exec_time, 2000.0)


if __name__ == "__main__":
    unittest.main()
