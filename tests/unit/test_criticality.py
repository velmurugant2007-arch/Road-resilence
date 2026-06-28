import unittest
import time
import tempfile
import shutil
from pathlib import Path
import networkx as nx
import numpy as np
from graph.analysis.criticality import CriticalityAnalyzer


class TestCriticalityAnalyzer(unittest.TestCase):
    """
    Unit test suite for Phase 7.4.5 (Graph-Theoretic Criticality Analysis).
    Verifies centrality computations, bridge/articulation detection, composite scoring,
    urban vulnerability reporting, network resilience index, and visualization exports.
    """

    def setUp(self):
        self.analyzer = CriticalityAnalyzer()
        self.temp_dir = Path(tempfile.mkdtemp())

        # Construct a synthetic bridge graph: Triangle A (0,1,2) connected by bridge (2,3) to Triangle B (3,4,5)
        self.G = nx.Graph()
        for i in range(6):
            self.G.add_node(i, pixel_coord=(i * 10, i * 10), node_type="junction" if i in (2, 3) else "endpoint")
        
        edges = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 5), (5, 3)]
        for u, v in edges:
            r1, c1 = self.G.nodes[u]["pixel_coord"]
            r2, c2 = self.G.nodes[v]["pixel_coord"]
            dist = float(np.hypot(r2 - r1, c2 - c1))
            self.G.add_edge(u, v, length=dist, geometry=[(r1, c1), (r2, c2)])

    def tearDown(self):
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_articulation_points_and_bridges(self):
        """Test exact identification of cut vertices (articulation points) and cut edges (bridges)."""
        self.analyzer.analyze(self.G)
        
        # Nodes 2 and 3 are the only articulation points connecting the two triangles
        self.assertEqual(self.analyzer.articulation_points, {2, 3})
        # Edge (2, 3) is the only bridge
        self.assertEqual(self.analyzer.bridges, {(2, 3)})

    def test_composite_criticality_ranking(self):
        """Test configurable weighting and ranking sorting order of nodes and edges."""
        self.analyzer.analyze(self.G)
        
        node_ranks = self.analyzer.get_critical_node_ranking(top_n=6)
        self.assertEqual(len(node_ranks), 6)
        # Nodes 2 and 3 should have the highest composite criticality due to articulation and high betweenness
        top_2_ids = {node_ranks[0]["node_id"], node_ranks[1]["node_id"]}
        self.assertEqual(top_2_ids, {2, 3})

        edge_ranks = self.analyzer.get_critical_edge_ranking(top_n=7)
        self.assertEqual(len(edge_ranks), 7)
        # Bridge edge (2, 3) should rank #1 in edge composite criticality
        top_edge = (min(edge_ranks[0]["source"], edge_ranks[0]["target"]), max(edge_ranks[0]["source"], edge_ranks[0]["target"]))
        self.assertEqual(top_edge, (2, 3))

    def test_urban_vulnerability_report(self):
        """Test generation of vulnerability summary metrics and risk level classification."""
        self.analyzer.analyze(self.G)
        report = self.analyzer.generate_urban_vulnerability_report()
        
        self.assertEqual(report["total_nodes"], 6)
        self.assertEqual(report["total_edges"], 7)
        self.assertEqual(report["connected_components"], 1)
        self.assertEqual(report["articulation_points_count"], 2)
        self.assertEqual(report["bridges_count"], 1)
        self.assertIn("urban_vulnerability_risk_level", report)

    def test_network_resilience_score(self):
        """Test scalar resilience score computation bounded in [0.0, 1.0]."""
        self.analyzer.analyze(self.G)
        score = self.analyzer.compute_network_resilience_score()
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)

    def test_visualization_generation(self):
        """Test rendering of the 3 diagnostic criticality plots."""
        self.analyzer.analyze(self.G)
        bg_mask = np.zeros((60, 60), dtype=np.uint8)
        paths = self.analyzer.generate_criticality_visualizations(bg_mask, self.temp_dir)
        
        self.assertIn("centrality_heatmap", paths)
        self.assertIn("critical_node_overlay", paths)
        self.assertIn("critical_edge_overlay", paths)
        for p in paths.values():
            self.assertTrue(Path(p).exists())

    def test_performance_benchmark(self):
        """Benchmark criticality analysis timing on synthetic grid graph."""
        grid_G = nx.grid_2d_graph(10, 10)  # 100 nodes, 180 edges
        # Convert node coords and edges to required structure
        test_G = nx.Graph()
        for r, c in grid_G.nodes():
            test_G.add_node((r, c), pixel_coord=(r * 10, c * 10), node_type="junction")
        for u, v in grid_G.edges():
            r1, c1 = u
            r2, c2 = v
            test_G.add_edge(u, v, length=10.0, geometry=[(r1 * 10, c1 * 10), (r2 * 10, c2 * 10)])

        start_t = time.perf_counter()
        self.analyzer.analyze(test_G)
        duration = time.perf_counter() - start_t
        
        print(f"\n[Benchmark] Analyzed 10x10 Grid Graph (100 nodes, 180 edges) in {duration:.4f} seconds.")
        self.assertLess(duration, 2.0)  # Should complete well under 2 seconds


if __name__ == "__main__":
    unittest.main()
