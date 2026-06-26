# Experiment Log Template

## EXP-XXXX: [Experiment Title]

---

### Metadata

| Field | Value |
|---|---|
| **Date** | YYYY-MM-DD |
| **Researcher** | |
| **Domain** | AI / Graph / GIS |
| **Related Requirement** | REQ-XXXX |
| **Related Decision** | DEC-XXXX |
| **Status** | Planned / Running / Complete / Failed |

---

### Hypothesis

What do you expect to happen and why?

### Objective

What specific question does this experiment answer?

### Setup

#### Model / Algorithm
- Architecture:
- Configuration:
- Pretrained weights:

#### Dataset
- Training set:
- Validation set:
- Test set:
- Augmentations applied:

#### Hardware
- GPU:
- RAM:
- Training time:

#### Hyperparameters

| Parameter | Value | Justification |
|---|---|---|
| Learning rate | | |
| Batch size | | |
| Epochs | | |
| Optimizer | | |
| Loss function | | |

---

### Results

#### Quantitative Metrics

| Metric | Value | Baseline | Δ |
|---|---|---|---|
| IoU | | | |
| Dice | | | |
| Precision | | | |
| Recall | | | |
| F1 | | | |
| Inference time (ms) | | | |
| GPU memory (GB) | | | |

#### Qualitative Observations

- Observation 1
- Observation 2

#### Failure Cases

Describe where the model/algorithm failed and why.

---

### Analysis

What do the results mean? Does the hypothesis hold?

### Engineering Impact

How does this experiment affect the project direction?

### Next Steps

What should be tried next based on these results?

### Artifacts

- [ ] Model checkpoint saved to `models/`
- [ ] Training logs saved to `experiments/`
- [ ] Visualizations saved to `experiments/`
- [ ] Research notebook updated
- [ ] Wiki updated
