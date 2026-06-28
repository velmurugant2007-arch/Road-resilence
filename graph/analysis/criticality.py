import math
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional, Set
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from utils.logger import get_logger

logger = get_logger("graph.analysis.criticality")


class CriticalityAnalyzer:
    """
    Analytics engine for Phase 7.4.5 (Graph-Theoretic Criticality Analysis).
    Identifies critical road segments and junctions affecting urban mobility and resilience.
    Computes centrality metrics, k-core decomposition, bridges, cut vertices, and configurable composite scores.
    """

    def __init__(
        self,
        node_weights: Optional[Dict[str, float]] = None,
        edge_weights: Optional[Dict[str, float]] = None
    ):
        self.node_weights = node_weights or {
            "betweenness": 0.30,
            "closeness": 0.20,
            "degree": 0.15,
            "eigenvector": 0.15,
            "kcore": 0.10,
            "articulation": 0.10
        }
        self.edge_weights = edge_weights or {
            "edge_betweenness": 0.50,
            "bridge": 0.30,
            "end_nodes_composite": 0.20
        }
        self.G: Optional[nx.Graph] = None
        self.node_ranking: List[Dict[str, Any]] = []
        self.edge_ranking: List[Dict[str, Any]] = []
        self.articulation_points: Set[Any] = set()
        self.bridges: Set[Tuple[Any, Any]] = set()
        self.connected_components_count: int = 0
        self.largest_component_fraction: float = 0.0

    def _normalize_dict(self, d: Dict[Any, float]) -> Dict[Any, float]:
        """Normalizes dictionary values linearly to [0.0, 1.0]."""
        if not d:
            return {}
        vals = list(d.values())
        min_v, max_v = min(vals), max(vals)
        if max_v - min_v < 1e-9:
            return {k: 0.0 for k in d}
        return {k: float((v - min_v) / (max_v - min_v)) for k, v in d.items()}

    def analyze(self, G: nx.Graph) -> nx.Graph:
        """
        Executes core algorithmic criticality suite on input graph G.
        Attaches individual metric attributes and composite criticality scores to nodes and edges.
        """
        logger.info(f"Starting criticality analysis on graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
        self.G = G.copy()
        if self.G.number_of_nodes() == 0:
            return self.G

        # 1. Connected Components Analysis
        components = list(nx.connected_components(self.G))
        self.connected_components_count = len(components)
        largest_comp_size = max(len(c) for c in components) if components else 0
        self.largest_component_fraction = float(largest_comp_size / self.G.number_of_nodes()) if self.G.number_of_nodes() > 0 else 0.0

        # 2. Cut Vertices (Articulation Points) & Bridges
        try:
            self.articulation_points = set(nx.articulation_points(self.G))
        except Exception as e:
            logger.warning(f"Articulation point detection failed: {e}")
            self.articulation_points = set()

        try:
            raw_bridges = list(nx.bridges(self.G))
            self.bridges = { (min(u, v), max(u, v)) for u, v in raw_bridges }
        except Exception as e:
            logger.warning(f"Bridge detection failed: {e}")
            self.bridges = set()

        # 3. Node Centralities
        logger.debug("Computing betweenness and closeness centralities...")
        bet_cen = nx.betweenness_centrality(self.G, weight="length", normalized=True)
        close_cen = nx.closeness_centrality(self.G, distance="length", wf_improved=True)
        deg_cen = nx.degree_centrality(self.G)

        # Eigenvector Centrality (fallback gracefully if non-convergent or disconnected)
        try:
            eig_cen = nx.eigenvector_centrality(self.G, max_iter=1000, tol=1e-4)
        except Exception:
            try:
                eig_cen = nx.eigenvector_centrality_numpy(self.G)
            except Exception:
                logger.warning("Eigenvector centrality did not converge; defaulting to degree centrality distribution.")
                eig_cen = deg_cen.copy()

        # k-Core Decomposition
        try:
            kcore_dict = nx.core_number(self.G)
            kcore_norm = self._normalize_dict({k: float(v) for k, v in kcore_dict.items()})
        except Exception:
            kcore_norm = {n: 0.0 for n in self.G.nodes()}

        # Normalize metrics
        norm_bet = self._normalize_dict(bet_cen)
        norm_close = self._normalize_dict(close_cen)
        norm_deg = self._normalize_dict(deg_cen)
        norm_eig = self._normalize_dict(eig_cen)

        # Compute Composite Node Score
        nw = self.node_weights
        self.node_ranking = []
        for n in self.G.nodes():
            is_art = 1.0 if n in self.articulation_points else 0.0
            comp_score = (
                nw.get("betweenness", 0.3) * norm_bet.get(n, 0.0) +
                nw.get("closeness", 0.2) * norm_close.get(n, 0.0) +
                nw.get("degree", 0.15) * norm_deg.get(n, 0.0) +
                nw.get("eigenvector", 0.15) * norm_eig.get(n, 0.0) +
                nw.get("kcore", 0.1) * kcore_norm.get(n, 0.0) +
                nw.get("articulation", 0.1) * is_art
            )
            comp_score = round(float(comp_score), 4)
            
            self.G.nodes[n]["composite_criticality"] = comp_score
            self.G.nodes[n]["betweenness_centrality"] = round(bet_cen.get(n, 0.0), 4)
            self.G.nodes[n]["closeness_centrality"] = round(close_cen.get(n, 0.0), 4)
            self.G.nodes[n]["degree_centrality"] = round(deg_cen.get(n, 0.0), 4)
            self.G.nodes[n]["eigenvector_centrality"] = round(eig_cen.get(n, 0.0), 4)
            self.G.nodes[n]["is_articulation_point"] = bool(is_art)

            self.node_ranking.append({
                "node_id": n,
                "composite_criticality": comp_score,
                "betweenness": round(bet_cen.get(n, 0.0), 4),
                "closeness": round(close_cen.get(n, 0.0), 4),
                "degree": round(deg_cen.get(n, 0.0), 4),
                "is_articulation_point": bool(is_art)
            })

        self.node_ranking.sort(key=lambda x: x["composite_criticality"], reverse=True)

        # 4. Edge Centralities
        logger.debug("Computing edge betweenness centrality...")
        ebet_cen = nx.edge_betweenness_centrality(self.G, weight="length", normalized=True)
        norm_ebet = self._normalize_dict({(min(u, v), max(u, v)): val for (u, v), val in ebet_cen.items()})

        ew = self.edge_weights
        self.edge_ranking = []
        for u, v, data in self.G.edges(data=True):
            edge_key = (min(u, v), max(u, v))
            is_bridge = 1.0 if edge_key in self.bridges else 0.0
            ebet_val = norm_ebet.get(edge_key, 0.0)
            
            u_score = self.G.nodes[u].get("composite_criticality", 0.0)
            v_score = self.G.nodes[v].get("composite_criticality", 0.0)
            end_nodes_avg = (u_score + v_score) / 2.0

            edge_comp = (
                ew.get("edge_betweenness", 0.5) * ebet_val +
                ew.get("bridge", 0.3) * is_bridge +
                ew.get("end_nodes_composite", 0.2) * end_nodes_avg
            )
            edge_comp = round(float(edge_comp), 4)

            data["composite_criticality"] = edge_comp
            data["edge_betweenness_centrality"] = round(ebet_cen.get((u, v), ebet_cen.get((v, u), 0.0)), 4)
            data["is_bridge"] = bool(is_bridge)

            self.edge_ranking.append({
                "source": u,
                "target": v,
                "composite_criticality": edge_comp,
                "edge_betweenness": round(ebet_cen.get((u, v), ebet_cen.get((v, u), 0.0)), 4),
                "is_bridge": bool(is_bridge),
                "length": round(float(data.get("length", 0.0)), 2)
            })

        self.edge_ranking.sort(key=lambda x: x["composite_criticality"], reverse=True)
        logger.info("Criticality analysis completed successfully.")
        return self.G

    def get_critical_node_ranking(self, top_n: int = 10) -> List[Dict[str, Any]]:
        """Returns top N critical nodes sorted by composite score."""
        return self.node_ranking[:top_n]

    def get_critical_edge_ranking(self, top_n: int = 10) -> List[Dict[str, Any]]:
        """Returns top N critical edges sorted by composite score."""
        return self.edge_ranking[:top_n]

    def generate_urban_vulnerability_report(self) -> Dict[str, Any]:
        """
        Generates comprehensive Urban Vulnerability Report summarizing network cut points,
        bridges, fragmentation risk, and component distribution.
        """
        if not self.G or self.G.number_of_nodes() == 0:
            return {}

        num_nodes = self.G.number_of_nodes()
        num_edges = self.G.number_of_edges()
        num_art = len(self.articulation_points)
        num_bridges = len(self.bridges)

        art_ratio = num_art / max(1, num_nodes)
        bridge_ratio = num_bridges / max(1, num_edges)

        # Determine structural risk level
        if self.connected_components_count > 5 or art_ratio > 0.15 or bridge_ratio > 0.20:
            risk_level = "Critical"
        elif self.connected_components_count > 2 or art_ratio > 0.08 or bridge_ratio > 0.10:
            risk_level = "High"
        elif art_ratio > 0.03 or bridge_ratio > 0.05:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        report = {
            "total_nodes": num_nodes,
            "total_edges": num_edges,
            "connected_components": self.connected_components_count,
            "largest_component_fraction": round(self.largest_component_fraction, 4),
            "articulation_points_count": num_art,
            "bridges_count": num_bridges,
            "articulation_point_ratio": round(art_ratio, 4),
            "bridge_ratio": round(bridge_ratio, 4),
            "urban_vulnerability_risk_level": risk_level
        }
        logger.info(f"Urban Vulnerability Report generated: Risk Level = {risk_level}")
        return report

    def compute_network_resilience_score(self) -> float:
        """
        Computes scalar Network Resilience Score in [0.0, 1.0].
        Synthesizes component continuity, bridge redundancy, and articulation point robustess.
        """
        if not self.G or self.G.number_of_nodes() == 0:
            return 0.0

        num_nodes = self.G.number_of_nodes()
        num_edges = self.G.number_of_edges()

        # Component continuity factor
        f_lcc = self.largest_component_fraction

        # Bridge redundancy (1.0 means no bridges; lower means heavy bottlenecking)
        r_bridge = 1.0 - min(1.0, len(self.bridges) / max(1, num_edges))

        # Cut vertex robustness
        r_art = 1.0 - min(1.0, len(self.articulation_points) / max(1, num_nodes))

        # Weighted composite structural resilience index
        resilience_score = 0.40 * f_lcc + 0.30 * r_bridge + 0.30 * r_art
        return round(float(resilience_score), 4)

    def generate_criticality_visualizations(
        self,
        bg_mask: Optional[np.ndarray],
        output_dir: Path
    ) -> Dict[str, str]:
        """
        Generates data structures and exports 3 diagnostic plots:
        1. Centrality Heatmap
        2. Critical Node Overlay
        3. Critical Edge Overlay
        """
        if not self.G or self.G.number_of_nodes() == 0:
            return {}

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        saved_paths = {}

        # Common base drawing helper
        def setup_base(ax, title):
            if bg_mask is not None:
                ax.imshow(bg_mask, cmap="gray", alpha=0.25)
            ax.set_title(title, fontsize=14, fontweight="bold")
            ax.axis("equal")
            ax.axis("off")

        # 1. Centrality Heatmap (Node Composite Criticality)
        fig, ax = plt.subplots(figsize=(10, 10))
        setup_base(ax, "Urban Mobility Network — Centrality Heatmap")
        
        # Draw background edges lightly
        for u, v, attr in self.G.edges(data=True):
            poly = attr.get("geometry", [])
            if poly:
                ax.plot([p[1] for p in poly], [p[0] for p in poly], color="#cccccc", linewidth=1, alpha=0.5)

        nx_coords, ny_coords, scores = [], [], []
        for n, d in self.G.nodes(data=True):
            r, c = d.get("pixel_coord", (0, 0))
            nx_coords.append(c)
            ny_coords.append(r)
            scores.append(d.get("composite_criticality", 0.0))

        sc = ax.scatter(nx_coords, ny_coords, c=scores, cmap="inferno", s=40, zorder=4)
        cbar = plt.colorbar(sc, ax=ax, fraction=0.036, pad=0.04)
        cbar.set_label("Composite Criticality Score", fontsize=11)
        
        p1 = output_dir / "centrality_heatmap.png"
        plt.tight_layout()
        plt.savefig(p1, dpi=150)
        plt.close(fig)
        saved_paths["centrality_heatmap"] = str(p1)

        # 2. Critical Node Overlay (Highlighting Cut Vertices / Articulation Points)
        fig, ax = plt.subplots(figsize=(10, 10))
        setup_base(ax, "Critical Node Overlay — Articulation Points & High-Risk Junctions")
        for u, v, attr in self.G.edges(data=True):
            poly = attr.get("geometry", [])
            if poly:
                ax.plot([p[1] for p in poly], [p[0] for p in poly], color="#3388ff", linewidth=1.5, alpha=0.6)

        top_score_cutoff = np.percentile(scores, 85) if scores else 0.5
        reg_x, reg_y = [], []
        crit_x, crit_y = [], []
        art_x, art_y = [], []

        for n, d in self.G.nodes(data=True):
            r, c = d.get("pixel_coord", (0, 0))
            if d.get("is_articulation_point"):
                art_x.append(c)
                art_y.append(r)
            elif d.get("composite_criticality", 0.0) >= top_score_cutoff:
                crit_x.append(c)
                crit_y.append(r)
            else:
                reg_x.append(c)
                reg_y.append(r)

        if reg_x: ax.scatter(reg_x, reg_y, c="#666666", s=15, alpha=0.6, label="Standard Nodes")
        if crit_x: ax.scatter(crit_x, crit_y, c="#ff6600", s=50, label="Top 15% Critical Nodes", zorder=5)
        if art_x: ax.scatter(art_x, art_y, c="#ff0000", s=100, marker="*", label="Articulation Points (Cut Vertices)", zorder=6)
        ax.legend(loc="upper right")

        p2 = output_dir / "critical_node_overlay.png"
        plt.tight_layout()
        plt.savefig(p2, dpi=150)
        plt.close(fig)
        saved_paths["critical_node_overlay"] = str(p2)

        # 3. Critical Edge Overlay (Highlighting Bridges / Bottlenecks)
        fig, ax = plt.subplots(figsize=(10, 10))
        setup_base(ax, "Critical Edge Overlay — Network Bridges & Bottleneck Roads")

        edge_scores = [d.get("composite_criticality", 0.0) for _, _, d in self.G.edges(data=True)]
        edge_cutoff = np.percentile(edge_scores, 85) if edge_scores else 0.5

        for u, v, attr in self.G.edges(data=True):
            poly = attr.get("geometry", [])
            if not poly:
                r1, c1 = self.G.nodes[u]["pixel_coord"]
                r2, c2 = self.G.nodes[v]["pixel_coord"]
                poly = [(r1, c1), (r2, c2)]
            xs = [p[1] for p in poly]
            ys = [p[0] for p in poly]

            if attr.get("is_bridge"):
                ax.plot(xs, ys, color="#ff00ff", linestyle="--", linewidth=3.5, label="Network Bridge (Single Point of Failure)", zorder=6)
            elif attr.get("composite_criticality", 0.0) >= edge_cutoff:
                ax.plot(xs, ys, color="#ff3300", linewidth=2.5, zorder=5)
            else:
                ax.plot(xs, ys, color="#00aa88", linewidth=1.5, alpha=0.5)

        # Dedup legends
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        if by_label:
            ax.legend(by_label.values(), by_label.keys(), loc="upper right")

        p3 = output_dir / "critical_edge_overlay.png"
        plt.tight_layout()
        plt.savefig(p3, dpi=150)
        plt.close(fig)
        saved_paths["critical_edge_overlay"] = str(p3)

        logger.info(f"Generated 3 criticality overlay plots in {output_dir}")
        return saved_paths
