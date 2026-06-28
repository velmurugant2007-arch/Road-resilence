# Project Timeline

**Project**: ATLAS — Route Resilience
**Status**: APPROVED

> **Hackathon Reality Check**: This timeline compresses a standard 3-month ISRO R&D lifecycle into the constrained timeline of a hackathon. Strict adherence to gates is mandatory to prevent feature creep.

---

## 1. Milestone 1: Foundation & Architecture (Pre-Hackathon / Day 1)
- **Objective**: Complete understanding, lock architecture, setup CI/CD.
- **Tasks**:
  - Analyze problem statement & official videos.
  - Generate SRS, MDD, LLD, and Database specs.
  - Setup GitHub, standardizing linting and testing.
- **Acceptance Criteria**: Design Readiness Report states "APPROVED".
- **Review Gate**: Architecture Review Board (CDR).

## 2. Milestone 2: The "Hero City" Data Pipeline
- **Objective**: Establish the static MVP pipeline.
- **Tasks**:
  - Download SpaceNet/OSM data for a single Indian city.
  - Run offline semantic segmentation (using a baseline pre-trained model).
  - Run offline graph vectorization and compute $O(VE)$ centrality.
  - Serialize to GeoJSON.
- **Acceptance Criteria**: A 15MB `hero_city.geojson` file exists with all node/edge attributes.
- **Risk Assessment**: If AI fails, use raw OSM data to generate the graph so the dashboard team is unblocked.

## 3. Milestone 3: Interactive Dashboard MVP
- **Objective**: Build the visual wow-factor.
- **Tasks**:
  - Build FastAPI Backend to serve the GeoJSON.
  - Build React + Deck.gl frontend.
  - Implement Bounding Box intersection algorithm on the backend.
- **Acceptance Criteria**: A user can draw a box on the UI, and the map updates within 500ms showing the disrupted network.
- **Review Gate**: UI/UX Review.

## 4. Milestone 4: AI Topological Fine-Tuning
- **Objective**: Replace the baseline model with the topology-aware model.
- **Tasks**:
  - Implement `clDice` loss.
  - Train SegFormer with synthetic cloud augmentations.
  - Replace the old GeoJSON with the newly predicted AI output.
- **Acceptance Criteria**: Model achieves target `clDice` score on the validation set.
- **Risk Assessment**: If training diverges or takes too long, we fall back to the Milestone 2 baseline model. The demo is safe.

## 5. Milestone 5: Presentation Polish
- **Objective**: Prepare for ISRO judging.
- **Tasks**:
  - Finalize all markdown documentation (ADRs, Tech Debt, Risk Register).
  - Record a 2-minute flawless fallback video in case live wifi fails.
  - Rehearse the "Standard AI vs Topology AI" talking points.
- **Acceptance Criteria**: Pitch deck matches the system capabilities perfectly.
- **Testing Gate**: End-to-end dry run of the 5-minute presentation.
