import time
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import networkx as nx
from utils.logger import get_logger
from backend.models.schemas import SystemConfig
from backend.core.exceptions import GraphNotInitializedError, BoundingBoxTooLargeError

# Import GIS & Graph modules
from graph.construction.builder import RoadGraphBuilder
from graph.healing.healer import GraphHealer
from graph.analysis.criticality import CriticalityAnalyzer
from graph.resilience.simulator import StressSimulator

logger = get_logger("backend.services.manager")


class BackendServiceManager:
    """
    Singleton service orchestration manager integrating GIS, AI, and Graph modules.
    Maintains precomputed Hero City baseline graph state in memory for <50ms endpoint response times.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BackendServiceManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if getattr(self, "initialized", False):
            return
        logger.info("Initializing BackendServiceManager and building Hero City baseline graph...")
        self.config = SystemConfig()
        self.base_G: Optional[nx.Graph] = None
        self.healed_G: Optional[nx.Graph] = None
        self.geojson_cache: Optional[Dict[str, Any]] = None
        self.criticality_report: Dict[str, Any] = {}
        self.modules_status = {
            "gis": True,
            "ai": True,
            "graph_construction": True,
            "graph_healing": True,
            "criticality_analysis": True,
            "stress_simulation": True
        }
        self._initialize_hero_city_baseline()
        self.initialized = True

    def _initialize_hero_city_baseline(self):
        """Constructs and precomputes the Hero City (Bengaluru) synthetic grid road network."""
        try:
            builder = RoadGraphBuilder()
            G = nx.Graph()
            # Build 8x8 synthetic urban grid representing Bengaluru Hero City bounded section
            grid = nx.grid_2d_graph(8, 8)
            for r, c in grid.nodes():
                lat = 12.90 + (r * 0.007)
                lon = 77.50 + (c * 0.007)
                G.add_node(f"N_{r}_{c}", pixel_coord=(r*20, c*20), geo_coord=(lat, lon), geographic_coord=(lat, lon), node_type="junction")

            for u, v in grid.edges():
                r1, c1 = u
                r2, c2 = v
                lat1, lon1 = 12.90 + (r1 * 0.007), 77.50 + (c1 * 0.007)
                lat2, lon2 = 12.90 + (r2 * 0.007), 77.50 + (c2 * 0.007)
                dist_m = float(np.hypot(lat2 - lat1, lon2 - lon1) * 111000.0)
                G.add_edge(
                    f"N_{r1}_{c1}", f"N_{r2}_{c2}",
                    length=round(dist_m, 2),
                    geometry=[(lat1, lon1), (lat2, lon2)],
                    ai_confidence=0.92
                )

            self.base_G = G
            
            # Run criticality offline
            analyzer = CriticalityAnalyzer(node_weights=self.config.criticality_weights)
            self.base_G = analyzer.analyze(self.base_G)
            self.criticality_report = analyzer.generate_urban_vulnerability_report()
            
            # Cache baseline GeoJSON
            self.geojson_cache = builder.export_geojson(self.base_G)
            logger.info("Hero City baseline graph successfully initialized and cached.")
        except Exception as e:
            logger.exception(f"Failed to initialize Hero City baseline: {e}")
            self.modules_status["graph_construction"] = False

    def get_health_status(self) -> Dict[str, Any]:
        return {
            "status": "healthy" if all(self.modules_status.values()) else "degraded",
            "version": "1.0.0",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "modules_initialized": self.modules_status
        }

    def get_config(self) -> SystemConfig:
        return self.config

    def update_config(self, new_config: SystemConfig) -> SystemConfig:
        self.config = new_config
        logger.info(f"Updated system configuration: threshold={new_config.ai_confidence_threshold}")
        return self.config

    def run_ai_inference(self, image_id: str, occlusion_type: str, confidence_threshold: float) -> Dict[str, Any]:
        """Simulates rapid AI SegFormer inference pipeline response."""
        start_t = time.perf_counter()
        time.sleep(0.01)  # Simulate fast model wrapper call
        duration_ms = round((time.perf_counter() - start_t) * 1000.0, 2)
        
        # Simulated metrics based on occlusion severity
        coverage = 18.5 if occlusion_type == "cloud" else (25.0 if occlusion_type == "shadow" else 10.0)
        cldice = round(0.88 - (coverage / 200.0), 4)
        iou = round(0.84 - (coverage / 250.0), 4)

        return {
            "status": "success",
            "image_id": image_id,
            "inference_time_ms": duration_ms,
            "cldice_score": cldice,
            "iou_score": iou,
            "occlusion_coverage_pct": coverage,
            "message": f"Successfully completed AI inference on {image_id} with {occlusion_type} occlusion."
        }

    def construct_graph(self, simplify_epsilon: float, prune_threshold: float) -> Dict[str, Any]:
        """Invokes RoadGraphBuilder on current mask state."""
        if self.base_G is None:
            raise GraphNotInitializedError()
        
        builder = RoadGraphBuilder()
        stats = builder.compute_statistics(self.base_G)
        self.geojson_cache = builder.export_geojson(self.base_G)
        
        return {
            "status": "success",
            "node_count": stats["num_nodes"],
            "edge_count": stats["num_edges"],
            "connected_components": stats["connected_components"],
            "average_degree": stats["avg_node_degree"],
            "geojson": self.geojson_cache
        }

    def heal_graph(self, max_search_radius: float, decision_threshold: float, min_ai_confidence: float) -> Dict[str, Any]:
        """Invokes GraphHealer with Hybrid Cost Function."""
        if self.base_G is None:
            raise GraphNotInitializedError()

        # Create fragmented test copy by removing a few edges to demonstrate healing
        frag_G = self.base_G.copy()
        if frag_G.has_edge("N_2_2", "N_2_3"): frag_G.remove_edge("N_2_2", "N_2_3")
        if frag_G.has_edge("N_4_4", "N_4_5"): frag_G.remove_edge("N_4_4", "N_4_5")

        healer = GraphHealer(
            max_search_radius=max_search_radius,
            decision_threshold=decision_threshold,
            min_ai_confidence=min_ai_confidence
        )
        self.healed_G, history_dicts = healer.heal_graph(frag_G, prob_mask=np.ones((200, 200)) * 0.85)
        stats = healer.compute_healing_statistics()
        
        # Convert explanations
        exp_models = []
        for d in history_dicts:
            exp_models.append({
                "repair_id": d.get("repair_id"),
                "edge_id": d.get("repair_id"),
                "source_node": d.get("source_node"),
                "destination_node": d.get("destination_node"),
                "distance": d.get("distance", 0.0),
                "ai_confidence": d.get("ai_confidence", 0.0),
                "direction_consistency": d.get("direction_consistency", 0.0),
                "road_width_similarity": d.get("road_width_similarity", 0.0),
                "local_road_density": d.get("local_road_density", 0.0),
                "hybrid_cost_score": d.get("hybrid_cost_score", 0.0),
                "decision_threshold": d.get("decision_threshold", 0.0),
                "status": d.get("status"),
                "accepted": d.get("accepted", False),
                "barrier_veto": False,
                "explanation": d.get("explanation", "")
            })

        builder = RoadGraphBuilder()
        
        return {
            "status": "success",
            "repaired_gap_count": stats["num_repaired_gaps"],
            "total_candidates_evaluated": stats["total_candidates_evaluated"],
            "false_connections_prevented": stats["false_connections_prevented"],
            "healed_geojson": builder.export_geojson(self.healed_G),
            "explanations": exp_models
        }

    def get_baseline_geojson(self) -> Dict[str, Any]:
        if self.geojson_cache is None:
            raise GraphNotInitializedError()
        return self.geojson_cache

    def run_criticality_analysis(self) -> Dict[str, Any]:
        if self.base_G is None:
            raise GraphNotInitializedError()
        analyzer = CriticalityAnalyzer(node_weights=self.config.criticality_weights)
        analyzer.analyze(self.base_G)
        return {
            "status": "success",
            "vulnerability_report": analyzer.generate_urban_vulnerability_report(),
            "network_resilience_score": analyzer.compute_network_resilience_score(),
            "top_critical_nodes": analyzer.get_critical_node_ranking(top_n=10),
            "top_critical_edges": analyzer.get_critical_edge_ranking(top_n=10)
        }

    def simulate_disaster(self, disaster_type: str, bbox: Optional[Dict[str, float]], failure_fraction: float) -> Dict[str, Any]:
        """Invokes StressSimulator to model regional or stochastic failures."""
        if self.base_G is None:
            raise GraphNotInitializedError()

        sim = StressSimulator(self.base_G)
        
        if bbox:
            lat_diff = bbox["max_lat"] - bbox["min_lat"]
            lon_diff = bbox["max_lon"] - bbox["min_lon"]
            if lat_diff > 0.20 or lon_diff > 0.20:
                raise BoundingBoxTooLargeError("Bounding box exceeds 0.20 degrees span (~20km). Please select a more localized regional disruption area.")

            # Find nodes within bbox
            nodes_to_remove = set()
            for n, d in self.base_G.nodes(data=True):
                geo = d.get("geographic_coord", (0, 0))
                if bbox["min_lat"] <= geo[0] <= bbox["max_lat"] and bbox["min_lon"] <= geo[1] <= bbox["max_lon"]:
                    nodes_to_remove.add(n)
            res = sim._execute_simulation(nodes_to_remove, set())
        else:
            res = sim.simulate_random_failure(failure_fraction=failure_fraction, seed=42)

        m = res["simulation_metrics"]
        ds = res["decision_support"]
        
        builder = RoadGraphBuilder()

        return {
            "status": "success",
            "resilience_score": m["composite_resilience_score"],
            "baseline_resilience_score": sim.baseline_metrics.get("composite_resilience_score", 1.0),
            "nodes_lost": m["removed_nodes_count"],
            "edges_lost": m["removed_edges_count"],
            "connected_components": m["connected_components"],
            "connectivity_ratio": m["connectivity_ratio"],
            "travel_impact_pct": m["travel_impact_estimate_pct"],
            "degraded_graph": builder.export_geojson(res["damaged_graph"]),
            "recommended_repair_priority": ds["recommended_repair_priority"]
        }


service_manager = BackendServiceManager()
