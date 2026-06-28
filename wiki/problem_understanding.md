# Problem Understanding

## Project ATLAS — Route Resilience
### Knowledge Base Entry

> This page consolidates the complete understanding of the problem domain based on the Phase 2 Problem Statement Analysis. It is the single authoritative reference for what the project must solve and why.

---

## Official Problem Statement

**Competition**: Bharatiya Antariksh Hackathon 2026 (ISRO)  
**Problem ID**: PS-4  
**Title**: Route Resilience: Occlusion-Robust Road Extraction & Graph-Theoretic Criticality Analysis for Urban Mobility

**Core Challenge Description**: Modern urban centres, particularly rapidly expanding Indian metropolises (e.g., Bengaluru), face a dual challenge in spatial modelling: fragmentation and stagnation. Standard satellite-based road extraction often fails due to "spectral blindness" caused by tree canopies, building shadows and cloud cover. These "broken" masks are useless for real-world applications like disaster response or traffic simulation because they lack topological connectivity. This solution aims to bridge this gap by creating an end-to-end pipeline: first, using context-aware Deep Learning to "see through" occlusions, and second, transforming those masks into a mathematically continuous, weighted graph to identify systemic bottlenecks and simulate urban collapse scenarios.

---

## Problem Domain Decomposition

The problem requires a shift from pure "Computer Vision" to "Topology-Aware Computer Vision" and "Network Science".

### 1. Occlusion-Robust Road Extraction

**What**: Extract road networks from satellite imagery even when roads are partially or fully hidden by occlusions.

**Key Technical Insight**: Standard AI models suffer from "spectral blindness." We need context-aware Deep Learning that looks at the surrounding area to infer a road's presence through clouds, shadows, and trees.

**Metrics that Matter**: Pixel accuracy (mIoU) is not enough. The AI must be evaluated on `Connectivity (IoU on Graph)` and `Breaks / km`.

### 2. Graph-Theoretic Criticality Analysis

**What**: Construct a graph representation of the extracted road network and identify critical infrastructure.

**Key Technical Insight**: The graph must be "mathematically continuous." Because the AI mask might still be imperfect, an explicit "Topological Cleaning" step is required during graph construction.

**Centrality Metrics required**: Betweenness Centrality (BC), CFFBC, a-Centrality, and k-Core. These identify "systemic bottlenecks."

### 3. Route Resilience under Disruptions

**What**: Simulate urban collapse scenarios.

**Key Technical Insight**: Resilience is measured by tracking the "Network Connectivity" (specifically the Giant Component Size) as nodes/edges are disrupted in various scenarios.

---

## Engineering Analysis & Pipeline

The end-to-end pipeline must flow as follows:

1. **Multi-source Urban Data Ingestion** (Satellite primarily, extensible to Aerial/LiDAR).
2. **Context-Aware Deep Learning** (Occlusion-robust extraction producing a road mask).
3. **Road Graph Construction** (Vectorizing the mask into a graph structure).
4. **Topological Cleaning** (Bridging gaps, removing artifacts to ensure a mathematically continuous graph).
5. **Criticality Analysis** (Computing BC, k-Core, etc. to find bottlenecks).
6. **Urban Collapse Simulation** (Disruption scenarios vs Giant Component Size).

---

*This page is the distillation of the full analysis found in `research/problem_analysis/ps4_analysis.md`.*
