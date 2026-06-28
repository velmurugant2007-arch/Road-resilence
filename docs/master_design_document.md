# Master Design Document

## Project ATLAS — Route Resilience
### Bharatiya Antariksh Hackathon 2026 (ISRO) — PS-4
### Occlusion-Robust Road Extraction & Graph-Theoretic Criticality Analysis for Urban Mobility

---

**Document Version**: 0.2.0  
**Last Updated**: 2026-06-26  
**Status**: Phase 2 — Problem Research Complete  
**Classification**: Internal Engineering Document

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [System Overview](#3-system-overview)
4. [Requirements](#4-requirements)
5. [Architecture](#5-architecture)
6. [AI/ML Design](#6-aiml-design)
7. [Graph Intelligence Design](#7-graph-intelligence-design)
8. [GIS Processing Design](#8-gis-processing-design)
9. [Backend Design](#9-backend-design)
10. [Frontend/Dashboard Design](#10-frontendashboard-design)
11. [Data Management](#11-data-management)
12. [Testing Strategy](#12-testing-strategy)
13. [Deployment Strategy](#13-deployment-strategy)
14. [Innovation Register](#14-innovation-register)
15. [Risk Analysis](#15-risk-analysis)
16. [Appendices](#16-appendices)

---

## 1. Executive Summary

This document serves as the **single source of truth** for all engineering design decisions in the Route Resilience project. Every module, algorithm, interface, and architectural choice documented here traces to an official requirement or a clearly identified innovation.

The project addresses ISRO Problem Statement 4: developing a system that extracts road networks from satellite imagery under occlusion conditions, constructs graph-theoretic representations, and performs criticality analysis for urban mobility applications.

> **Current State**: Phase 2 (Problem Research) is complete. Requirements have been extracted and mapped. The engineering strategy shifts from pure CV to Topology-Aware CV and Network Science.
> 
> **Next Target**: [Milestone 1 Roadmap](project_roadmap.md) (Architecture & Mock Pipeline).

---

## 2. Problem Statement

Modern urban centres, particularly rapidly expanding Indian metropolises (e.g., Bengaluru), face a dual challenge in spatial modelling: fragmentation and stagnation. Standard satellite-based road extraction often fails due to "spectral blindness" caused by tree canopies, building shadows and cloud cover. These "broken" masks are useless for real-world applications like disaster response or traffic simulation because they lack topological connectivity. This solution aims to bridge this gap by creating an end-to-end pipeline: first, using context-aware Deep Learning to "see through" occlusions, and second, transforming those masks into a mathematically continuous, weighted graph to identify systemic bottlenecks and simulate urban collapse scenarios.

---

## 3. System Overview

> Populated during Phase 5 (Architecture).

---

## 4. Requirements

### 4.1 Requirement Traceability Matrix

| Req ID | Description | Source | Module | Priority |
|---|---|---|---|---|
| REQ-01 | Handle dense Indian urban environments | PS Sentence 1 | GIS / Data | High |
| REQ-02 | Occlusion-robust road extraction | PS Sentence 2 | AI | Critical |
| REQ-03 | Maximize topological connectivity | PS Sentence 3 | AI / Graph | Critical |
| REQ-04 | End-to-end processing pipeline | PS Sentence 4 | Backend / Sys | High |
| REQ-05 | Context-aware Deep Learning model | PS Sentence 4 | AI | Critical |
| REQ-06 | Mathematically continuous, weighted graph | PS Sentence 4 | Graph | Critical |
| REQ-07 | Systemic bottleneck identification | PS Sentence 4 | Graph | High |
| REQ-08 | Urban collapse scenario simulation | PS Sentence 4 | Graph | High |
| REQ-09 | Measure mIoU, Graph IoU, Breaks/km | PS Diagram | AI Eval | Medium |
| REQ-10 | Implement Topological Cleaning | PS Diagram | Graph | High |
| REQ-11 | Multiple Centrality Metrics (BC, k-Core, etc) | PS Diagram | Graph | High |
| REQ-12 | Giant Component Size tracking | PS Diagram | Graph | High |

---

## 5. Architecture

> Populated during Phase 5. References:
> - [High-Level Architecture](../architecture/high_level_architecture.md)
> - [Low-Level Architecture](../architecture/low_level_architecture.md)
> - [Data Flow](../architecture/data_flow.md)
> - [Technology Stack](../architecture/technology_stack.md)

---

## 6. AI/ML Design

> Populated during Phases 2-5. References:
> - [AI Wiki](../wiki/ai.md)
> - [AI Guide](ai_guide.md)
> - [Research Notebook](research_notebook.md)

---

## 7. Graph Intelligence Design

> Populated during Phases 2-5. References:
> - [Graph Theory Wiki](../wiki/graph_theory.md)
> - [Graph Theory Guide](graph_theory_guide.md)

---

## 8. GIS Processing Design

> Populated during Phases 2-5. References:
> - [GIS Wiki](../wiki/gis.md)
> - [GIS Guide](gis_guide.md)

---

## 9. Backend Design

> Populated during Phase 5.

---

## 10. Frontend/Dashboard Design

> Populated during Phase 5.

---

## 11. Data Management

> Populated during Phase 2-5.

---

## 12. Testing Strategy

> Populated during Phase 5. References:
> - [Testing Guide](testing_guide.md)

---

## 13. Deployment Strategy

> Populated during Phase 5. References:
> - [Deployment Guide](deployment_guide.md)

---

## 14. Innovation Register

> Cross-reference: [Future Ideas](../memory/future_ideas.md)

Innovations accepted for implementation:

| Innovation ID | Description | Domain | Judging Impact | Status |
|---|---|---|---|---|
| IDEA-0004 | Interactive Disruption Dashboard via click | Dashboard | High | Proposed |
| IDEA-0005 | Confidence-Weighted Routing | AI/Graph | High | Proposed |

---

## 15. Risk Analysis

> Cross-reference: [Risk Register](../memory/risks.md)

---

## 16. Appendices

- A. Glossary of Terms
- B. Reference Papers
- C. Technology Evaluation Matrices
- D. Meeting Notes Archive

---

*This is a living document. Updated after every significant design decision.*
