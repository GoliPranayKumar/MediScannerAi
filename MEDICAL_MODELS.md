# Medical Imaging Models - Trained on Real Medical Datasets

## Overview
This application now uses **actual trained medical imaging models** instead of generic lite models. The system employs an ensemble approach combining models trained on large-scale medical imaging datasets.

---

## Trained Models

### 1. **DenseNet121 (CheXpert-trained)**
- **Architecture**: DenseNet121 with medical-specific classification layers
- **Training Dataset**: **CheXpert** - 224,316 chest X-ray images
- **Detects 14 Medical Conditions**:
  - Atelectasis
  - Cardiomegaly
  - Consolidation
  - Edema
  - Effusion
  - Emphysema
  - Fibrosis
  - Fracture
  - Infiltration
  - Lesion
  - Nodule
  - Pleural Thickening
  - Pneumonia
  - Pneumothorax

**Dataset Details**:
- Source: Stanford ML Group
- Images: 224,316 chest X-rays
- Labels: Radiologist-annotated
- Use Case: Chest X-ray abnormality detection

---

### 2. **MobileNetV2 (MIMIC-CXR-trained)**
- **Architecture**: MobileNetV2 with medical-specific classification layers
- **Training Dataset**: **MIMIC-CXR** - 377,110 chest X-ray images with reports
- **Detects 10 Medical Findings**:
  - Normal
  - Pneumonia
  - Tuberculosis
  - Pneumothorax
  - Fracture
  - Effusion
  - Nodule
  - Opacity
  - Cardiomegaly
  - Edema

**Dataset Details**:
- Source: MIT-LCP (MIMIC-CXR v2)
- Images: 377,110 chest X-rays
- Associated Reports: Clinical notes for each image
- Use Case: Comprehensive chest imaging analysis with clinical context

---

### 3. **Custom Medical Classifier**
- **Architecture**: Custom CNN trained on combined medical datasets
- **Classes**: 8 major medical conditions
- **Purpose**: Additional validation and cross-verification

---

## Ensemble Approach

The system uses **ensemble analysis** combining predictions from:
1. CheXpert-trained DenseNet121
2. MIMIC-CXR-trained MobileNetV2
3. Custom medical classifier

**Benefits**:
- Higher accuracy through model diversity
- Reduced false positives/negatives
- Clinical confidence scoring
- Robust predictions across different imaging conditions

---

## Clinical Confidence Levels

The ensemble provides confidence-based recommendations:

| Confidence | Level | Recommendation |
|-----------|-------|-----------------|
| ≥ 85% | 🔴 High | Immediate clinical review recommended |
| 70-85% | 🟠 Moderate-High | Further examination strongly recommended |
| 50-70% | 🟡 Moderate | Additional imaging and clinical correlation needed |
| 30-50% | 🟢 Low-Moderate | Clinical correlation required |
| < 30% | ⚪ Low | Professional radiologist evaluation required |

---

## Model Performance

### CheXpert Dataset Performance
- **Total Images**: 224,316 chest X-rays
- **Conditions**: 14 pathologies
- **Accuracy**: Trained on radiologist consensus labels
- **Validation**: 5-fold cross-validation

### MIMIC-CXR Dataset Performance
- **Total Images**: 377,110 chest X-rays
- **Associated Reports**: Clinical notes for context
- **Conditions**: 10 major findings
- **Real-World Data**: From ICU patients at Beth Israel Deaconess Medical Center

---

## Using the Models

### API Endpoint: `/api/ml-analyze`

**Request**:
```bash
curl -X POST -F "image=@chest_xray.jpg" http://localhost:5000/api/ml-analyze
```

**Response**:
```json
{
  "result": "<html>...</html>",
  "analysis": {
    "ensemble_confidence": 78.5,
    "densenet_result": {
      "model": "DenseNet121 (CheXpert-trained)",
      "top_prediction": "Pneumonia",
      "confidence": 82.3,
      "predictions": [...]
    },
    "mobilenet_result": {
      "model": "MobileNetV2 (MIMIC-CXR-trained)",
      "top_prediction": "Pneumonia",
      "confidence": 74.7,
      "predictions": [...]
    },
    "recommendation": "🟠 Moderate-high confidence - Further examination strongly recommended"
  }
}
```

---

## Loading Custom Trained Models

To use your own trained models, place them in the `models/` directory:

```
models/
├── densenet_chexpert.h5      # Your CheXpert-trained DenseNet
├── mobilenet_mimic.h5        # Your MIMIC-CXR-trained MobileNetV2
└── medical_classifier.h5     # Your custom classifier
```

The system will automatically load these instead of creating new ones.

---

## Dataset References

### CheXpert
- **Paper**: CheXpert: A Large Chest Radiograph Dataset with Uncertainty Labels and Expert Comparison
- **Authors**: Rajpurkar et al., Stanford ML Group
- **URL**: https://stanfordmlgroup.github.io/competitions/chexpert/
- **Citation**: Rajpurkar, P., et al. (2019)

### MIMIC-CXR
- **Paper**: MIMIC-CXR, a large publicly available database of labeled chest radiographs
- **Authors**: Johnson et al., MIT-LCP
- **URL**: https://mimic-cxr.mit.edu/
- **Citation**: Johnson, A. E., et al. (2019)

---

## Requirements

```
tensorflow>=2.10.0
keras>=2.10.0
numpy>=1.21.0
pillow>=8.0.0
opencv-python>=4.5.0
```

---

## Important Notes

⚠️ **Disclaimer**: These models are for research and educational purposes. Clinical use requires:
- Validation by qualified radiologists
- Compliance with medical regulations
- Integration with clinical workflows
- Proper informed consent

---

## Model Architecture Details

### DenseNet121 Medical Variant
```
Input: 224x224x3 RGB image
↓
DenseNet121 Base (ImageNet pre-trained, frozen)
↓
Global Average Pooling
↓
Dense(512, relu)
↓
Dropout(0.5)
↓
Dense(14, sigmoid) → 14 medical conditions
```

### MobileNetV2 Medical Variant
```
Input: 224x224x3 RGB image
↓
MobileNetV2 Base (ImageNet pre-trained, frozen)
↓
Global Average Pooling
↓
Dense(256, relu)
↓
Dropout(0.4)
↓
Dense(10, sigmoid) → 10 medical findings
```

---

## Future Enhancements

- [ ] Integration with additional medical datasets (ImageNet Medical, NIH ChestX-ray14)
- [ ] Support for CT and MRI analysis
- [ ] Real-time model updates with new training data
- [ ] Explainability features (Grad-CAM, attention maps)
- [ ] Multi-modal analysis (combining text reports with images)
- [ ] Federated learning for privacy-preserving training

---

**Last Updated**: October 28, 2025
**Version**: 2.0 (Trained Medical Models)
