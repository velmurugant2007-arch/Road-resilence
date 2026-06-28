# Decision Register

## Project ATLAS — Route Resilience
### Bharatiya Antariksh Hackathon 2026 (ISRO) — PS-4

> This register records every significant engineering decision made during the project lifecycle. Each entry includes the context, alternatives evaluated, selection rationale, and traceability to requirements. This document is updated after every decision point.

---

## Decision Format

Each decision follows this structure:

```
### DEC-XXXX: [Title]

- **Date**: YYYY-MM-DD
- **Phase**: [Phase number and name]
- **Domain**: [AI / Graph / GIS / Backend / Frontend / Architecture / Infra]
- **Status**: Proposed / Accepted / Superseded / Rejected

**Context**: Why this decision was needed.

**Alternatives Considered**:
1. [Alternative A] — [Pros/Cons]
2. [Alternative B] — [Pros/Cons]

**Decision**: What was decided.

**Rationale**: Why this was selected over alternatives.

**Consequences**: Expected impact of this decision.

**Traceability**: [Requirement ID or INNOVATION]
```

---

## Decisions

### DEC-0001: Repository Structure and Engineering Workflow

- **Date**: 2026-06-26
- **Phase**: Phase 1 — Workspace Initialization
- **Domain**: Architecture / Infrastructure
- **Status**: Accepted

**Context**: The project requires a professional engineering workspace that enforces research-first policy, documentation-code parity, requirement traceability, and ISRO-grade standards. The repository must support 12 project phases and multiple engineering domains (AI, Graph Theory, GIS, Backend, Frontend, Dashboard).

**Alternatives Considered**:
1. **Flat structure** — All code in root directories. Rejected: does not scale, violates separation of concerns, impossible to enforce traceability.
2. **Monorepo with packages** — npm/pip workspaces. Rejected: premature for hackathon context, adds tooling complexity without clear benefit at this scale.
3. **Domain-driven directory structure** — Directories organized by engineering domain with cross-cutting concerns (memory, wiki, docs, templates) as separate top-level folders. Selected.

**Decision**: Adopt a domain-driven directory structure with 30+ directories, organized by engineering domain. Cross-cutting concerns (documentation, memory, wiki, templates, architecture) are first-class top-level directories.

**Rationale**: This structure maps directly to the engineering teams identified in the project constitution. Each directory has clear ownership, purpose, and conventions. The memory and wiki systems provide persistent context that survives individual sessions. The template library enforces consistency across all deliverables.

**Consequences**:
- Every file has a clear home
- New contributors can navigate the repository intuitively
- Documentation and code live close together but are clearly separated
- The repository can grow beyond the hackathon without restructuring

**Traceability**: Project Constitution Rules 6, 7, 8

---

### DEC-0002: Git Branch Strategy

- **Date**: 2026-06-26
- **Phase**: Phase 1 — Workspace Initialization
- **Domain**: Infrastructure
- **Status**: Accepted

**Context**: Need a branching strategy that supports parallel work across research, implementation, and documentation while maintaining stability.

**Alternatives Considered**:
1. **GitFlow** — Full GitFlow with hotfix branches. Rejected: too heavyweight for team size, hotfix branches unnecessary for hackathon.
2. **Trunk-based development** — All commits to main. Rejected: too risky without CI/CD maturity, no isolation for experiments.
3. **Modified GitFlow** — main/develop with feature/research/experiment branches. Selected.

**Decision**: Modified GitFlow with `main` (stable), `develop` (integration), and typed branches (`feature/*`, `research/*`, `experiment/*`, `fix/*`, `docs/*`).

**Rationale**: Provides stability (main is always releasable), experimentation safety (research and experiment branches), and clear categorization of work types. The `research/*` and `experiment/*` branch types are specifically designed for ML research workflows where many experiments may not merge.

**Consequences**:
- Clear separation between stable and experimental work
- Research experiments can be tracked without polluting the main codebase
- Branch naming convention enables automated categorization

**Traceability**: Project Constitution Rule 9 (Quality over Speed)

---

### DEC-0003: Adoption of Topology-Aware AI Evaluation

- **Date**: 2026-06-26
- **Phase**: Phase 2 — Problem Research
- **Domain**: AI / Evaluation
- **Status**: Accepted

**Context**: The official problem statement explicitly faults standard AI for producing "broken masks" and the diagrams specify evaluating via "Connectivity (IoU on Graph)" and "Breaks / km".

**Alternatives Considered**:
1. **Standard CV Evaluation** — Relying purely on Pixel Accuracy, mIoU, and F1 score. Rejected: Doesn't align with the problem statement's core complaint about topological connectivity.
2. **Topology-Aware Evaluation** — Implementing custom metrics (Graph IoU, Breaks/km) alongside mIoU to select the best model. Selected.

**Decision**: The AI module will be evaluated primarily on topological continuity metrics (`Connectivity (IoU on Graph)`, `Breaks / km`), with standard mIoU acting as a secondary baseline metric.

**Rationale**: This directly answers the problem statement's requirement to overcome "fragmentation" and ensures the AI output is actually useful for the downstream Graph module.

**Consequences**:
- Requires custom metric implementation during the training/evaluation phase.
- May lead us to choose a model with slightly lower mIoU but better connectivity.

**Traceability**: REQ-03, REQ-09

---

### DEC-0004: Two-Stage Graph Construction

- **Date**: 2026-06-26
- **Phase**: Phase 2 — Problem Research
- **Domain**: Graph Theory
- **Status**: Accepted

**Context**: Even with occlusion-robust AI, predictions will not be perfectly continuous. The problem statement demands a "mathematically continuous" graph and the diagram explicitly requires a "Topological Cleaning" step.

**Alternatives Considered**:
1. **Direct Translation** — Simply converting the AI mask pixels to nodes/edges. Rejected: Leaves disconnections that break centrality analysis.
2. **Two-Stage Construction** — Stage 1: Vectorize raw mask to graph. Stage 2: Topological Cleaning (bridge gaps, prune spurs) to enforce continuity. Selected.

**Decision**: Implement a two-stage Graph Construction pipeline involving explicit Topological Cleaning.

**Rationale**: Mathematically guarantees a continuous graph (or at least maximizes the Giant Component Size) before feeding it into the Centrality and Resilience analysis engines.

**Consequences**:
- Graph module requires advanced topology-healing algorithms (e.g., MST heuristic gap bridging).

**Traceability**: REQ-06, REQ-10

---

*Next decisions will be recorded as they occur in subsequent phases.*
