# ATLAS — Technical Debt Report
**Date**: 2026-06-28  
**Audit Milestone**: Pre-Phase 7.4 Implementation Audit  
**Status**: Active Register  

---

## 1. Overview
This report registers conscious architectural and implementation trade-offs made during Phases 7.1 through 7.3.4. In compliance with the 30-hour Bharatiya Antariksh Hackathon execution constraints, engineering prioritization favored deterministic feasibility, mathematical stability, and demo reliability over theoretical perfection.

---

## 2. Technical Debt Register

| Debt ID | Module | Title | Risk Impact | Priority | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TD-0001** | `graph/` (Pending) | Pre-computed "Hero City" Centrality | Live $O(VE)$ graph algorithms will crash or timeout during interactive demo evaluation. | **High** | Pre-compute offline graph metrics for Bengaluru; provide sandbox for single-tile live uploads. |
| **TD-0002** | `graph/` (Pending) | Heuristic MST Gap Bridging | Naive Euclidean joining may bridge roads across physical barriers (e.g., rivers without bridges). | **Medium** | Impose a strict maximum distance cutoff (`< 30m`) for topological healing. |
| **TD-0003** | `ai/models/` | Optical-Only Architecture (No SAR) | Model must infer road continuity under dense cloud cover without radar penetration data. | **Low** (Hackathon)<br>**High** (Prod) | Expose softmax probability confidence maps to dashboard to flag low-confidence imputed edges. |
| **TD-0004** | `ai/loss/` | Iterative Soft-Skeletonization Pooling | Approximating morphological thinning via 10 iterations of min/max pooling consumes extra VRAM. | **Low** | Prune forward evaluation when `cldice_weight == 0.0`; wrap GT operations in `no_grad()`. |
| **TD-0005** | `gis/loader.py` | Single-Node Memory Mapping | Massive GeoTIFF ingestion relies on local filesystem OS memory mapping rather than distributed tiling. | **Low** | Sufficient for single-GPU RTX 4050 hackathon constraints. Long-term: migrate to Cloud Optimized GeoTIFF (COG) byte-streaming. |

---

## 3. Deep-Dive Analysis of AI Implementation Debt

### TD-0004: Soft-Skeletonization VRAM Overhead
- **Context**: Standard centerline extraction (Zhang-Suen thinning) uses discrete integer checks that block backpropagation gradients. Our custom `SoftSkeletonize` module achieves full differentiability using iterative morphological pooling operations.
- **Cost**: Each iteration constructs pooling activation tensors in the PyTorch autograd computational graph. At 10 iterations, this increases memory consumption by approximately 18% during training passes.
- **Remediation Status**: Mitigated during the pre-Phase 7.4 audit by short-circuiting inactive loss evaluation and isolating static target masks.

### TD-0005: Local GeoTIFF Tiling Dependency
- **Context**: `GeoTIFFLoader` and `GeoTiler` read imagery directly from disk windows into RAM.
- **Cost**: While highly efficient for local 512x512 tile extraction, it assumes fast NVMe local storage and cannot scale out-of-the-box to multi-node S3 bucket distributed training without rasterio VSI wrappers (`/vsis3/`).
- **Remediation Status**: Documented for post-hackathon cloud scaling.

---

## 4. Governance Compliance
All documented debt items align with the frozen **Master Design Document (MDD)** and **Software Requirements Specification (SRS)**. No architectural redesigns are required to proceed with Phase 7.4.
