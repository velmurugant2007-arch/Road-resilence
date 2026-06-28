import unittest
import time
import tempfile
import shutil
from pathlib import Path
import networkx as nx
import numpy as np
from graph.resilience.simulator import StressSimulator


class TestStressSimulator(unittest.TestCase):
    """
    Unit test suite for Phase 7.4.6 (Urban Mobility Stress Simulation).
    Verifies single, multi, regional, random, and custom failure modes,
    post-simulation connectivity metrics, repair priorities, and diagnostic exports.
    """

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())

        # Construct synthetic grid network (4x4 = 16 nodes)
        self.G = nx.Graph()
        for r in range(4):
            for c in range(4):
                node_id = (r, c)
                self.G.add_node(node_id, pixel_coord=(r * 10, c * 10), node_type="junction")
        
        for r in range(4):
            for c in range(4):
                if r < 3:
                    self.G.add_edge((r, c), (r + 1, c), length=10.0, geometry=[(r*10, c*10), ((r+1)*10, c*10)])
                if c < 3:
                    self.G.add_edge((r, c), (r, c + 1), length=10.0, geometry=[(r*10, c*10), (r*10, (c+1)*10)])

        self.simulator = StressSimulator(self.G)

    def tearDown(self):
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_single_node_failure(self):
        """Test removal of a single central hub node and metrics update."""
        res = self.simulator.simulate_single_node_failure((1, 1))
        metrics = res["simulation_metrics"]
        
        self.assertEqual(metrics["removed_nodes_count"], 1)
        self.assertEqual(res["damaged_graph"].number_of_nodes(), 15)
        self.assertLessEqual(metrics["composite_resilience_score"], 1.0)

    def test_multi_node_failure(self):
        """Test simultaneous removal of multiple bottleneck nodes."""
        res = self.simulator.simulate_multi_node_failure([(1, 1), (2, 2)])
        metrics = res["simulation_metrics"]
        
        self.assertEqual(metrics["removed_nodes_count"], 2)
        self.assertEqual(res["damaged_graph"].number_of_nodes(), 14)

    def test_regional_failure(self):
        """Test radial simulated flood wipeout centered at specific coordinates."""
        # Circle at (0, 0) with radius 12 meters should capture (0,0), (0,1), and (1,0)
        res = self.simulator.simulate_regional_failure((0.0, 0.0), 12.0)
        metrics = res["simulation_metrics"]
        
        self.assertEqual(metrics["removed_nodes_count"], 3)
        self.assertNotIn((0, 0), res["damaged_graph"])

    def test_random_failure(self):
        """Test stochastic failure mode with reproducible seed."""
        res = self.simulator.simulate_random_failure(failure_fraction=0.25, seed=42)
        metrics = res["simulation_metrics"]
        
        self.assertEqual(metrics["removed_nodes_count"], 4)  # 25% of 16 is 4

    def test_custom_failure_and_decision_support(self):
        """Test custom failure mode and ranked repair priority recommendations."""
        res = self.simulator.simulate_custom_failure([(1, 1)], [((0, 0), (0, 1))])
        ds = res["decision_support"]
        
        self.assertIn("recommended_repair_priority", ds)
        repair_list = ds["recommended_repair_priority"]
        self.assertGreaterEqual(len(repair_list), 1)
        # Check Delta R structure
        first_repair = repair_list[0]
        self.assertIn("estimated_resilience_improvement", first_repair)
        self.assertIn("priority_rank", first_repair)
        self.assertEqual(first_repair["priority_rank"], 1)

    def test_visualization_generation(self):
        """Test export of all 4 diagnostic PNG visualization reports."""
        res = self.simulator.simulate_single_node_failure((1, 1))
        bg_mask = np.zeros((40, 40), dtype=np.uint8)
        paths = self.simulator.generate_simulation_visualizations(res, bg_mask, self.temp_dir)
        
        self.assertIn("before_after", paths)
        self.assertIn("affected_heatmap", paths)
        self.assertIn("connectivity_chart", paths)
        self.assertIn("impact_summary", paths)
        for p in paths.values():
            self.assertTrue(Path(p).exists())

    def test_performance_benchmark(self):
        """Benchmark stress simulation execution timing on larger grid network."""
        grid_G = nx.grid_2d_graph(10, 10)  # 100 nodes
        test_G = nx.Graph()
        for r, c in grid_G.nodes():
            test_G.add_node((r, c), pixel_coord=(r * 10, c * 10))
        for u, v in grid_G.edges():
            test_G.add_edge(u, v, length=10.0)

        sim = StressSimulator(test_G)
        start_t = time.perf_counter()
        sim.simulate_random_failure(0.15, seed=1)
        duration = time.perf_counter() - start_t
        
        print(f"\n[Benchmark] Simulated 15% random failure on 100-node graph in {duration:.4f} seconds.")
        self.assertLess(duration, 2.0)


if __name__ == "__main__":
    unittest.main()
