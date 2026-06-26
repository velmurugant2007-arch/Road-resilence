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

*Next decisions will be recorded as they occur in subsequent phases.*
