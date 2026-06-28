# Project Folder Architecture

**Project**: ATLAS — Route Resilience
**Status**: APPROVED

> **Enterprise Justification**: This repository is structured like a deployable ISRO software product, not a chaotic 24-hour hackathon dump. Strict modularity ensures that the CV engineer, GIS engineer, and Frontend developer never create Git merge conflicts with each other.

---

## 1. Directory Tree & Rationale

```text
road-resilence/
├── ai/                      # AI Module
│   ├── models/              # Neural network definitions (SegFormer.py)
│   ├── loss/                # Custom topology losses (cldice.py)
│   └── train.py             # Training loop
├── architecture/            # HLD, LLD, and API specs (No code)
├── backend/                 # FastAPI Service
│   ├── routes/              # API endpoints
│   ├── core/                # Geometric intersection logic
│   └── main.py              # Server entrypoint
├── dashboard/               # Frontend Application
│   ├── src/components/      # React components (Map, Sidebar, Charts)
│   └── src/layers/          # Deck.gl custom rendering layers
├── datasets/                # Data Management
│   ├── raw/                 # Immutable source TIFFs
│   └── processed/           # Normalized tensors (Git ignored)
├── docs/                    # MDD, SRS, Timelines
├── gis/                     # Geospatial Utilities
│   └── preprocessing.py     # Rasterio tiling logic
├── graph/                   # Network Science Module
│   ├── construction.py      # Mask -> Graph + MST Healing
│   └── analysis.py          # Centrality computations
├── memory/                  # Technical Debt, ADRs, Logs
├── tests/                   # QA
│   ├── unit/                # Testing isolated functions
│   └── integration/         # Testing the API <-> Graph bridge
└── scripts/                 # Automation (e.g., precompute_city.py)
```

## 2. strict Modularity Rules
1. **No Circular Dependencies**: `backend/` can import from `graph/`, but `graph/` can **never** import from `backend/`.
2. **Immutable Raw Data**: Scripts can read from `datasets/raw/` but can never write to it.
3. **No Direct Database Access from UI**: The `dashboard/` must communicate exclusively through the `backend/` REST APIs.
