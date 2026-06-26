# Problem Understanding

## Project ATLAS — Route Resilience
### Knowledge Base Entry

> This page consolidates the complete understanding of the problem domain. It is the single authoritative reference for what the project must solve and why.

---

## Official Problem Statement

**Competition**: Bharatiya Antariksh Hackathon 2026 (ISRO)  
**Problem ID**: PS-4  
**Title**: Route Resilience: Occlusion-Robust Road Extraction & Graph-Theoretic Criticality Analysis for Urban Mobility

> ⚠️ **Status**: Awaiting official problem statement upload. This page will be fully populated during Phase 2: Problem Research.

---

## Problem Domain Decomposition

The problem title suggests three distinct technical challenges:

### 1. Occlusion-Robust Road Extraction

**What**: Extract road networks from satellite imagery even when roads are partially or fully hidden by occlusions.

**Types of Occlusion** (anticipated):
- Cloud cover (partial and full)
- Tree canopy / dense vegetation
- Building shadows
- Atmospheric haze
- Temporal occlusion (construction, flooding)

**Technical Domain**: Computer Vision, Semantic Segmentation, Remote Sensing

### 2. Graph-Theoretic Criticality Analysis

**What**: Construct a graph representation of the extracted road network and identify critical infrastructure — nodes and edges whose removal would most severely impact network connectivity and traffic flow.

**Technical Domain**: Graph Theory, Network Science, Topology Analysis

### 3. Urban Mobility

**What**: Apply the analysis to real-world urban mobility scenarios — travel time estimation, alternative route identification, and infrastructure vulnerability assessment.

**Technical Domain**: Transportation Engineering, GIS, Spatial Analysis

---

## Sentence-by-Sentence Analysis

> **Populated during Phase 2** after the official problem statement is uploaded. Each sentence will be analyzed for:
> - Original statement
> - Simple explanation
> - Technical meaning
> - Hidden requirements
> - Implementation requirements
> - Research opportunities
> - Possible risks
> - Innovation ideas
> - Related modules
> - Priority

---

## Evaluation Criteria

> **Populated during Phase 2.** Expected criteria domains:
> - Road extraction accuracy (IoU, Dice, Precision, Recall)
> - Occlusion recovery quality
> - Graph connectivity metrics
> - Criticality analysis correctness
> - Visualization quality
> - Innovation
> - Presentation quality
> - Documentation

---

## Key Questions to Answer in Phase 2

1. What specific satellite imagery data is provided or expected?
2. What spatial resolution and spectral bands are available?
3. What geographic scope (urban, rural, mixed)?
4. What are the specific evaluation metrics and their weights?
5. Is there a predefined workflow or is the approach open?
6. What output formats are expected?
7. Are there constraints on tools, libraries, or platforms?
8. What is the judging format (live demo, presentation, documentation)?

---

*This page is updated continuously as new understanding emerges.*
