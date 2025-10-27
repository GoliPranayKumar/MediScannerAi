# 🏗️ System Architecture & Design

## Overview

This document describes the complete system architecture of the Medical Imaging Diagnosis Agent, including component interactions, data flows, and design decisions.

---

## 1. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  React Frontend (Port 3000 → 5000 after build)          │  │
│  │  - Dark Theme UI                                        │  │
│  │  - Real-time Image Preview                             │  │
│  │  - Loading States & Animations                         │  │
│  │  - Results Display                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬─────────────────────────────────────┘
                             │ HTTP/CORS
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Flask Backend (Port 5000)                              │  │
│  │  ├─ Route: POST /api/ml-analyze                         │  │
│  │  ├─ Route: POST /api/analyze                           │  │
│  │  ├─ Route: GET /                                       │  │
│  │  └─ CORS Middleware                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────┬──────────────────────────────────────────┬─────────┘
             │                                          │
             ↓                                          ↓
┌──────────────────────────────┐        ┌──────────────────────────┐
│   ML INFERENCE LAYER         │        │   LLM API LAYER          │
│  ┌────────────────────────┐  │        │  ┌──────────────────┐   │
│  │ ml_model.py            │  │        │  │ Groq API Client  │   │
│  │ ├─ DenseNet121         │  │        │  │ (Llama 4 Scout)  │   │
│  │ ├─ ResNet50            │  │        │  └──────────────────┘   │
│  │ └─ Ensemble Logic      │  │        │                         │
│  └────────────────────────┘  │        └──────────────────────────┘
└──────────────────────────────┘
             │                                          │
             ↓                                          ↓
┌──────────────────────────────┐        ┌──────────────────────────┐
│   INFERENCE ENGINES          │        │   EXTERNAL SERVICE       │
│  ├─ TensorFlow/Keras         │        │  ├─ Groq Cloud           │
│  ├─ CUDA (optional)          │        │  ├─ Llama 4 Scout        │
│  └─ CPU Fallback             │        │  └─ API Rate Limits      │
└──────────────────────────────┘        └──────────────────────────┘
```

---

## 2. Component Architecture

### **Frontend (React)**

```
src/
├── App.js
│   ├── State Management
│   │   ├─ page: 'home' | 'scanner'
│   │   ├─ selectedFile: File | null
│   │   ├─ preview: string (base64)
│   │   ├─ loading: boolean
│   │   ├─ result: HTML string
│   │   └─ error: string | null
│   │
│   ├── Pages
│   │   ├─ Home Page
│   │   │   ├─ Title & Description
│   │   │   ├─ Key Features
│   │   │   └─ Get Started Button
│   │   │
│   │   └─ Scanner Page
│   │       ├─ Upload Area
│   │       ├─ Image Preview
│   │       ├─ Analyze Button
│   │       ├─ Results Display
│   │       └─ Reset Button
│   │
│   ├── Styles
│   │   ├─ Tailwind CSS
│   │   ├─ Custom Animations
│   │   ├─ Dark Theme
│   │   └─ Responsive Design
│   │
│   └── API Integration
│       ├─ axios.post('/api/ml-analyze')
│       └─ axios.post('/api/analyze')
```

### **Backend (Flask)**

```
app.py
├── Configuration
│   ├─ Flask app setup
│   ├─ CORS configuration
│   ├─ Upload folder setup
│   └─ Environment variables
│
├── Routes
│   ├─ GET /
│   │   └─ Serve React app
│   │
│   ├─ POST /api/ml-analyze
│   │   ├─ File validation
│   │   ├─ Image preprocessing
│   │   ├─ Model inference
│   │   ├─ Ensemble aggregation
│   │   └─ JSON response
│   │
│   ├─ POST /api/analyze
│   │   ├─ File validation
│   │   ├─ Groq API call
│   │   ├─ Markdown to HTML
│   │   └─ JSON response
│   │
│   └─ GET /<path>
│       └─ Serve static files
│
├── Utilities
│   ├─ encode_image()
│   ├─ allowed_file()
│   └─ format_ml_analysis()
│
└─ Error Handling
   ├─ File validation errors
   ├─ Model inference errors
   ├─ API errors
   └─ Logging
