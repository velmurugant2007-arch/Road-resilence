# AI/ML Pipeline

## Module: `ai/`

**Owner**: AI/ML Engineer + Computer Vision Engineer  
**Status**: Awaiting Phase 7 (Implementation)

## Purpose

Semantic segmentation of road networks from satellite imagery, with specific focus on occlusion-robust extraction. This module produces binary road masks and confidence maps that feed into the Graph module.

## Structure

```
ai/
├── models/          # Model architecture definitions
├── training/        # Training scripts, configs, loss functions
├── inference/       # Inference pipeline
├── evaluation/      # Evaluation scripts and metrics
└── README.md
```

## Dependencies

- Receives: Satellite imagery tiles (from GIS module)
- Produces: Binary road masks, confidence maps
- Consumed by: Graph module (for network construction)

## Key References

- [AI Wiki](../wiki/ai.md)
- [AI Guide](../docs/ai_guide.md)
- [Experiment Template](../templates/experiment_template.md)
- [Model Evaluation Template](../templates/ai_model_evaluation_template.md)

---

*No code until Phase 7. Research and architecture must be completed first.*
