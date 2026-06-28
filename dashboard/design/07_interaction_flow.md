# Deliverable 7: ATLAS Interaction & Workflow Specification

This document maps user interactions to frontend state transitions, TanStack Query cache mutations, and FastAPI network requests.

---

## 1. Primary Operational Workflow Flowchart

```mermaid
sequenceDiagram
    autonumber
    actor User as GIS Commander
    participant HUD as Floating HUD / Dock
    participant Map as WebGL Canvas (Deck.gl)
    participant Store as Zustand / TanStack Query
    participant API as FastAPI Backend (/api/v1/)

    User->>HUD: Select View: "Graph Healing"
    HUD->>Store: Set activeView = "healing"
    Store->>API: POST /api/v1/graph/heal {max_search_radius: 150}
    API-->>Store: 200 OK (Healed GeoJSON + Explanations List)
    Store->>Map: Update WebGL Vector Layer (Render healed edges as green pulse)
    
    User->>Map: Click Healed Edge (ID: RH-001)
    Map->>Store: Set selectedEdgeId = "RH-001"
    Store->>HUD: Open Explainability XAI Inspector Panel
    HUD-->>User: Display Hybrid Cost Breakdown & Rationale text
```

---

## 2. Disaster Simulation & Decision Support Loop

```mermaid
stateDiagram-v2
    [*] --> Baseline: Hero City Grid Loaded
    Baseline --> TargetingDisaster: User draws Bounding Box on Map
    TargetingDisaster --> Simulating: Click "SIMULATE DISASTER"
    
    state Simulating {
        [*] --> POST_Disrupt: Send failure_fraction & bbox
        POST_Disrupt --> AwaitingResponse: Network Latency (<100ms)
        AwaitingResponse --> RenderDegraded: Update Map Red Severed Links
    }
    
    Simulating --> DecisionSupportActive: Return Recommended Repairs List
    DecisionSupportActive --> ReviewingPriority: Click Priority #1 Link
    ReviewingPriority --> MapHighlight: FlyTo Camera & Pulse Broken Route
    MapHighlight --> [*]
```

---

## 3. Debounced Parameter Slider Behavior

When a user drags a parameter slider (e.g., RDP Simplification Tolerance $\epsilon$ from 2.0m to 5.0m):
1. **Immediate Visual Feedback (0ms):** The local numerical counter updates instantly using `Roboto Mono` tabular figures.
2. **Debounce Timer (150ms):** Prevents spamming the REST API while the mouse button is actively dragged.
3. **Optimistic Map Fade (150ms):** Existing map polyline opacity drops to 0.5 to signal incoming spatial data recalculation.
4. **Network Commit:** `POST /api/v1/graph/construct` is dispatched. Upon response, the WebGL buffer swaps atomically with zero flicker.