```

### **ML Models (ml_model.py)**

```
MedicalImagingAnalyzer
├── Initialization
│   ├─ Load DenseNet121
│   ├─ Load ResNet50
│   └─ Cache models
│
├── Image Processing
│   ├─ preprocess_image()
│   │   ├─ Read image (PIL)
│   │   ├─ Resize to 224x224
│   │   ├─ Convert to RGB
│   │   ├─ Normalize (ImageNet)
│   │   └─ Batch expand
│   │
│   └─ Feature Extraction
│       └─ extract_features()
│
├── Inference
│   ├─ analyze_with_densenet()
│   │   ├─ Forward pass
│   │   ├─ Softmax output
│   │   ├─ Decode predictions
│   │   └─ Top-5 results
│   │
│   ├─ analyze_with_resnet()
│   │   ├─ Forward pass
│   │   ├─ Softmax output
│   │   ├─ Decode predictions
│   │   └─ Top-5 results
│   │
│   └─ ensemble_analysis()
│       ├─ Run both models
│       ├─ Average scores
│       ├─ Generate recommendation
│       └─ Return combined results
│
└─ Utilities
   └─ _get_medical_recommendation()
```

---

## 3. Data Flow Diagrams

### **ML Analysis Flow**

```
User Upload
    ↓
┌─────────────────────────────────────┐
│ Frontend Validation                 │
├─────────────────────────────────────┤
│ ✓ File type check                   │
│ ✓ File size check                   │
│ ✓ Generate preview                  │
│ ✓ Show loading state                │
└─────────────────────────────────────┘
    ↓
POST /api/ml-analyze
    ↓
┌─────────────────────────────────────┐
│ Backend Validation                  │
├─────────────────────────────────────┤
│ ✓ File exists                       │
│ ✓ Extension allowed                 │
│ ✓ Save to uploads/                  │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ Image Preprocessing                 │
├─────────────────────────────────────┤
│ ✓ Read with PIL                     │
│ ✓ Resize 224x224                    │
│ ✓ Convert RGB                       │
│ ✓ Normalize                         │
│ ✓ Batch expand                      │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ Parallel Inference                  │
├─────────────────────────────────────┤
│ ├─ DenseNet121                      │
│ │  └─ 150ms inference               │
│ │     └─ Top-5 predictions          │
│ │                                   │
│ └─ ResNet50                         │
│    └─ 150ms inference               │
│       └─ Top-5 predictions          │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ Ensemble Aggregation                │
├─────────────────────────────────────┤
│ ✓ Average confidence scores         │
│ ✓ Generate recommendation           │
│ ✓ Format as HTML                    │
└─────────────────────────────────────┘
    ↓
JSON Response
    ↓
Frontend Display
    ↓
User Views Results
```

### **Groq LLM Analysis Flow**

```
User Upload
    ↓
POST /api/analyze
    ↓
┌─────────────────────────────────────┐
│ File Validation                     │
├─────────────────────────────────────┤
│ ✓ Check extension                   │
│ ✓ Save file                         │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ Image Encoding                      │
├─────────────────────────────────────┤
│ ✓ Read binary                       │
│ ✓ Base64 encode                     │
│ ✓ Create data URI                   │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ Groq API Call                       │
├─────────────────────────────────────┤
│ ✓ Create Groq client                │
│ ✓ Send image + prompt               │
│ ✓ Model: Llama 4 Scout              │
│ ✓ Wait for response                 │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ Response Processing                 │
├─────────────────────────────────────┤
│ ✓ Extract text                      │
│ ✓ Markdown to HTML                  │
│ ✓ Format for display                │
└─────────────────────────────────────┘
    ↓
JSON Response
    ↓
Frontend Display
```

---

## 4. Database & Storage

### **File Storage**

```
uploads/
├── image_1.jpg          (Temporary)
├── image_2.png          (Temporary)
└── image_3.dicom        (Temporary)

Note: Files are temporary and can be cleaned up
```

### **Model Cache**

```
~/.keras/models/
├── densenet121_weights_tf_dim_ordering_tf_kernels.h5
└── resnet50_weights_tf_dim_ordering_tf_kernels.h5

Note: Downloaded on first run (~500MB)
```

### **Environment Variables**

```
.env
├── GROQ_API_KEY=gsk_...
└── FLASK_ENV=development
```

---

## 5. API Specification

### **Endpoint 1: ML Analysis**

```
POST /api/ml-analyze

Request:
- Content-Type: multipart/form-data
- Body: image (binary file)

Response (200 OK):
{
  "result": "<div>...</div>",
  "analysis": {
    "ensemble_confidence": 87.5,
    "densenet_result": {
      "model": "DenseNet121",
      "top_prediction": "chest X-ray",
      "confidence": 89.2,
      "predictions": [
        {"class": "chest X-ray", "confidence": 89.2, "score": 0.892},
        {"class": "X-ray", "confidence": 7.8, "score": 0.078}
      ]
    },
    "resnet_result": {
      "model": "ResNet50",
      "top_prediction": "X-ray",
      "confidence": 85.8,
      "predictions": [...]
    },
    "recommendation": "High confidence detection..."
  }
}

