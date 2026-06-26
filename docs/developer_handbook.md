# Developer Handbook

## Project ATLAS — Route Resilience
### Bharatiya Antariksh Hackathon 2026 (ISRO) — PS-4

---

## Welcome

This handbook is the onboarding guide for anyone contributing to the Route Resilience project. It covers project philosophy, repository navigation, workflows, and conventions.

---

## 1. Project Philosophy

- **Research before implementation** — Understand the problem completely before writing code
- **Documentation-code parity** — Every code change has a corresponding documentation update
- **Traceability** — Every feature traces to a requirement or documented innovation
- **Quality over speed** — ISRO-grade standards throughout
- **No hallucination** — If uncertain, investigate; if still uncertain, say so

---

## 2. Repository Navigation

| Directory | Purpose | When to Use |
|---|---|---|
| `docs/` | Engineering documentation | Reading guides, updating design docs |
| `research/` | Research artifacts | Adding research findings |
| `architecture/` | Architecture decisions | Viewing/updating design |
| `memory/` | Project memory | After ANY significant action |
| `wiki/` | Knowledge base | Looking up domain knowledge |
| `ai/` | AI/ML pipeline | AI model development |
| `graph/` | Graph intelligence | Graph algorithm development |
| `gis/` | GIS processing | Spatial data handling |
| `backend/` | Backend services | API and service development |
| `frontend/` | Frontend application | UI development |
| `dashboard/` | Visualization dashboard | Dashboard components |
| `datasets/` | Data management | Dataset handling |
| `tests/` | Test suites | Writing and running tests |
| `templates/` | Document templates | Starting new documents |
| `config/` | Configuration | Environment and settings |
| `scripts/` | Utility scripts | Automation and helpers |

---

## 3. Workflow: Making Changes

1. **Check memory** — Review `memory/decisions.md` and relevant wiki pages
2. **Create branch** — Follow naming convention in [CONTRIBUTING.md](../.github/CONTRIBUTING.md)
3. **Implement** — Write code following [Coding Standards](coding_standards.md)
4. **Document** — Update relevant docs, wiki, and memory files
5. **Test** — Run relevant test suites
6. **Self-review** — Complete [Review Checklist](../templates/review_checklist.md)
7. **Pull request** — Use [PR template](../.github/PULL_REQUEST_TEMPLATE.md)

---

## 4. Updating Project Memory

After every significant action, update the relevant memory files:

| Action | Files to Update |
|---|---|
| Made a design decision | `memory/decisions.md`, `memory/daily_log.md` |
| Completed a task | `memory/progress.md`, `memory/daily_log.md` |
| Discovered a risk | `memory/risks.md` |
| Made an assumption | `memory/assumptions.md` |
| Had a new idea | `memory/future_ideas.md` |
| Learned something | `memory/lessons_learned.md` |
| Changed architecture | `memory/architecture_history.md`, `memory/decisions.md` |

---

## 5. Key References

- [Master Design Document](master_design_document.md) — Single source of truth
- [Architecture Handbook](architecture_handbook.md) — Architecture philosophy
- [Coding Standards](coding_standards.md) — Code conventions
- [Testing Guide](testing_guide.md) — Testing approach
- [Contributing Guidelines](../.github/CONTRIBUTING.md) — Git workflow

---

*This handbook is updated as project conventions evolve.*
