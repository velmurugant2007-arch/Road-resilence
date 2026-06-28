# AI Architecture Document

**Project**: ATLAS — Route Resilience
**Status**: APPROVED (Post-CER Revisions)

---

## 1. Objective
Select the optimal deep learning architecture for semantic road extraction under severe occlusion (clouds, shadows, trees) while maximizing topological continuity.

## 2. Model Comparison Matrix
*(Summary)*
- **U-Net / DeepLabV3+**: Rejected (Local receptive fields fail on massive clouds).
- **Mask2Former / SAM**: Rejected (Too heavy/slow for hackathon retraining).
- **SegFormer (MiT-B2/B3)**: **SELECTED**. Global receptive field via Transformers, highly robust to occlusions, manageable training overhead.

## 3. Topology-Aware Loss Function (Differentiable)
Standard clDice uses discrete skeletonization (Zhang-Suen), which breaks backpropagation. We employ **Soft-Skeletonization** (iterative min/max pooling) within the PyTorch graph to ensure the clDice loss gradients flow back smoothly into the SegFormer encoder.

## 4. Confidence Calibration (Validation Gate)
Before the AI passes its output to the Graph Healing module, the probability map's reliability must be validated. If the model is overconfident on false predictions, the Hybrid Cost Function will bridge roads incorrectly.

- **Calibration Metric**: We will evaluate the **Expected Calibration Error (ECE)**. A well-calibrated model ensures that a pixel with an 80% softmax confidence is actually correct 80% of the time.
- **Platt Scaling / Temperature Scaling**: If the SegFormer outputs highly polarized predictions (mostly 0.99 or 0.01), we will apply Temperature Scaling to smooth the logits. This ensures the *AI Confidence Integral* $P(e_{uv})$ used in the Graph Healing's Hybrid Cost Function accurately reflects true uncertainty under clouds, rather than blindly committing to hallucinated connections.
