# Data Management

## Module: `datasets/`

**Owner**: AI/ML Engineer + Data Management  
**Status**: Awaiting Phase 2 (Problem Research)

## Structure

```
datasets/
├── raw/           # Original, unmodified data (never edited)
├── processed/     # Cleaned, normalized data ready for training
├── augmented/     # Augmented data (occlusion simulation, transforms)
└── README.md
```

## Data Governance

1. **Raw data is immutable** — Never modify files in `raw/`
2. **Provenance tracking** — Every processed dataset records its source and transformations
3. **Version control** — Large files use Git LFS or DVC, not direct commits
4. **Documentation** — Every dataset has metadata (source, license, format, statistics)
