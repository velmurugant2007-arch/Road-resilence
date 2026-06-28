import math
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from utils.logger import get_logger

logger = get_logger("graph.healing.healer")


class RepairExplanation:
    """
    Explainability object storing metadata for every candidate graph-healing decision.
    Traceable for debugging, validation, and dashboard demonstration.
    """
    def __init__(
        self,
        repair_id: str,
        source_node: str,
        destination_node: str,
        distance: float,
        ai_confidence: float,
        direction_score: float,
        width_score: float,
        density_score: float,
        hybrid_score: float,
        threshold: float,
        accepted: bool,
        explanation: str
    ):
        self.repair_id = repair_id
        self.source_node = source_node
        self.destination_node = destination_node
        self.distance = round(distance, 4)
        self.ai_confidence = round(ai_confidence, 4)
        self.direction_score = round(direction_score, 4)
        self.width_score = round(width_score, 4)
        self.density_score = round(density_score, 4)
        self.hybrid_score = round(hybrid_score, 4)
        self.threshold = threshold
        self.accepted = accepted
        self.status = "Accepted" if accepted else "Rejected"
        self.explanation = explanation

    def to_dict(self) -> Dict[str, Any]:
        return {
            "repair_id": self.repair_id,
            "source_node": self.source_node,
            "destination_node": self.destination_node,
            "distance": self.distance,
            "ai_confidence": self.ai_confidence,
            "direction_consistency": self.direction_score,
            "road_width_similarity": self.width_score,
            "local_road_density": self.density_score,
            "hybrid_cost_score": self.hybrid_score,
            "decision_threshold": self.threshold,
            "status": self.status,
            "accepted": self.accepted,
            "explanation": self.explanation
        }


