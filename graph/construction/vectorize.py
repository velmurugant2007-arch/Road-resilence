import time
import numpy as np
from scipy.ndimage import convolve, label
from typing import List, Tuple, Dict, Any
import matplotlib.pyplot as plt
from pathlib import Path
from utils.logger import get_logger

logger = get_logger("graph.construction.vectorize")


class RoadVectorizer:
    """
    Converts 1-pixel-wide binary skeleton masks into topological vector polylines.
    
    Performs skeleton chain tracing, node detection (junctions and endpoints),
    spur pruning, Ramer-Douglas-Peucker (RDP) polyline simplification, and
    connectivity verification.
    
    Architecture Traceability:
        - Phase 7.4.2 (Vectorization)
        - ISRO Alignment FR-02: Maintain topological road network connectivity.
    """

    def __init__(
        self,
        min_spur_length: int = 10,
        rdp_epsilon: float = 2.0
    ):
        """
        Args:
            min_spur_length: Maximum length (in pixels) of dead-end branches
                             attached to junctions to be pruned as noise.
            rdp_epsilon: Maximum distance tolerance (in pixels) for Ramer-Douglas-Peucker
                         polyline simplification.
        """
        self.min_spur_length = min_spur_length
        self.rdp_epsilon = rdp_epsilon
        # 3x3 kernel for 8-neighbor connectivity counting
        self.neighbor_kernel = np.array([
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ], dtype=np.uint8)

    def _compute_degree_map(self, skel: np.ndarray) -> np.ndarray:
        """Computes the 8-connected degree for every skeleton pixel."""
        # Convolve counts neighbors; mask by skel so background stays 0
        counts = convolve(skel.astype(np.uint8), self.neighbor_kernel, mode="constant", cval=0)
        return counts * skel.astype(np.uint8)

    def detect_nodes(self, skel: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Identifies Endpoints (degree == 1) and Junctions (degree >= 3).
        
        Returns:
            endpoints: boolean mask of endpoint locations
            junctions: boolean mask of junction locations
        """
        deg = self._compute_degree_map(skel)
        endpoints = (deg == 1) & (skel == 1)
        junctions = (deg >= 3) & (skel == 1)
        return endpoints, junctions

    def prune_spurs(self, skel: np.ndarray) -> np.ndarray:
        """
        Removes short dead-end spurs originating from junctions without eroding main branches.
        An endpoint whose path terminates at a junction and is shorter than `min_spur_length` is removed.
        """
        if self.min_spur_length <= 0:
            return skel

        current_skel = skel.copy()
        deg = self._compute_degree_map(current_skel)
        endpoints = np.argwhere((deg == 1) & (current_skel == 1))
        junctions = set(map(tuple, np.argwhere((deg >= 3) & (current_skel == 1))))

        if not junctions:
            return current_skel

        spurs_to_remove = []
        for ep in endpoints:
            curr = tuple(ep)
            path = [curr]
            visited = {curr}
            hit_junction = False

            while len(path) <= self.min_spur_length:
                r, c = curr
                # Check neighbors in skeleton
                neighbors = []
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < current_skel.shape[0] and 0 <= nc < current_skel.shape[1]:
                            if current_skel[nr, nc] == 1 and (nr, nc) not in visited:
                                if (nr, nc) in junctions:
                                    hit_junction = True
                                else:
                                    neighbors.append((nr, nc))
                if hit_junction:
                    break
                if not neighbors:
                    break
                curr = neighbors[0]
                visited.add(curr)
                path.append(curr)

            if hit_junction and len(path) <= self.min_spur_length:
                spurs_to_remove.extend(path)

        for r, c in spurs_to_remove:
            current_skel[r, c] = 0

        logger.debug(f"Pruned {len(spurs_to_remove)} spur pixels up to length {self.min_spur_length}.")
        return current_skel

    def _order_component_pixels(self, coords: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Orders a set of component coordinates into a sequential path using hash lookups."""
        if len(coords) <= 1:
            return coords

        coord_set = set(coords)
        
        # Find an endpoint within this component (a coordinate with exactly 1 neighbor in coord_set)
        start_node = coords[0]
        for pt in coords:
            r, c = pt
            nbr_count = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0: continue
                    if (r + dr, c + dc) in coord_set:
                        nbr_count += 1
            if nbr_count == 1:
                start_node = pt
                break

        path = [start_node]
        visited = {start_node}
        curr = start_node

        while len(path) < len(coords):
            r, c = curr
            found_next = False
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0: continue
                    nxt = (r + dr, c + dc)
                    if nxt in coord_set and nxt not in visited:
                        curr = nxt
                        visited.add(curr)
                        path.append(curr)
                        found_next = True
                        break
                if found_next:
                    break
            if not found_next:
                break

        return path

    def _perpendicular_distance(self, point: np.ndarray, line_start: np.ndarray, line_end: np.ndarray) -> float:
        """Computes 2D perpendicular distance from point to segment [line_start, line_end]."""
        if np.allclose(line_start, line_end):
            return np.linalg.norm(point - line_start)
        return np.abs(np.cross(line_end - line_start, line_start - point)) / np.linalg.norm(line_end - line_start)

    def ramer_douglas_peucker(self, points: List[Tuple[int, int]], epsilon: float) -> List[Tuple[int, int]]:
        """Simplified iterative/recursive RDP algorithm to reduce polyline vertices."""
        if len(points) <= 2 or epsilon <= 0:
            return points

        pts = np.array(points, dtype=np.float64)
        start, end = pts[0], pts[-1]

        # Find point with maximum distance
        dists = [self._perpendicular_distance(p, start, end) for p in pts]
        max_dist = np.max(dists)
        index = np.argmax(dists)

        if max_dist > epsilon:
            # Recursive simplification
            left = self.ramer_douglas_peucker(points[:index + 1], epsilon)
            right = self.ramer_douglas_peucker(points[index:], epsilon)
            return left[:-1] + right
        else:
            return [points[0], points[-1]]

    def trace_polylines(self, skel: np.ndarray) -> List[List[Tuple[int, int]]]:
        """
        Extracts all vector polylines from the skeleton mask.
        Connects Junctions to Endpoints or Junctions to Junctions.
        """
        _, junctions = self.detect_nodes(skel)
        
        # Remove junctions to split skeleton into independent branch components
        skel_no_junc = skel.copy()
        skel_no_junc[junctions] = 0
        
        labeled, num_features = label(skel_no_junc)
        polylines = []

        junction_coords = set(map(tuple, np.argwhere(junctions > 0)))

        # Group non-zero pixel coordinates by component ID in O(N) time
        r_idx, c_idx = np.nonzero(labeled)
        comp_ids = labeled[r_idx, c_idx]
        coords_by_comp: Dict[int, List[Tuple[int, int]]] = {}
        for r, c, cid in zip(r_idx, c_idx, comp_ids):
            coords_by_comp.setdefault(int(cid), []).append((int(r), int(c)))

        for comp_id in range(1, num_features + 1):
            coords = coords_by_comp.get(comp_id, [])
            if not coords:
                continue
            path = self._order_component_pixels(coords)
            if not path:
                continue

            # Check if start or end are adjacent to junctions in original skel
            start_r, start_c = path[0]
            end_r, end_c = path[-1]

            # Find adjacent junctions for start
            adj_junc_start = []
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0: continue
                    nr, nc = start_r + dr, start_c + dc
                    if (nr, nc) in junction_coords:
                        adj_junc_start.append((nr, nc))

            # Find adjacent junctions for end
            adj_junc_end = []
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0: continue
                    nr, nc = end_r + dr, end_c + dc
                    if (nr, nc) in junction_coords:
                        adj_junc_end.append((nr, nc))

            # Attach closest junction to start if found
            if adj_junc_start:
                path.insert(0, adj_junc_start[0])
            # Attach closest junction to end if found (avoid duplicate if start == end)
            if adj_junc_end and (not adj_junc_start or adj_junc_end[0] != adj_junc_start[0] or len(path) > 1):
                path.append(adj_junc_end[0])

            # Simplify with RDP
            simplified = self.ramer_douglas_peucker(path, self.rdp_epsilon)
            polylines.append(simplified)

        # Also check for direct junction-to-junction adjacent edges
        j_list = list(junction_coords)
        for i in range(len(j_list)):
            for j in range(i + 1, len(j_list)):
                r1, c1 = j_list[i]
                r2, c2 = j_list[j]
                if max(abs(r1 - r2), abs(c1 - c2)) == 1:
                    polylines.append([(r1, c1), (r2, c2)])

        return polylines

    def verify_connectivity(self, skel: np.ndarray, polylines: List[List[Tuple[int, int]]]) -> bool:
        """
        Verifies that the number of connected components in the generated polylines
        matches the number of connected components in the input skeleton mask.
        """
        _, orig_features = label(skel)
        if orig_features == 0 and len(polylines) == 0:
            return True

        # Build adjacency graph of polylines endpoints/vertices
        parent = {}
        def find(u):
            if parent.setdefault(u, u) != u:
                parent[u] = find(parent[u])
            return parent[u]
        def union(u, v):
            parent[find(u)] = find(v)

        for poly in polylines:
            for k in range(len(poly) - 1):
                union(poly[k], poly[k+1])

        unique_components = len(set(find(u) for u in parent))
        
        # Note: sometimes adjacent junctions merged into single vector nodes might slightly alter component counts
        # But generally unique vector components should equal raster connected components
        is_connected = (unique_components == orig_features)
        if not is_connected:
            logger.warning(f"Connectivity mismatch: Raster components ({orig_features}) != Vector components ({unique_components})")
        return is_connected

    def vectorize(self, skel: np.ndarray) -> Dict[str, Any]:
        """
        Executes end-to-end vectorization pipeline and reports metrics.
        """
        start_time = time.perf_counter()
        
        # 1. Spur pruning
        pruned_skel = self.prune_spurs(skel)
        
        # 2. Node detection
        endpoints, junctions = self.detect_nodes(pruned_skel)
        num_endpoints = int(np.sum(endpoints))
        num_junctions = int(np.sum(junctions))
        
        # 3. Connected components
        _, num_components = label(pruned_skel)
        
        # 4. Polyline tracing & RDP simplification
        polylines = self.trace_polylines(pruned_skel)
        
        # Compute branch lengths
        lengths = []
        for poly in polylines:
            length = sum(np.hypot(poly[i+1][0] - poly[i][0], poly[i+1][1] - poly[i][1]) for i in range(len(poly) - 1))
            lengths.append(length)
        avg_branch_length = float(np.mean(lengths)) if lengths else 0.0
        
        # 5. Connectivity verification
        connectivity_preserved = self.verify_connectivity(pruned_skel, polylines)
        
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        
        results = {
            "polylines": polylines,
            "pruned_skeleton": pruned_skel,
            "metrics": {
                "connected_components": int(num_components),
                "junction_count": num_junctions,
                "endpoint_count": num_endpoints,
                "polyline_count": len(polylines),
                "avg_branch_length_px": round(avg_branch_length, 2),
                "connectivity_preserved": connectivity_preserved,
                "execution_time_ms": round(elapsed_ms, 2)
            }
        }
        logger.info(f"Vectorization completed in {elapsed_ms:.2f}ms — Polylines: {len(polylines)}, Junctions: {num_junctions}")
        return results

    def generate_visualizations(self, orig_mask: np.ndarray, skel: np.ndarray, polylines: List[List[Tuple[int, int]]], output_path: Path):
        """Generates Original Mask, Skeleton, and Skeleton Overlay visual report."""
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
        axes[0].imshow(orig_mask, cmap='gray')
        axes[0].set_title("Original Binary Mask", fontsize=14, fontweight='bold')
        axes[0].axis('off')
        
        axes[1].imshow(skel, cmap='gray')
        axes[1].set_title("1-px Centerline Skeleton", fontsize=14, fontweight='bold')
        axes[1].axis('off')
        
        axes[2].imshow(orig_mask, cmap='gray', alpha=0.5)
        for poly in polylines:
            ys = [p[0] for p in poly]
            xs = [p[1] for p in poly]
            axes[2].plot(xs, ys, color='cyan', linewidth=2, marker='o', markersize=3, markerfacecolor='red')
        axes[2].set_title("Vector Polyline Overlay (RDP Simplified)", fontsize=14, fontweight='bold')
        axes[2].axis('off')
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close(fig)
        logger.info(f"Saved vectorization visualization to {output_path}")
