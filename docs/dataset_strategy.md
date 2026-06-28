# Dataset Strategy

**Project**: ATLAS — Route Resilience
**Status**: APPROVED

---

## 1. Dataset Acquisition Plan
The ISRO problem statement requires extracting roads in urban Indian environments under occlusion. Since a perfectly curated dataset for this specific scenario does not exist openly, we will build a composite dataset.

- **Primary Source**: SpaceNet 3 (Road Network Extraction) or DeepGlobe Road Extraction Challenge.
- **Geographic Tuning Source**: OpenStreetMap (OSM) vector data paired with Sentinel-2 / Google Earth Engine imagery for Indian metropolises (Bengaluru, Mumbai).

## 2. Training, Validation, and Testing Splits
- **Training Set (70%)**: Clear satellite imagery matched with accurate ground truth masks. This teaches the model the base semantics of roads.
- **Validation Set (15%)**: Used to tune hyperparameters during training. Must contain a mix of clear and occluded imagery.
- **Testing Set (15%)**: **Must be geographically isolated** from the training set (e.g., if trained on Bengaluru, test on Mumbai) to prove the model generalizes and doesn't just memorize specific Indian city layouts.

## 3. Data Augmentation Strategy (Crucial)
Because we lack a massive dataset of naturally occluded roads with perfect ground truth, we will programmatically generate synthetic occlusions during the PyTorch DataLoader step.

1. **Cloud Injection**: Superimpose Perlin noise masks or alpha-blended transparent white polygons over the optical images to simulate dense clouds.
2. **Shadow Injection**: Overlay dark, sharp-edged polygons corresponding to the cloud shapes, shifted by a calculated sun angle, to simulate cloud shadows.
3. **Geometric Jitter**: Random rotations, flips, and crops to prevent overfitting.

By doing this, the model sees an image covered in clouds, but the *ground truth mask* still contains the continuous road. The model learns to "guess" the connection beneath the cloud based on the visible entry/exit points.

## 4. Fine-Tuning Strategy
1. Pre-train SegFormer on the standard SpaceNet dataset (no clouds) for 50 epochs using standard Cross-Entropy loss.
2. Unfreeze the encoder, inject the synthetic cloud augmentations, and switch the loss function to `clDice`. Train for another 50 epochs at a learning rate of $1e-5$.

## 5. Future ISRO Dataset Integration
The pipeline is designed to be sensor-agnostic. In a post-hackathon deployment, ISRO can supply multi-modal data (e.g., Cartosat-3 Optical + RISAT-2B SAR). 
- **Integration**: The preprocessing module will be updated to accept a 4-channel tensor (RGB + SAR). The SAR channel inherently penetrates clouds, eliminating the need for the AI to "hallucinate" the occluded roads, converting the system from a geometric heuristic into a physically accurate measurement tool.