class GraphHealer:
    """
    Reconnects fragmented road networks across cloud/shadow occlusions using an
    explainable Hybrid Cost Function.
    
    Weights:
        - Distance (w1 = 0.25)
        - AI Confidence (w2 = 0.35)
        - Direction Consistency (w3 = 0.20)
        - Road Width Similarity (w4 = 0.10)
        - Local Road Density (w5 = 0.10)
    """

    def __init__(
        self,
        max_search_radius: float = 100.0,
        decision_threshold: float = 0.65,
        min_ai_confidence: float = 0.30,
        weights: Optional[Tuple[float, float, float, float, float]] = None
    ):
        self.max_search_radius = max_search_radius
        self.threshold = decision_threshold
        self.min_ai_confidence = min_ai_confidence
        self.weights = weights or (0.25, 0.35, 0.20, 0.10, 0.10)
        self.repair_history: List[RepairExplanation] = []
        self._repair_counter = 1

    def _compute_direction_vector(self, G: nx.Graph, node: str) -> np.ndarray:
        """Computes outgoing unit direction vector for an endpoint based on incident edge."""
        neighbors = list(G.neighbors(node))
        if not neighbors:
            return np.array([0.0, 0.0])
        nbr = neighbors[0]
        r1, c1 = G.nodes[node]["pixel_coord"]
        r2, c2 = G.nodes[nbr]["pixel_coord"]
        # Direction pointing outward from neighbor to endpoint (continuation vector)
        vec = np.array([float(r1 - r2), float(c1 - c2)])
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 1e-6 else np.array([0.0, 0.0])

    def _sample_ai_confidence(self, r1: int, c1: int, r2: int, c2: int, prob_mask: Optional[np.ndarray]) -> float:
        """Samples average AI prediction probability along line segment connecting (r1, c1) and (r2, c2)."""
        if prob_mask is None:
            return 0.85  # Default baseline confidence when synthetic

        num_samples = max(int(math.hypot(r2 - r1, c2 - c1)), 2)
        rs = np.linspace(r1, r2, num_samples)
        cs = np.linspace(c1, c2, num_samples)
        
        h, w = prob_mask.shape
        vals = []
        for r, c in zip(rs, cs):
            ir, ic = int(round(r)), int(round(c))
            if 0 <= ir < h and 0 <= ic < w:
                vals.append(float(prob_mask[ir, ic]))
        
        return float(np.mean(vals)) if vals else 0.0

    def _compute_local_density(self, r: int, c: int, radius: int, density_mask: Optional[np.ndarray]) -> float:
        """Computes local road density in a window around (r, c)."""
        if density_mask is None:
            return 0.80  # Default baseline density

        h, w = density_mask.shape
        r_min, r_max = max(0, r - radius), min(h, r + radius + 1)
        c_min, c_max = max(0, c - radius), min(w, c + radius + 1)
        window = density_mask[r_min:r_max, c_min:c_max]
        return float(np.mean(window > 0))

    def evaluate_candidate(
        self,
        G: nx.Graph,
        u: str,
        v: str,
        prob_mask: Optional[np.ndarray] = None,
        density_mask: Optional[np.ndarray] = None
    ) -> RepairExplanation:
        """Evaluates a candidate connection between endpoints u and v and generates an explainability object."""
        r1, c1 = G.nodes[u]["pixel_coord"]
        r2, c2 = G.nodes[v]["pixel_coord"]
        
        dist = math.hypot(r2 - r1, c2 - c1)
        s_dist = max(0.0, 1.0 - (dist / self.max_search_radius))

        s_ai = self._sample_ai_confidence(r1, c1, r2, c2, prob_mask)

        # Direction alignment
        vec_u = self._compute_direction_vector(G, u)
        vec_v = self._compute_direction_vector(G, v)
        vec_uv = np.array([float(r2 - r1), float(c2 - c1)])
        norm_uv = np.linalg.norm(vec_uv)
        if norm_uv > 1e-6:
            vec_uv /= norm_uv
            cos_u = float(np.dot(vec_u, vec_uv))
            cos_v = float(np.dot(vec_v, -vec_uv))
            s_dir = max(0.0, (cos_u + cos_v) / 2.0)
        else:
            s_dir = 1.0

        # Width similarity (default 1.0 if width not tracked)
        w_u = G.nodes[u].get("width", 1.0)
        w_v = G.nodes[v].get("width", 1.0)
        max_w = max(w_u, w_v, 1.0)
        s_width = max(0.0, 1.0 - abs(w_u - w_v) / max_w)

        # Local density
        d_u = self._compute_local_density(r1, c1, 20, density_mask)
        d_v = self._compute_local_density(r2, c2, 20, density_mask)
        s_density = (d_u + d_v) / 2.0

        w1, w2, w3, w4, w5 = self.weights
        hybrid_score = w1 * s_dist + w2 * s_ai + w3 * s_dir + w4 * s_width + w5 * s_density

        # Safety rule: Never connect across obvious non-road barriers when AI confidence is low
        barrier_veto = (prob_mask is not None) and (s_ai < self.min_ai_confidence)
        accepted = (hybrid_score >= self.threshold) and not barrier_veto

        repair_id = f"RH-{self._repair_counter:03d}"
        self._repair_counter += 1

        if accepted:
            reasons = []
            if s_ai >= 0.7: reasons.append("strong AI road mask confidence")
            if s_dir >= 0.7: reasons.append("aligned collinear road trajectory")
            if s_dist >= 0.7: reasons.append("short gap distance")
            reason_str = ", ".join(reasons) if reasons else "satisfactory multi-factor scores"
            explanation = (
                f"Accepted because hybrid cost score ({hybrid_score:.2f}) exceeded threshold ({self.threshold}). "
                f"Connection supported by {reason_str}."
            )
        elif barrier_veto:
            explanation = (
                f"Rejected because AI road confidence across gap ({s_ai:.2f}) fell below mandatory minimum safety barrier threshold ({self.min_ai_confidence}), "
                f"preventing connection across obvious non-road barrier."
            )
        else:
            reasons = []
            if s_ai < 0.5: reasons.append("low AI road prediction across gap")
            if s_dir < 0.3: reasons.append("divergent or perpendicular orientation")
            if s_dist < 0.3: reasons.append("excessive occlusion distance")
            reason_str = ", ".join(reasons) if reasons else "insufficient combined score"
            explanation = (
                f"Rejected because hybrid cost score ({hybrid_score:.2f}) fell below threshold ({self.threshold}). "
                f"Connection penalised by {reason_str}."
            )

        return RepairExplanation(
            repair_id=repair_id,
            source_node=u,
            destination_node=v,
            distance=dist,
            ai_confidence=s_ai,
            direction_score=s_dir,
            width_score=s_width,
            density_score=s_density,
            hybrid_score=hybrid_score,
            threshold=self.threshold,
            accepted=accepted,
            explanation=explanation
        )

    def heal_graph(
        self,
        G: nx.Graph,
        prob_mask: Optional[np.ndarray] = None,
        density_mask: Optional[np.ndarray] = None
    ) -> Tuple[nx.Graph, List[Dict[str, Any]]]:
        """
        Identifies disconnected endpoints within search radius, evaluates hybrid costs,
        and reconnects valid edges while attaching full explainability metadata.
        """
        healed_G = G.copy()
        endpoints = [n for n, d in healed_G.nodes(data=True) if d.get("node_type") == "endpoint" or healed_G.degree(n) == 1]
        
        candidates: List[Tuple[float, str, str, RepairExplanation]] = []

        for i in range(len(endpoints)):
            for j in range(i + 1, len(endpoints)):
                u, v = endpoints[i], endpoints[j]
                if healed_G.has_edge(u, v):
                    continue
                
                r1, c1 = healed_G.nodes[u]["pixel_coord"]
                r2, c2 = healed_G.nodes[v]["pixel_coord"]
                if math.hypot(r2 - r1, c2 - c1) > self.max_search_radius:
                    continue

                explanation = self.evaluate_candidate(healed_G, u, v, prob_mask, density_mask)
                self.repair_history.append(explanation)
                candidates.append((explanation.hybrid_score, u, v, explanation))

        # Sort descending by hybrid score for greedy non-conflicting matching
        candidates.sort(key=lambda x: x[0], reverse=True)
        healed_nodes = set()
        accepted_repairs = []

        for score, u, v, exp in candidates:
            if exp.accepted and u not in healed_nodes and v not in healed_nodes:
                healed_nodes.add(u)
                healed_nodes.add(v)
                
                r1, c1 = healed_G.nodes[u]["pixel_coord"]
                r2, c2 = healed_G.nodes[v]["pixel_coord"]
                gx1, gy1 = healed_G.nodes[u].get("geo_coord", (float(c1), float(r1)))
                gx2, gy2 = healed_G.nodes[v].get("geo_coord", (float(c2), float(r2)))

                healed_G.add_edge(
                    u, v,
                    geometry=[(r1, c1), (r2, c2)],
                    geo_geometry=[(gx1, gy1), (gx2, gy2)],
                    length=exp.distance,
                    direction="bidirectional",
                    edge_type="healed",
                    repair_metadata=exp.to_dict(),
                    metadata={"road_type": "healed", "source": "graph_healer"}
                )
                accepted_repairs.append(exp.to_dict())
                logger.info(f"Healed edge {u} <-> {v} ({exp.repair_id}) | Score: {score:.2f}")

        logger.info(f"Graph healing complete. Added {len(accepted_repairs)} healed connections out of {len(candidates)} evaluated.")
        return healed_G, [exp.to_dict() for exp in self.repair_history]

    def compute_healing_statistics(self) -> Dict[str, Any]:
        """
        Generates graph-healing statistics:
        - Number of repaired gaps
        - Average gap length
        - Confidence distribution
        - False connection detection
        """
        total_eval = len(self.repair_history)
        accepted = [exp for exp in self.repair_history if exp.accepted]
        rejected = [exp for exp in self.repair_history if not exp.accepted]

        num_repaired = len(accepted)
        avg_gap_len = float(np.mean([exp.distance for exp in accepted])) if accepted else 0.0

        all_confs = [exp.ai_confidence for exp in self.repair_history]
        conf_dist = {
            "mean": round(float(np.mean(all_confs)), 4) if all_confs else 0.0,
            "min": round(float(np.min(all_confs)), 4) if all_confs else 0.0,
            "max": round(float(np.max(all_confs)), 4) if all_confs else 0.0,
            "std": round(float(np.std(all_confs)), 4) if all_confs else 0.0
        }

        # False connection detection: count of candidates rejected due to falling below threshold or safety barrier
        false_connections_prevented = len(rejected)

        stats = {
            "total_candidates_evaluated": total_eval,
            "num_repaired_gaps": num_repaired,
            "avg_gap_length": round(avg_gap_len, 2),
            "confidence_distribution": conf_dist,
            "false_connections_prevented": false_connections_prevented
        }
        logger.info(f"Healing statistics: {stats}")
        return stats

    def generate_healing_visualization(
        self,
        orig_G: nx.Graph,
        healed_G: nx.Graph,
        bg_mask: Optional[np.ndarray],
        output_path: Path
    ):
        """
        Generates a 4-panel diagnostic visualization report:
        1. Original graph
        2. Candidate connections
        3. Accepted repairs
        4. Final healed graph
        """
        fig, axes = plt.subplots(2, 2, figsize=(16, 16))
        ax_orig, ax_cand, ax_rep, ax_final = axes.flatten()

        def draw_base_graph(ax, G_to_draw, title):
            if bg_mask is not None:
                ax.imshow(bg_mask, cmap="gray", alpha=0.3)
            ax.set_title(title, fontsize=13, fontweight="bold")
            # Draw original edges
            for u, v, attr in G_to_draw.edges(data=True):
                if attr.get("edge_type") != "healed":
                    poly = attr.get("geometry", [])
                    if poly:
                        ys = [p[0] for p in poly]
                        xs = [p[1] for p in poly]
                        ax.plot(xs, ys, color="#00d2ff", linewidth=2, alpha=0.8)
            # Draw endpoints
            ex, ey = [], []
            for n, d in G_to_draw.nodes(data=True):
                if d.get("node_type") == "endpoint" or G_to_draw.degree(n) == 1:
                    r, c = d.get("pixel_coord", (0, 0))
                    ex.append(c)
                    ey.append(r)
            if ex:
                ax.scatter(ex, ey, c="#ff9900", s=30, marker="s", zorder=4)
            ax.axis("equal")
            ax.axis("off")

        # 1. Original Graph
        draw_base_graph(ax_orig, orig_G, "1. Original Fragmented Graph")

        # 2. Candidate Connections
        draw_base_graph(ax_cand, orig_G, "2. Evaluated Candidate Connections")
        for exp in self.repair_history:
            if exp.source_node in orig_G and exp.destination_node in orig_G:
                r1, c1 = orig_G.nodes[exp.source_node]["pixel_coord"]
                r2, c2 = orig_G.nodes[exp.destination_node]["pixel_coord"]
                color = "green" if exp.accepted else "red"
                style = "-" if exp.accepted else "--"
                alpha = 0.8 if exp.accepted else 0.4
                ax_cand.plot([c1, c2], [r1, r2], color=color, linestyle=style, linewidth=1.5, alpha=alpha)

        # 3. Accepted Repairs
        draw_base_graph(ax_rep, orig_G, "3. Accepted Repairs (Healed Gaps)")
        for exp in self.repair_history:
            if exp.accepted and exp.source_node in orig_G and exp.destination_node in orig_G:
                r1, c1 = orig_G.nodes[exp.source_node]["pixel_coord"]
                r2, c2 = orig_G.nodes[exp.destination_node]["pixel_coord"]
                ax_rep.plot([c1, c2], [r1, r2], color="#00ff66", linewidth=2.5, zorder=5)

        # 4. Final Healed Graph
        draw_base_graph(ax_final, healed_G, "4. Final Healed Network Graph")
        for u, v, attr in healed_G.edges(data=True):
            if attr.get("edge_type") == "healed":
                poly = attr.get("geometry", [])
                if poly:
                    ys = [p[0] for p in poly]
                    xs = [p[1] for p in poly]
                    ax_final.plot(xs, ys, color="#00ff66", linewidth=2.5, zorder=5)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close(fig)
        logger.info(f"Saved 4-panel healing visualization to {output_path}")
