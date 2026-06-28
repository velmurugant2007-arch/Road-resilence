import math
import random
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional, Set
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from utils.logger import get_logger

logger = get_logger("graph.resilience.simulator")


class StressSimulator:
    """
    Simulation engine for Phase 7.4.6 (Urban Mobility Stress Simulation).
    Evaluates the impact of localized infrastructure failures on urban road connectivity,
    computes global network efficiency, generates decision support repair priorities, and renders visual diagnostic overlays.
    """

    def __init__(self, base_G: nx.Graph):
        self.base_G = base_G.copy()
        self.baseline_metrics: Dict[str, Any] = {}
        if self.base_G.number_of_nodes() > 0:
            self.baseline_metrics = self._compute_network_metrics(self.base_G, is_baseline=True)

    def _compute_network_efficiency(self, G: nx.Graph) -> float:
        """
        Computes Latora-Marchiori global network efficiency:
        E = 1 / (N * (N - 1)) * sum_{i != j} (1 / d(i, j))
        Using 'length' edge attribute for distance. If disconnected or N < 2, returns 0.0.
        To ensure performance on larger graphs, we sample or compute component-wise.
        """
        n = G.number_of_nodes()
        if n < 2:
            return 0.0

        nodes = list(G.nodes())
        # For efficiency on graphs > 300 nodes, sample 150 random source nodes
        sample_nodes = nodes if n <= 300 else random.sample(nodes, 150)
        
        total_inv_dist = 0.0
        count = 0
        for u in sample_nodes:
            lengths = nx.single_source_dijkstra_path_length(G, u, weight="length")
            for v, dist in lengths.items():
                if u != v and dist > 1e-6:
                    total_inv_dist += 1.0 / dist
                    count += 1

        # Normalize by total pairs sampled
        max_pairs = len(sample_nodes) * (n - 1)
        return float(total_inv_dist / max_pairs) if max_pairs > 0 else 0.0

    def _compute_network_metrics(self, G: nx.Graph, is_baseline: bool = False, removed_nodes: Optional[Set[Any]] = None, removed_edges: Optional[Set[Tuple[Any, Any]]] = None) -> Dict[str, Any]:
        """Computes comprehensive structural and mobility metrics for graph G."""
        n = G.number_of_nodes()
        m = G.number_of_edges()
        base_n = self.base_G.number_of_nodes()

        if n == 0 or base_n == 0:
            return {
                "connected_components": 0,
                "largest_component_size": 0,
                "largest_component_fraction": 0.0,
                "average_shortest_path_length": 0.0,
                "network_efficiency": 0.0,
                "connectivity_ratio": 0.0,
                "travel_impact_estimate_pct": 100.0,
                "composite_resilience_score": 0.0,
                "removed_nodes_count": len(removed_nodes or []),
                "removed_edges_count": len(removed_edges or [])
            }

        components = list(nx.connected_components(G))
        num_comp = len(components)
        largest_comp = max(components, key=len) if components else set()
        lcc_size = len(largest_comp)
        lcc_fraction = float(lcc_size / base_n)

        # Average shortest path length on largest connected component
        if lcc_size >= 2:
            sub_G = G.subgraph(largest_comp)
            # If > 200 nodes, approximate ASPL
            if lcc_size > 200:
                sample_src = random.sample(list(sub_G.nodes()), 50)
                lens = []
                for src in sample_src:
                    dists = nx.single_source_dijkstra_path_length(sub_G, src, weight="length")
                    lens.extend([d for tgt, d in dists.items() if src != tgt])
                aspl = float(np.mean(lens)) if lens else 0.0
            else:
                aspl = float(nx.average_shortest_path_length(sub_G, weight="length"))
        else:
            aspl = 0.0

        efficiency = self._compute_network_efficiency(G)

        # Connectivity ratio: ratio of reachable pairs compared to baseline
        # Roughly approximated by sum(size * (size - 1)) / baseline_pairs
        base_pairs = base_n * (base_n - 1)
        surviving_pairs = sum(len(c) * (len(c) - 1) for c in components)
        conn_ratio = float(surviving_pairs / base_pairs) if base_pairs > 0 else 1.0

        # Travel impact estimate: drop in efficiency or increase in ASPL
        base_eff = self.baseline_metrics.get("network_efficiency", efficiency) if not is_baseline else efficiency
        if base_eff > 1e-6:
            eff_drop = max(0.0, (base_eff - efficiency) / base_eff) * 100.0
        else:
            eff_drop = 0.0

        # Composite resilience score bounded in [0, 1]
        # Combines LCC retention, surviving connectivity, and relative efficiency
        eff_ratio = float(efficiency / base_eff) if base_eff > 1e-6 else 1.0
        resilience_score = 0.40 * lcc_fraction + 0.35 * conn_ratio + 0.25 * min(1.0, eff_ratio)

        return {
            "connected_components": num_comp,
            "largest_component_size": lcc_size,
            "largest_component_fraction": round(lcc_fraction, 4),
            "average_shortest_path_length": round(aspl, 2),
            "network_efficiency": round(efficiency, 6),
            "connectivity_ratio": round(conn_ratio, 4),
            "travel_impact_estimate_pct": round(eff_drop, 2),
            "composite_resilience_score": round(float(resilience_score), 4),
            "removed_nodes_count": len(removed_nodes or []),
            "removed_edges_count": len(removed_edges or [])
        }

    def _execute_simulation(self, nodes_to_remove: Set[Any], edges_to_remove: Set[Tuple[Any, Any]]) -> Dict[str, Any]:
        """Internal helper to mutate graph, calculate post-damage metrics, and generate decision support recommendations."""
        sim_G = self.base_G.copy()
        sim_G.remove_nodes_from(nodes_to_remove)
        for u, v in edges_to_remove:
            if sim_G.has_edge(u, v):
                sim_G.remove_edge(u, v)

        metrics = self._compute_network_metrics(sim_G, removed_nodes=nodes_to_remove, removed_edges=edges_to_remove)

        # Decision Support: Recommend repair priorities by evaluating Delta R for restoring each removed item
        repair_priority = []
        base_res = metrics["composite_resilience_score"]

        for n in nodes_to_remove:
            if n in self.base_G:
                test_G = sim_G.copy()
                test_G.add_node(n, **self.base_G.nodes[n])
                for nbr in self.base_G.neighbors(n):
                    if nbr in test_G:
                        test_G.add_edge(n, nbr, **self.base_G.edges[n, nbr])
                test_m = self._compute_network_metrics(test_G)
                delta_r = round(test_m["composite_resilience_score"] - base_res, 4)
                repair_priority.append({
                    "element_type": "node",
                    "element_id": n,
                    "estimated_resilience_improvement": max(0.0, delta_r),
                    "priority_rank": 0
                })

        for u, v in edges_to_remove:
            if self.base_G.has_edge(u, v) and u in sim_G and v in sim_G:
                test_G = sim_G.copy()
                test_G.add_edge(u, v, **self.base_G.edges[u, v])
                test_m = self._compute_network_metrics(test_G)
                delta_r = round(test_m["composite_resilience_score"] - base_res, 4)
                repair_priority.append({
                    "element_type": "edge",
                    "element_id": f"{u}-{v}",
                    "source": u,
                    "target": v,
                    "estimated_resilience_improvement": max(0.0, delta_r),
                    "priority_rank": 0
                })

        repair_priority.sort(key=lambda x: x["estimated_resilience_improvement"], reverse=True)
        for idx, item in enumerate(repair_priority, 1):
            item["priority_rank"] = idx

        # Identify most affected regions (bounding box of disconnected nodes)
        disconnected_nodes = set(self.base_G.nodes()) - set(sim_G.nodes())
        for comp in nx.connected_components(sim_G):
            if len(comp) < metrics["largest_component_size"]:
                disconnected_nodes.update(comp)

        affected_coords = [self.base_G.nodes[n]["pixel_coord"] for n in disconnected_nodes if n in self.base_G and "pixel_coord" in self.base_G.nodes[n]]
        if affected_coords:
            min_r = min(p[0] for p in affected_coords)
            max_r = max(p[0] for p in affected_coords)
            min_c = min(p[1] for p in affected_coords)
            max_c = max(p[1] for p in affected_coords)
            affected_region_summary = {"min_row": min_r, "max_row": max_r, "min_col": min_c, "max_col": max_c, "isolated_node_count": len(disconnected_nodes)}
        else:
            affected_region_summary = {"isolated_node_count": 0}

        return {
            "simulation_metrics": metrics,
            "decision_support": {
                "most_affected_region": affected_region_summary,
                "recommended_repair_priority": repair_priority[:10],
                "total_repair_candidates_evaluated": len(repair_priority)
            },
            "damaged_graph": sim_G
        }

    def simulate_single_node_failure(self, node_id: Any) -> Dict[str, Any]:
        """Simulates complete failure and removal of a single junction/node."""
        logger.info(f"Simulating single-node failure: {node_id}")
        return self._execute_simulation({node_id}, set())

    def simulate_multi_node_failure(self, node_ids: List[Any]) -> Dict[str, Any]:
        """Simulates simultaneous failure of multiple selected nodes."""
        logger.info(f"Simulating multi-node failure ({len(node_ids)} nodes)")
        return self._execute_simulation(set(node_ids), set())

    def simulate_regional_failure(self, center_coord: Tuple[float, float], radius_meters: float) -> Dict[str, Any]:
        """Simulates localized flood or landslide failure within radial distance from center (row, col)."""
        logger.info(f"Simulating regional failure centered at {center_coord} with radius {radius_meters}")
        cr, cc = center_coord
        nodes_in_region = set()
        for n, d in self.base_G.nodes(data=True):
            r, c = d.get("pixel_coord", (0, 0))
            if math.hypot(r - cr, c - cc) <= radius_meters:
                nodes_in_region.add(n)
        return self._execute_simulation(nodes_in_region, set())

    def simulate_random_failure(self, failure_fraction: float = 0.10, seed: Optional[int] = None) -> Dict[str, Any]:
        """Simulates stochastic distributed infrastructure failure of a given node fraction."""
        if seed is not None:
            random.seed(seed)
        all_nodes = list(self.base_G.nodes())
        num_fail = int(len(all_nodes) * failure_fraction)
        failed_nodes = set(random.sample(all_nodes, min(num_fail, len(all_nodes))))
        logger.info(f"Simulating random failure ({failure_fraction*100:.1f}% = {len(failed_nodes)} nodes)")
        return self._execute_simulation(failed_nodes, set())

    def simulate_custom_failure(self, node_ids: List[Any], edge_ids: List[Tuple[Any, Any]]) -> Dict[str, Any]:
        """Simulates custom user-defined scenario removing both nodes and specific road edges."""
        logger.info(f"Simulating custom failure ({len(node_ids)} nodes, {len(edge_ids)} edges)")
        norm_edges = {(min(u, v), max(u, v)) for u, v in edge_ids}
        return self._execute_simulation(set(node_ids), norm_edges)

    def generate_simulation_visualizations(
        self,
        sim_result: Dict[str, Any],
        bg_mask: Optional[np.ndarray],
        output_dir: Path
    ) -> Dict[str, str]:
        """
        Generates and exports 4 diagnostic stress simulation plots:
        1. Before vs After graph comparison
        2. Heatmap of affected regions
        3. Connectivity comparison chart
        4. Impact dashboard summary
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        saved_paths = {}
        damaged_G: nx.Graph = sim_result["damaged_graph"]
        metrics = sim_result["simulation_metrics"]

        # 1. Before vs After Graph Comparison
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        if bg_mask is not None:
            ax1.imshow(bg_mask, cmap="gray", alpha=0.3)
            ax2.imshow(bg_mask, cmap="gray", alpha=0.3)
        ax1.set_title("Baseline Road Network", fontsize=13, fontweight="bold")
        ax2.set_title(f"Post-Damage Network (Resilience: {metrics['composite_resilience_score']:.2f})", fontsize=13, fontweight="bold")

        for u, v, attr in self.base_G.edges(data=True):
            poly = attr.get("geometry", [])
            if not poly:
                r1, c1 = self.base_G.nodes[u]["pixel_coord"]
                r2, c2 = self.base_G.nodes[v]["pixel_coord"]
                poly = [(r1, c1), (r2, c2)]
            xs = [p[1] for p in poly]
            ys = [p[0] for p in poly]
            ax1.plot(xs, ys, color="#00d2ff", linewidth=1.5, alpha=0.8)

            if damaged_G.has_edge(u, v) and u in damaged_G and v in damaged_G:
                ax2.plot(xs, ys, color="#00ff66", linewidth=1.5, alpha=0.8)
            else:
                ax2.plot(xs, ys, color="#ff0033", linestyle="--", linewidth=2.0, alpha=0.9, label="Failed/Disconnected Segment")

        ax1.axis("equal"); ax1.axis("off")
        ax2.axis("equal"); ax2.axis("off")
        p1 = output_dir / "sim_before_after.png"
        plt.tight_layout()
        plt.savefig(p1, dpi=150)
        plt.close(fig)
        saved_paths["before_after"] = str(p1)

        # 2. Heatmap of Affected Regions (Isolated nodes & broken edges)
        fig, ax = plt.subplots(figsize=(10, 10))
        if bg_mask is not None:
            ax.imshow(bg_mask, cmap="gray", alpha=0.3)
        ax.set_title("Stress Impact Heatmap — Isolated Regions & Road Cut Points", fontsize=13, fontweight="bold")
        
        for u, v, attr in damaged_G.edges(data=True):
            r1, c1 = damaged_G.nodes[u]["pixel_coord"]
            r2, c2 = damaged_G.nodes[v]["pixel_coord"]
            ax.plot([c1, c2], [r1, r2], color="#aaaaaa", linewidth=1, alpha=0.4)

        failed_nodes = set(self.base_G.nodes()) - set(damaged_G.nodes())
        fx, fy = [], []
        for n in failed_nodes:
            r, c = self.base_G.nodes[n]["pixel_coord"]
            fx.append(c); fy.append(r)
        if fx:
            ax.scatter(fx, fy, c="red", s=80, marker="X", label="Failed Junctions/Endpoints", zorder=6)

        ax.axis("equal"); ax.axis("off")
        if fx: ax.legend(loc="upper right")
        p2 = output_dir / "sim_affected_heatmap.png"
        plt.tight_layout()
        plt.savefig(p2, dpi=150)
        plt.close(fig)
        saved_paths["affected_heatmap"] = str(p2)

        # 3. Connectivity Comparison Chart
        fig, ax = plt.subplots(figsize=(8, 6))
        labels = ["Connectivity Ratio", "Largest Comp %", "Efficiency %", "Resilience Score"]
        base_vals = [100.0, 100.0, 100.0, self.baseline_metrics.get("composite_resilience_score", 1.0) * 100.0]
        post_vals = [
            metrics["connectivity_ratio"] * 100.0,
            metrics["largest_component_fraction"] * 100.0,
            max(0.0, 100.0 - metrics["travel_impact_estimate_pct"]),
            metrics["composite_resilience_score"] * 100.0
        ]
        x = np.arange(len(labels))
        width = 0.35
        ax.bar(x - width/2, base_vals, width, label="Baseline", color="#0088ff")
        ax.bar(x + width/2, post_vals, width, label="Post-Failure Simulation", color="#ff4400")
        ax.set_ylabel("Metric Index (%)", fontsize=11)
        ax.set_title("Network Resilience & Connectivity Retention", fontsize=13, fontweight="bold")
        ax.set_xticks(x); ax.set_xticklabels(labels, fontweight="bold")
        ax.set_ylim(0, 115)
        ax.legend()
        p3 = output_dir / "sim_connectivity_chart.png"
        plt.tight_layout()
        plt.savefig(p3, dpi=150)
        plt.close(fig)
        saved_paths["connectivity_chart"] = str(p3)

        # 4. Impact Dashboard Summary Text Visual
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.axis("off")
        summary_text = (
            f"URBAN MOBILITY STRESS SIMULATION SUMMARY\n"
            f"=========================================\n\n"
            f"• Failed Elements: {metrics['removed_nodes_count']} Nodes | {metrics['removed_edges_count']} Edges\n"
            f"• Surviving Connected Components: {metrics['connected_components']}\n"
            f"• Largest Component Fraction: {metrics['largest_component_fraction']*100:.1f}%\n"
            f"• Connectivity Retention: {metrics['connectivity_ratio']*100:.1f}%\n"
            f"• Travel Efficiency Loss: {metrics['travel_impact_estimate_pct']:.1f}%\n"
            f"• Composite Resilience Index: {metrics['composite_resilience_score']:.4f}\n\n"
            f"Top Recommended Repair Priority: "
            f"{sim_result['decision_support']['recommended_repair_priority'][0]['element_id'] if sim_result['decision_support']['recommended_repair_priority'] else 'None'}\n"
        )
        ax.text(0.05, 0.5, summary_text, fontsize=12, fontfamily="monospace", verticalalignment="center",
                bbox=dict(boxstyle="round,pad=1", facecolor="#f8f9fa", edgecolor="#ced4da", linewidth=2))
        p4 = output_dir / "sim_impact_summary.png"
        plt.tight_layout()
        plt.savefig(p4, dpi=150)
        plt.close(fig)
        saved_paths["impact_summary"] = str(p4)

        logger.info(f"Generated 4 diagnostic stress simulation visual reports in {output_dir}")
        return saved_paths
