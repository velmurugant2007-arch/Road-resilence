# Dashboard Design

**Project**: ATLAS — Route Resilience
**Status**: APPROVED (Post-CER Revisions)

---

## 1. UI Philosophy
The dashboard is the only thing the hackathon judges will interact with. It must be brutally fast, scientifically authoritative, and visually stunning (Dark Mode, neon highlights, fluid 60fps animations). 

## 2. Global Layout
- **Left Panel (350px)**: Control Panel & Decision Support.
- **Center Area (Fluid)**: The WebGL Interactive Map.
- **Top Bar (60px)**: Title, ISRO Logo, Global Status Indicator (Healthy vs Degraded).

## 3. The Interactive Map (Deck.gl / Mapbox)
- **Base Map**: Dark satellite style.
- **Graph Layer**: Healthy roads (Cyan), Degraded/Bottlenecked (Red/Orange).
- **Explainability Layer**: Clicking any node or edge instantly renders an overlay detailing *why* it holds its specific Betweenness Centrality score (e.g., "Connects Northern Suburbs directly to Airport").

## 4. Control Panel (Left Sidebar)

### Section A: Visualization Toggles & Disasters
- `[Toggle]` Base Satellite vs AI Probability Mask vs Healed Graph.
- `[Simulation]` Draw Polygon (Flood), Draw Circle (Earthquake).
- `[Execute]` Trigger Disruption.

### Section B: Decision Support Panel (Post-Disruption)
Replacing a generic "Top 3 Roads" list, this advanced panel answers the ultimate judge question: *"What do we do now?"*
- **Critical Vulnerability Ranking**: Lists the top targets for emergency repair.
- **Why is this critical?**: (e.g., "Node 452 is now the sole bridge connecting the East-West axis.")
- **Estimated Impact of Repair**: Predicts the $\Delta$ Resilience Score if that specific road is fixed.
- **Alternative Routing**: Highlights secondary paths traffic will take while the road is down.

### Section C: Live Resilience Metrics
- **Network Health**: Progress bar (e.g., drops from 100% to 62%).
- **Nodes/Edges Lost**: Integer count.
- **Overall Resilience Score**: Calculated ratio $0.0 - 1.0$.

## 5. GeoJSON Contingency
The map initially loads via a massive GeoJSON payload. We will monitor First Contentful Paint (FCP) and heap size. If performance degrades beneath 30fps during panning, we will seamlessly swap the backend to serve MVT Vector Tiles.
