# Artificial Intelligence & Computer Vision

## Project ATLAS — Route Resilience
### Knowledge Base Entry

> This page documents all AI/ML knowledge acquired during the project — model architectures evaluated, training strategies, evaluation metrics, and the scientific reasoning behind every selection.

---

## Problem Context

The AI module must perform **semantic segmentation of road networks from satellite imagery under occlusion conditions**. This is not standard road extraction — the system must reconstruct or infer road presence even when roads are partially or fully obscured.

---

## Model Architecture Candidates

> **Detailed comparison will be completed during Phase 2-5.** Below is the initial candidate list.

| Model | Type | Year | Key Strength | Key Weakness | Status |
|---|---|---|---|---|---|
| UNet | Encoder-Decoder | 2015 | Simple, proven baseline | Limited receptive field | To evaluate |
| UNet++ | Nested Encoder-Decoder | 2018 | Dense skip connections | Higher memory usage | To evaluate |
| DeepLabV3+ | Atrous Convolution | 2018 | Multi-scale features | Slower inference | To evaluate |
| SegFormer | Vision Transformer | 2021 | Efficient, no positional encoding | Requires more data | To evaluate |
| Mask2Former | Universal Segmentation | 2022 | State-of-the-art, flexible | Complex, heavy | To evaluate |
| HRNet | High-Resolution Network | 2019 | Maintains high-res throughout | Computationally expensive | To evaluate |
| SAM | Segment Anything | 2023 | Zero-shot generalization | Not optimized for roads | To evaluate |
| Swin Transformer | Hierarchical ViT | 2021 | Shifted window attention | Requires large pretraining | To evaluate |
| D-LinkNet | Dilated LinkNet | 2018 | Designed for roads | Less general | To evaluate |

---

## Evaluation Criteria for Model Selection

Each candidate will be evaluated against these criteria:

1. **Segmentation accuracy** — IoU, Dice coefficient on road datasets
2. **Occlusion robustness** — Performance degradation under synthetic occlusion
3. **Connectivity preservation** — Do extracted roads form connected networks?
4. **Inference speed** — Frames per second, critical for dashboard demo
5. **Training feasibility** — Can be trained within hackathon GPU/time constraints
6. **Memory footprint** — GPU VRAM requirements
7. **Transfer learning availability** — Pretrained weights on relevant domains
8. **Generalization** — Performance on unseen geographic regions

---

## Key Concepts

### Semantic Segmentation
Pixel-level classification of satellite imagery into road/non-road classes. Binary segmentation simplifies the problem but may lose multi-class information.

### Occlusion Recovery
The core challenge. Methods include:
- **Inpainting-based** — Predict road presence in occluded regions
- **Attention-based** — Learn contextual cues from surrounding road patterns
- **Temporal fusion** — Use multi-temporal imagery to see through transient occlusions
- **Topology-aware loss** — Loss functions that penalize connectivity breaks

### Loss Functions to Investigate
- Binary Cross-Entropy
- Dice Loss
- Focal Loss (for class imbalance)
- Connectivity Loss (topology-aware)
- Boundary Loss
- Combined / Compound losses

---

## Research Papers to Review

> **Populated during Phase 2.** Will include papers on:
> - Road extraction from satellite imagery
> - Occlusion handling in remote sensing
> - Topology-preserving segmentation
> - Graph neural networks for road networks

---

## Datasets

> **Assessed during Phase 2.** Candidate public datasets:
> - SpaceNet (roads challenge)
> - DeepGlobe Road Extraction
> - Massachusetts Roads
> - INRIA Aerial Image Labeling
> - ISRO-provided data (if any)

---

*This page is updated after every AI-related research finding, experiment, and decision.*