Error Response (400/500):
{
  "error": "Error message"
}
```

### **Endpoint 2: Groq Analysis**

```
POST /api/analyze

Request:
- Content-Type: multipart/form-data
- Body: image (binary file)

Response (200 OK):
{
  "result": "<div><p>Analysis text...</p></div>"
}

Error Response (400/500):
{
  "error": "Error message"
}
```

### **Endpoint 3: Health Check**

```
GET /

Response (200 OK):
- React app HTML

Response (404):
- "React app not built..."
```

---

## 6. Technology Decisions

### **Why DenseNet121 + ResNet50?**

| Aspect | DenseNet121 | ResNet50 |
|--------|-----------|---------|
| Parameters | 7.97M | 25.6M |
| Speed | Fast | Medium |
| Accuracy | High | Very High |
| Memory | Low | Medium |
| **Combined** | **Balanced** | **Robust** |

**Decision**: Use both for ensemble robustness

### **Why Transfer Learning?**

- ✅ Pre-trained on 1.2M ImageNet images
- ✅ No need for large medical datasets
- ✅ Fast inference
- ✅ Good generalization
- ✅ Proven architecture

### **Why Flask?**

- ✅ Lightweight
- ✅ Easy to integrate with ML
- ✅ Good for APIs
- ✅ Python ecosystem
- ✅ Development friendly

### **Why React?**

- ✅ Modern UI framework
- ✅ Real-time updates
- ✅ Component reusability
- ✅ Large ecosystem
- ✅ Good for animations

### **Why Groq API?**

- ✅ Fast inference
- ✅ Powerful LLM (Llama 4)
- ✅ Medical domain knowledge
- ✅ Text analysis capability
- ✅ Complements vision models

---

## 7. Performance Optimization

### **Frontend Optimization**

```
Techniques:
├─ Code splitting
├─ Lazy loading
├─ Image optimization
├─ CSS minification
├─ JS minification
└─ Caching
```

### **Backend Optimization**

```
Techniques:
├─ Model caching (load once)
├─ Batch processing
├─ Async operations (optional)
├─ Response compression
└─ Error handling
```

### **ML Optimization**

```
Techniques:
├─ GPU acceleration (if available)
├─ Model quantization (optional)
├─ Batch inference
├─ Feature caching
└─ Memory pooling
```

---

## 8. Security Considerations

### **Input Validation**

```
✓ File type checking
✓ File size limits
✓ Filename sanitization
✓ MIME type validation
```

### **API Security**

```
✓ CORS configuration
✓ Rate limiting (optional)
✓ Input sanitization
✓ Error message filtering
```

### **Data Privacy**

```
✓ Temporary file cleanup
✓ No data persistence
✓ API key in environment
✓ HTTPS ready
```

---

## 9. Scalability Considerations

### **Current Limitations**

- Single-threaded Flask
- No database
- No caching layer
- No load balancing

### **Future Improvements**

```
├─ Gunicorn/uWSGI for production
├─ Redis for caching
├─ Database for history
├─ Load balancing
├─ Containerization (Docker)
├─ Kubernetes orchestration
└─ Microservices architecture
```

---

## 10. Deployment Architecture

### **Development**

```
Local Machine
├─ Flask (debug mode)
├─ React (dev server)
├─ Models (local)
└─ Groq API (cloud)
```

### **Production (Recommended)**

```
Cloud Server (AWS/GCP/Azure)
├─ Gunicorn (WSGI)
├─ Nginx (reverse proxy)
├─ React (static files)
├─ Redis (cache)
├─ PostgreSQL (optional)
└─ Groq API (cloud)
```

### **Docker Deployment**

```
Dockerfile
├─ Python 3.10
├─ TensorFlow
├─ Flask
├─ Node.js
├─ React build
└─ Nginx
```

---

## 11. Monitoring & Logging

### **Logging Strategy**

```
Levels:
├─ DEBUG: Development info
├─ INFO: General events
├─ WARNING: Potential issues
└─ ERROR: Failures

Logs:
├─ app.log (Flask)
├─ model.log (ML)
└─ error.log (Errors)
```

### **Metrics to Track**

```
├─ Request count
├─ Response time
├─ Error rate
├─ Model inference time
├─ API call latency
└─ Resource usage
```

---

## 12. Disaster Recovery

### **Backup Strategy**

```
├─ Model weights (auto-download)
├─ Source code (Git)
├─ Configuration (.env)
└─ User uploads (temporary)
```

### **Recovery Plan**

```
├─ Model re-download
├─ Code rollback
├─ Config restoration
└─ Service restart
```

---

**Last Updated**: October 27, 2025  
**Version**: 2.0
