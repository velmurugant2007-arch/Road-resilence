import unittest
import numpy as np
import networkx as nx
from graph.healing.healer import GraphHealer, RepairExplanation


class TestGraphHealer(unittest.TestCase):
    """
    Unit test suite for Phase 7.4.4 (Graph Healing) & Explainability Enhancement.
    Verifies Hybrid Cost scoring, RepairExplanation metadata generation, threshold decisions,
    and topological edge insertion.
    """

    def setUp(self):
        self.healer = GraphHealer(max_search_radius=50.0, decision_threshold=0.65)

    def test_repair_explanation_metadata(self):
        """Test that RepairExplanation serializes all requested explainability fields."""
        exp = RepairExplanation(
            repair_id="RH-001",
            source_node="N154",
            destination_node="N173",
            distance=8.2,
            ai_confidence=0.91,
            direction_score=0.96,
            width_score=0.88,
            density_score=0.84,
            hybrid_score=0.93,
            threshold=0.65,
            accepted=True,
            explanation="Accepted because confidence exceeded threshold."
        )
        data = exp.to_dict()
        
        self.assertEqual(data["repair_id"], "RH-001")
        self.assertEqual(data["source_node"], "N154")
        self.assertEqual(data["destination_node"], "N173")
        self.assertAlmostEqual(data["distance"], 8.2)
        self.assertAlmostEqual(data["ai_confidence"], 0.91)
        self.assertAlmostEqual(data["direction_consistency"], 0.96)
        self.assertAlmostEqual(data["road_width_similarity"], 0.88)
        self.assertAlmostEqual(data["local_road_density"], 0.84)
        self.assertAlmostEqual(data["hybrid_cost_score"], 0.93)
        self.assertEqual(data["decision_threshold"], 0.65)
        self.assertEqual(data["status"], "Accepted")
        self.assertTrue(data["accepted"])
        self.assertIn("Accepted because", data["explanation"])

    def test_evaluate_candidate_accepted_and_rejected(self):
        """Test candidate evaluation scoring and automated explanation generation."""
        G = nx.Graph()
        # Create two collinear road endpoints separated by 10 pixels
        G.add_node("N1", pixel_coord=(10, 10), node_type="endpoint")
        G.add_node("N0", pixel_coord=(10, 0), node_type="path_node")
        G.add_edge("N0", "N1")  # Road pointing right along row 10
        
        G.add_node("N2", pixel_coord=(10, 20), node_type="endpoint")
        G.add_node("N3", pixel_coord=(10, 30), node_type="path_node")
        G.add_edge("N2", "N3")  # Road pointing left along row 10

        exp = self.healer.evaluate_candidate(G, "N1", "N2")
        self.assertTrue(exp.accepted)
        self.assertEqual(exp.status, "Accepted")
        self.assertIn("Accepted because", exp.explanation)
        self.assertGreaterEqual(exp.hybrid_score, 0.65)

        # Test distant candidate that should be rejected or low score
        G.add_node("N99", pixel_coord=(50, 50), node_type="endpoint")
        exp_rej = self.healer.evaluate_candidate(G, "N1", "N99")
        self.assertFalse(exp_rej.accepted)
        self.assertEqual(exp_rej.status, "Rejected")
        self.assertIn("Rejected because", exp_rej.explanation)

    def test_heal_graph_edge_insertion_and_metadata(self):
        """Test end-to-end graph healing and verification of attached repair_metadata on healed edges."""
        G = nx.Graph()
        # Segment 1
        G.add_node("N1", pixel_coord=(20, 20), node_type="endpoint")
        G.add_node("N0", pixel_coord=(20, 10), node_type="path_node")
        G.add_edge("N0", "N1")
        # Segment 2 across 10-px gap
        G.add_node("N2", pixel_coord=(20, 30), node_type="endpoint")
        G.add_node("N3", pixel_coord=(20, 40), node_type="path_node")
        G.add_edge("N2", "N3")

        healed_G, history = self.healer.heal_graph(G)
        
        self.assertTrue(healed_G.has_edge("N1", "N2"))
        edge_data = healed_G.edges["N1", "N2"]
        self.assertEqual(edge_data["edge_type"], "healed")
        self.assertIn("repair_metadata", edge_data)
        
        meta = edge_data["repair_metadata"]
        self.assertEqual(meta["source_node"], "N1")
        self.assertEqual(meta["destination_node"], "N2")
        self.assertEqual(meta["status"], "Accepted")


if __name__ == "__main__":
    unittest.main()
