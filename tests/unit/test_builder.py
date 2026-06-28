import unittest
import tempfile
import shutil
from pathlib import Path
import numpy as np
import networkx as nx
from graph.construction.builder import RoadGraphBuilder


class TestRoadGraphBuilder(unittest.TestCase):
    """
    Unit test suite for Phase 7.4.3 (Graph Construction).
    Verifies node/edge generation, geo-transform mapping, statistics computation,
    duplicate edge handling, topology validation, GeoJSON export, and visualization.
    """

    def setUp(self):
        # Sample affine transform: col * 10, row * 10
        self.transform = (100.0, 10.0, 0.0, 200.0, 0.0, 10.0)
        self.builder = RoadGraphBuilder(geo_transform=self.transform)
        self.temp_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_build_graph_nodes_and_edges(self):
        """Test construction of NetworkX graph with node types and edge attributes."""
        polylines = [
            [(10, 10), (10, 20), (10, 30)],  # Horizontal branch
            [(10, 30), (20, 30), (30, 30)],  # Vertical branch down
            [(10, 30), (0, 30)]              # Vertical branch up
        ]
        
        G = self.builder.build_graph(polylines)
        
        self.assertEqual(G.number_of_nodes(), 4)
        self.assertEqual(G.number_of_edges(), 3)
        
        # Check node types
        # The node at (10, 30) connects all 3 branches -> degree 3 -> junction
        junc_node = [n for n, d in G.nodes(data=True) if d["pixel_coord"] == (10, 30)][0]
        self.assertEqual(G.nodes[junc_node]["node_type"], "junction")
        
        # Check geo coordinates transformation for (10, 10)
        # x = 100 + 10*10 = 200, y = 200 + 10*10 = 300
        ep_node = [n for n, d in G.nodes(data=True) if d["pixel_coord"] == (10, 10)][0]
        self.assertEqual(G.nodes[ep_node]["geo_coord"], (200.0, 300.0))

    def test_duplicate_edge_handling(self):
        """Test that duplicate paths between the same nodes are merged keeping the shortest path."""
        polylines = [
            [(0, 0), (0, 5), (0, 10)],       # Length 10
            [(0, 0), (5, 5), (0, 10)]        # Length ~14.14
        ]
        G = self.builder.build_graph(polylines)
        
        self.assertEqual(G.number_of_edges(), 1)
        u = [n for n, d in G.nodes(data=True) if d["pixel_coord"] == (0, 0)][0]
        v = [n for n, d in G.nodes(data=True) if d["pixel_coord"] == (0, 10)][0]
        
        self.assertAlmostEqual(G.edges[u, v]["length"], 10.0)

    def test_compute_statistics(self):
        """Test structural metrics reporting."""
        polylines = [
            [(0, 0), (0, 10)],
            [(0, 10), (10, 10)],
            [(50, 50), (60, 60)]  # Disjoint second component
        ]
        G = self.builder.build_graph(polylines)
        stats = self.builder.compute_statistics(G)
        
        self.assertEqual(stats["num_nodes"], 5)
        self.assertEqual(stats["num_edges"], 3)
        self.assertEqual(stats["connected_components"], 2)
        self.assertEqual(stats["largest_connected_component_nodes"], 3)
        self.assertEqual(stats["largest_connected_component_percent"], 60.0)

    def test_validate_topology(self):
        """Test topology validation rules."""
        polylines = [[(0, 0), (1, 1)]]
        G = self.builder.build_graph(polylines)
        report = self.builder.validate_topology(G, polylines)
        self.assertTrue(report["is_valid"])
        self.assertTrue(report["no_duplicate_edges"])

    def test_export_geojson_and_visualization(self):
        """Test GeoJSON generation and matplotlib graph overlay export."""
        polylines = [[(5, 5), (5, 15), (15, 15)]]
        G = self.builder.build_graph(polylines)
        
        geojson_file = self.temp_dir / "test_graph.geojson"
        geojson = self.builder.export_geojson(G, filepath=geojson_file)
        
        self.assertEqual(geojson["type"], "FeatureCollection")
        self.assertTrue(geojson_file.exists())
        
        vis_file = self.temp_dir / "test_graph_vis.png"
        bg_mask = np.zeros((30, 30), dtype=np.uint8)
        bg_mask[5, 5:16] = 1
        bg_mask[5:16, 15] = 1
        self.builder.generate_visualization(G, bg_mask, vis_file)
        self.assertTrue(vis_file.exists())


if __name__ == "__main__":
    unittest.main()
