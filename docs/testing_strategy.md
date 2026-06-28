# Testing Strategy

**Project**: ATLAS — Route Resilience
**Status**: APPROVED

---

## 1. Unit Testing (`tests/unit/`)
Tests the smallest components of the system in isolation.
- **AI Module**: Assert that the SegFormer outputs exactly a $1 \times 512 \times 512$ probability matrix with values bounded $[0,1]$.
- **Graph Module**: Assert that the Zhang-Suen algorithm reduces a 3-pixel wide line to exactly 1-pixel.
- **GIS Module**: Assert that the normalizer prevents `NaN` or negative values.

## 2. Graph Validation (The Core Mathematical Test)
Because mathematical correctness is our core differentiator, graph construction is tested heavily:
- **Gap Bridging Test**: Create a synthetic 100x100 matrix with a straight line missing 5 pixels in the middle. Assert that `heal_graph()` successfully creates a continuous path.
- **Centrality Test**: Manually create a 5-node star graph. Assert that the BC algorithm perfectly identifies the center node with the highest score, matching theoretical manual calculations exactly.

## 3. Integration Testing (`tests/integration/`)
Tests the handoffs between decoupled modules.
- **Pipeline Test**: Feed a mock GeoTIFF into the GIS module $\rightarrow$ AI Module $\rightarrow$ Graph Module. Assert that the final output is a valid NetworkX graph with > 0 nodes.
- **API Simulation Test**: Send a mock bounding box to the `/api/v1/simulation/disrupt` endpoint. Assert it returns HTTP 200 and the returned graph has exactly the expected number of nodes removed.

## 4. Model Testing (AI Evaluation)
- **Metrics**: `mIoU`, `Precision`, `Recall`, `clDice`.
- **Hold-Out Set**: Tested exclusively on a secondary Indian city (e.g., Mumbai) that the model has never seen, ensuring it didn't just overfit the spatial layout of the training city.

## 5. Dashboard & UI Testing
- **Framework**: Cypress.
- **Flows**: Simulate a user clicking the "Draw Box" tool, drawing a square, clicking "Execute", and asserting that the DOM updates the "Resilience Score" element correctly.

## 6. Stress Testing
- **API Load**: Use `Locust` to hit the `/baseline` endpoint with 100 concurrent requests to ensure the cached memory strategy holds up without OOM errors.
- **Graph Size**: Feed a 500,000 node graph into the backend simulation engine and assert that the bounding box intersection and sub-graph extraction completes in $<500ms$.
