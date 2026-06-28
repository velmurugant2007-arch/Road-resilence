# Success Metrics

**Purpose**: To define project success holistically from a judging and engineering perspective, ensuring we are not just chasing technical metrics (like mIoU) at the expense of overall project viability.

---

## 1. Technical Success
**Focus**: The underlying mathematical and AI correctness.
- [ ] AI model achieves `Connectivity (IoU on Graph)` > 0.80.
- [ ] AI model achieves `Breaks / km` < 5.0.
- [ ] Graph module successfully bridges 95% of sub-30m false gaps.
- [ ] Centrality algorithms exactly match standard NetworkX mathematical baselines.

## 2. Engineering Success
**Focus**: The stability and architecture of the system.
- [ ] System handles "Hero City" pre-computation without memory overflows.
- [ ] Live Dashboard API responses for disruption simulations return in < 200ms.
- [ ] Zero unhandled exceptions or crashes during the end-to-end pipeline execution.
- [ ] Codebase strictly adheres to defined Python Coding Standards and typing.

## 3. Documentation Success
**Focus**: The ISRO-grade traceability and professional presentation.
- [ ] Every major architectural choice is documented via an ADR.
- [ ] 100% traceability from REQ-XX to codebase implementation.
- [ ] Master Design Document is fully populated and accurately reflects the final system.
- [ ] Risk Register and Technical Debt log are up-to-date at project submission.

## 4. Innovation Success
**Focus**: Differentiating the project from the 90% of generic submissions.
- [ ] At least two Tier-1 innovations from the Innovation Matrix are successfully implemented.
- [ ] The dashboard includes a unique, visually impressive interaction (e.g., Bounding Box Disruption).

## 5. Presentation Success
**Focus**: The 5-minute hackathon pitch and demo.
- [ ] The live demo requires zero loading bars for graph calculations (Zero-Latency MVP).
- [ ] The presentation clearly contrasts "Standard AI" vs "Topology-Aware AI".
- [ ] Judges are able to directly interact with the dashboard without causing failures.

## 6. Deployment Success
**Focus**: Post-hackathon viability.
- [ ] The repository includes a `docker-compose.yml` that stands up the entire environment with one command.
- [ ] The codebase structure clearly separates research notebooks from production pipeline code.
