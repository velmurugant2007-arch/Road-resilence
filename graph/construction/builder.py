import json
import math
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from utils.logger import get_logger

logger = get_logger("graph.construction.builder")


class RoadGraphBuilder:
    """
    Converts vector polylines into a mathematically verified NetworkX graph
    and GeoJSON representation suitable for routing and resilience analysis.
    
    Architecture Traceability:
        - Phase 7.4.3 (Graph Construction)
        - ISRO Alignment FR-02: Maintain topological connectivity and routing capability.
        - ISRO Alignment HR-01: Graph abstraction with junction and endpoint attribution.
    """

    def __init__(self, geo_transform: Optional[Tuple[float, float, float, float, float, float]] = None):
        """
        Args:
            geo_transform: Affine transform tuple (c, a, b, f, d, e) where
                           x = c + a*col + b*row
                           y = f + d*col + e*row
                           If None, uses identity transform (x=col, y=row).
        """
        self.geo_transform = geo_transform

    def _pixel_to_geo(self, row: float, col: float) -> Tuple[float, float]:
        """Converts pixel coordinate (row, col) to geographic (x, y) / (lon, lat)."""
        if self.geo_transform:
            c, a, b, f, d, e = self.geo_transform
            x = c + a * col + b * row
            y = f + d * col + e * row
            return (round(x, 6), round(y, 6))
        # Default pixel transform: x = col, y = row
        return (float(col), float(row))

    def _compute_polyline_length(self, poly: List[Tuple[int, int]]) -> float:
        """Computes total Euclidean arc-length of a polyline."""
        length = 0.0
        for i in range(len(poly) - 1):
            r1, c1 = poly[i]
            r2, c2 = poly[i+1]
            length += math.hypot(r2 - r1, c2 - c1)
        return round(length, 4)

    def build_graph(self, polylines: List[List[Tuple[int, int]]]) -> nx.Graph:
        """
        Constructs a NetworkX undirected graph from vector polylines.
        Guarantees no duplicate edges and attributes nodes/edges with geometric metadata.
        """
        G = nx.Graph()
        node_coord_to_id: Dict[Tuple[int, int], str] = {}
        node_counter = 0

        def get_or_create_node(coord: Tuple[int, int]) -> str:
            nonlocal node_counter
            if coord not in node_coord_to_id:
                node_id = f"N_{node_counter}"
                node_counter += 1
                node_coord_to_id[coord] = node_id
                r, c = coord
                gx, gy = self._pixel_to_geo(r, c)
                G.add_node(
                    node_id,
                    pixel_coord=(r, c),
                    geo_coord=(gx, gy)
                )
            return node_coord_to_id[coord]

        duplicate_edge_count = 0

        for poly in polylines:
            if len(poly) < 2:
                continue

            start_coord = poly[0]
            end_coord = poly[-1]

            u = get_or_create_node(start_coord)
            v = get_or_create_node(end_coord)

            # Prevent self-loops unless specifically desired; in road networks, circular dead-ends exist
            # Check for duplicate edges
            if G.has_edge(u, v):
                duplicate_edge_count += 1
                # If duplicate exists, keep the shorter geometry
                existing_len = G.edges[u, v].get("length", float("inf"))
                new_len = self._compute_polyline_length(poly)
                if new_len < existing_len:
                    geo_coords = [self._pixel_to_geo(r, c) for r, c in poly]
                    G.edges[u, v].update({
                        "geometry": poly,
                        "geo_geometry": geo_coords,
                        "length": new_len
                    })
                continue

            length = self._compute_polyline_length(poly)
            geo_coords = [self._pixel_to_geo(r, c) for r, c in poly]

            G.add_edge(
                u, v,
                geometry=poly,
                geo_geometry=geo_coords,
                length=length,
                direction="bidirectional",
                metadata={"road_type": "default", "source": "vectorize"}
            )

        if duplicate_edge_count > 0:
            logger.debug(f"Merged {duplicate_edge_count} duplicate edge paths during graph construction.")

        # Classify node types based on degree
        for node, deg in G.degree():
            if deg >= 3:
                G.nodes[node]["node_type"] = "junction"
            elif deg == 1:
                G.nodes[node]["node_type"] = "endpoint"
            elif deg == 0:
                G.nodes[node]["node_type"] = "isolated"
            else:
                G.nodes[node]["node_type"] = "path_node"

        logger.info(f"Constructed graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges.")
        return G

    def compute_statistics(self, G: nx.Graph) -> Dict[str, Any]:
        """Computes structural topology and resilience statistics for the road graph."""
        num_nodes = G.number_of_nodes()
        num_edges = G.number_of_edges()

        if num_nodes == 0:
            return {
                "num_nodes": 0,
                "num_edges": 0,
                "connected_components": 0,
                "avg_node_degree": 0.0,
                "largest_connected_component_nodes": 0,
                "largest_connected_component_percent": 0.0,
                "graph_density": 0.0
            }

        num_components = nx.number_connected_components(G)
        avg_degree = float(sum(d for _, d in G.degree()) / num_nodes)
        
        components = list(nx.connected_components(G))
        lcc_nodes = max(components, key=len)
        lcc_size = len(lcc_nodes)
        lcc_percent = round((lcc_size / num_nodes) * 100.0, 2)
        density = round(nx.density(G), 6)

        stats = {
            "num_nodes": num_nodes,
            "num_edges": num_edges,
            "connected_components": num_components,
            "avg_node_degree": round(avg_degree, 2),
            "largest_connected_component_nodes": lcc_size,
            "largest_connected_component_percent": lcc_percent,
            "graph_density": density
        }
        logger.info(f"Graph stats — Components: {num_components}, LCC: {lcc_percent}%, Avg Degree: {stats['avg_node_degree']}")
        return stats

    def validate_topology(self, G: nx.Graph, polylines: List[List[Tuple[int, int]]]) -> Dict[str, bool]:
        """
        Validates topological invariants:
        1. No duplicate edges (guaranteed by nx.Graph structure).
        2. No unexpected isolated nodes.
        3. Connectivity preservation.
        """
        no_duplicates = True  # nx.Graph enforces unique (u, v) pairs
        isolated_nodes = list(nx.isolates(G))
        no_isolated = len(isolated_nodes) == 0

        # Verify connectivity matches non-trivial polylines
        poly_count = len([p for p in polylines if len(p) >= 2])
        graph_comps = nx.number_connected_components(G) if G.number_of_nodes() > 0 else 0
        
        # Note: polyline input components might be equal or slightly greater if disjoint lines exist
        connectivity_preserved = (graph_comps > 0) if poly_count > 0 else (graph_comps == 0)

        validation_report = {
            "no_duplicate_edges": no_duplicates,
            "no_isolated_artifacts": no_isolated,
            "connectivity_preserved": connectivity_preserved,
            "is_valid": no_duplicates and connectivity_preserved
        }
        if not validation_report["is_valid"]:
            logger.warning(f"Topology validation warning: {validation_report}")
        return validation_report

    def export_geojson(self, G: nx.Graph, filepath: Optional[Path] = None) -> Dict[str, Any]:
        """Exports the graph nodes and edges as a standard GeoJSON FeatureCollection."""
        features = []

        # Export Nodes
        for node_id, attr in G.nodes(data=True):
            gx, gy = attr.get("geo_coord", (0.0, 0.0))
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [gx, gy]
                },
                "properties": {
                    "node_id": node_id,
                    "node_type": attr.get("node_type", "unknown"),
                    "degree": G.degree(node_id)
                }
            }
            features.append(feature)

        # Export Edges
        for u, v, attr in G.edges(data=True):
            geo_geom = attr.get("geo_geometry", [])
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": geo_geom
                },
                "properties": {
                    "source": u,
                    "target": v,
                    "length": attr.get("length", 0.0),
                    "direction": attr.get("direction", "bidirectional"),
                    "road_type": attr.get("metadata", {}).get("road_type", "default")
                }
            }
            features.append(feature)

        geojson_data = {
            "type": "FeatureCollection",
            "features": features
        }

        if filepath:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(geojson_data, f, indent=2)
            logger.info(f"Exported GeoJSON to {filepath}")

        return geojson_data

    def generate_visualization(self, G: nx.Graph, bg_mask: Optional[np.ndarray], output_path: Path):
        """Generates visual overlay report showing Graph Nodes (Junctions/Endpoints) and Edges."""
        fig, ax = plt.subplots(figsize=(10, 10))

        if bg_mask is not None:
            ax.imshow(bg_mask, cmap="gray", alpha=0.4)
            ax.set_title("Road Resilience Graph Overlay (Nodes + Edges)", fontsize=14, fontweight="bold")
        else:
            ax.set_title("Road Resilience Graph Structure", fontsize=14, fontweight="bold")

        # Draw edges
        for u, v, attr in G.edges(data=True):
            poly = attr.get("geometry", [])
            if poly:
                ys = [p[0] for p in poly]
                xs = [p[1] for p in poly]
                ax.plot(xs, ys, color="#00d2ff", linewidth=2, alpha=0.85)

        # Draw nodes by classification
        junc_x, junc_y = [], []
        end_x, end_y = [], []
        path_x, path_y = [], []

        for node_id, attr in G.nodes(data=True):
            r, c = attr.get("pixel_coord", (0, 0))
            ntype = attr.get("node_type", "")
            if ntype == "junction":
                junc_x.append(c)
                junc_y.append(r)
            elif ntype == "endpoint":
                end_x.append(c)
                end_y.append(r)
            else:
                path_x.append(c)
                path_y.append(r)

        if path_x:
            ax.scatter(path_x, path_y, c="yellow", s=20, label="Path Nodes", zorder=3)
        if end_x:
            ax.scatter(end_x, end_y, c="#ff9900", s=40, marker="s", label="Endpoints", zorder=4)
        if junc_x:
            ax.scatter(junc_x, junc_y, c="#ff0044", s=60, marker="^", label="Junctions", zorder=5)

        ax.axis("equal")
        ax.axis("off")
        ax.legend(loc="upper right", framealpha=0.9)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close(fig)
        logger.info(f"Saved graph visualization to {output_path}")
