# Contributing to Route Resilience

## Engineering Philosophy

This project follows ISRO-grade engineering standards. Every contribution must be:

1. **Traceable** — Maps to an official requirement or documented innovation
2. **Justified** — Includes written rationale for design decisions
3. **Documented** — Updates relevant documentation alongside code
4. **Tested** — Includes appropriate test coverage
5. **Reviewed** — Passes self-review checklist before requesting peer review

---

## Branch Strategy

```
main                    Production-ready releases
├── develop             Integration branch for ongoing work
│   ├── feature/*       New features (e.g., feature/road-segmentation)
│   ├── research/*      Research experiments (e.g., research/unet-comparison)
│   ├── fix/*           Bug fixes (e.g., fix/graph-connectivity)
│   ├── docs/*          Documentation updates (e.g., docs/api-reference)
│   └── experiment/*    ML experiments (e.g., experiment/deeplabv3-training)
└── release/*           Release candidates (e.g., release/v0.2.0)
```

### Branch Naming Convention

- `feature/<module>-<description>` — e.g., `feature/ai-road-extraction`
- `research/<topic>` — e.g., `research/occlusion-recovery-methods`
- `fix/<module>-<description>` — e.g., `fix/graph-disconnected-components`
- `docs/<topic>` — e.g., `docs/architecture-diagrams`
- `experiment/<model>-<description>` — e.g., `experiment/segformer-b3-training`

### Branch Rules

- `main` requires pull request with at least one approval
- `develop` is the default working branch
- All feature branches merge into `develop`
- Only tested, documented `develop` merges into `main`
- Never force-push to `main` or `develop`

---

## Commit Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | Description |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `research` | Research finding or analysis |
| `refactor` | Code restructuring |
| `test` | Adding or updating tests |
| `build` | Build system or dependency changes |
| `ci` | CI/CD configuration |
| `perf` | Performance improvement |
| `chore` | Maintenance tasks |
| `experiment` | ML experiment results |

### Scopes

`ai`, `graph`, `gis`, `backend`, `frontend`, `dashboard`, `api`, `docs`, `infra`, `data`, `memory`

### Examples

```
feat(ai): implement UNet++ road segmentation pipeline
research(graph): complete betweenness centrality benchmark
docs(architecture): add high-level system architecture diagram
fix(gis): correct CRS transformation for WGS84 to UTM
experiment(ai): SegFormer-B3 achieves 0.87 IoU on test set
```

---

## Pull Request Process

1. **Self-Review** — Complete the [review checklist](../templates/review_checklist.md) before opening a PR
2. **Documentation** — Update all affected documentation
3. **Memory** — Update relevant files in `memory/` (decisions, progress, daily log)
4. **Tests** — Include or update tests as appropriate
5. **Traceability** — Reference the requirement or issue in the PR description
6. **Description** — Explain what changed, why, and what alternatives were considered

---

## Versioning

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** — Breaking architectural changes
- **MINOR** — New features or significant additions
- **PATCH** — Bug fixes, documentation updates, refinements

Pre-release tags: `-alpha`, `-beta`, `-rc.N`

---

## Code Review Criteria

Reviewers should verify:

- [ ] Solves a real, documented problem
- [ ] Traces to a requirement or innovation
- [ ] Engineering decision is justified in writing
- [ ] Documentation is updated
- [ ] Tests are included and pass
- [ ] No hardcoded values without explanation
- [ ] Error handling is appropriate
- [ ] Performance implications are considered
- [ ] An ISRO scientist would approve this
