# Assumptions Register

## Project ATLAS — Route Resilience
### Bharatiya Antariksh Hackathon 2026 (ISRO) — PS-4

> This register documents all assumptions made during the project. Each assumption is tracked with its validation status, impact if incorrect, and mitigation strategy. Updated continuously.

---

## Assumption Format

```
### ASM-XXXX: [Assumption Statement]

- **Date Recorded**: YYYY-MM-DD
- **Phase**: [Phase name]
- **Status**: Unvalidated / Validated / Invalidated
- **Validation Method**: How this will be confirmed or refuted
- **Impact if Wrong**: What breaks if this assumption is incorrect
- **Mitigation**: Fallback plan
```

---

## Assumptions

### ASM-0001: The problem statement focuses on satellite imagery road extraction under occlusion

- **Date Recorded**: 2026-06-26
- **Phase**: Phase 1 — Workspace Initialization
- **Status**: Unvalidated (awaiting official problem statement upload)
- **Validation Method**: Direct comparison against the official ISRO problem statement document
- **Impact if Wrong**: Entire architecture may need restructuring; AI model selection may change
- **Mitigation**: Modular architecture design that can adapt to revised scope

### ASM-0002: The competition expects both road extraction (CV) and graph-theoretic analysis (network science)

- **Date Recorded**: 2026-06-26
- **Phase**: Phase 1 — Workspace Initialization
- **Status**: Unvalidated
- **Validation Method**: Problem statement analysis in Phase 2
- **Impact if Wrong**: One entire engineering module may be unnecessary
- **Mitigation**: Separate AI and Graph modules to allow independent scoping

### ASM-0003: Standard satellite imagery (RGB, possibly multispectral) will be provided or publicly available

- **Date Recorded**: 2026-06-26
- **Phase**: Phase 1 — Workspace Initialization
- **Status**: Unvalidated
- **Validation Method**: Dataset examination in Phase 2
- **Impact if Wrong**: May need to source or synthesize satellite imagery
- **Mitigation**: Identify public satellite imagery datasets (SpaceNet, DeepGlobe, INRIA) as fallbacks

### ASM-0004: GPU access is available for model training

- **Date Recorded**: 2026-06-26
- **Phase**: Phase 1 — Workspace Initialization
- **Status**: Unvalidated
- **Validation Method**: Hardware assessment
- **Impact if Wrong**: Must use lightweight models or pretrained weights only
- **Mitigation**: Select models that can be fine-tuned on consumer GPUs; prepare CPU-only inference pipeline

---

*Additional assumptions will be recorded as they arise during research and implementation.*
