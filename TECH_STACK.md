# 🛠️ Complete Tech Stack Documentation

## Overview

This document provides detailed information about every technology, library, and framework used in the Medical Imaging Diagnosis Agent.

---

## 📋 Table of Contents

1. [Backend Stack](#backend-stack)
2. [Frontend Stack](#frontend-stack)
3. [ML/AI Stack](#mlai-stack)
4. [DevOps & Deployment](#devops--deployment)
5. [Version Matrix](#version-matrix)
6. [Dependency Tree](#dependency-tree)
7. [Installation Guide](#installation-guide)

---

## 🔧 Backend Stack

### **Core Framework: Flask**

```
Package: flask
Version: Latest
Purpose: Web framework for API endpoints
Key Features:
  ├─ Lightweight and modular
  ├─ Built-in development server
  ├─ Jinja2 templating
  ├─ Werkzeug WSGI toolkit
  └─ Blueprint support for modular apps

Usage in Project:
  ├─ app.py: Flask app initialization
  ├─ Routes: /api/ml-analyze, /api/analyze, /
  └─ Error handling & logging
```

### **CORS Support: flask-cors**

```
Package: flask-cors
Version: Latest
Purpose: Enable Cross-Origin Resource Sharing
Key Features:
  ├─ Simple decorator-based API
  ├─ Automatic preflight handling
  ├─ Resource-level configuration
  └─ Wildcard support

Usage in Project:
  ├─ Allow React frontend to call Flask backend
  ├─ Enable cross-domain requests
  └─ Handle OPTIONS requests
```

### **Environment Configuration: python-dotenv**

```
Package: python-dotenv
Version: Latest
Purpose: Load environment variables from .env file
Key Features:
  ├─ .env file support
  ├─ Automatic loading
  ├─ Override capability
  └─ Type conversion

Usage in Project:
  ├─ Load GROQ_API_KEY
  ├─ Load FLASK_ENV
  └─ Configuration management
```

### **Markdown Processing: markdown**

```
Package: markdown
Version: Latest
Purpose: Convert Markdown to HTML
Key Features:
  ├─ Fenced code blocks
  ├─ Tables support
  ├─ Extensions system
  └─ HTML sanitization

Usage in Project:
  ├─ Convert Groq API responses to HTML
  ├─ Format medical analysis results
  └─ Display in React frontend
```

### **HTML Safety: markupsafe**

```
Package: markupsafe
Version: Latest
Purpose: Safe string handling in templates
Key Features:
  ├─ XSS prevention
  ├─ HTML escaping
  ├─ Safe string marking
  └─ Jinja2 integration

Usage in Project:
  ├─ Protect against injection attacks
  ├─ Safe HTML rendering
  └─ Template security
```

### **LLM API: groq**

```
Package: groq
Version: Latest
Purpose: Groq API client for LLM inference
Key Features:
  ├─ Async support
  ├─ Streaming responses
  ├─ Error handling
  └─ Rate limiting

Usage in Project:
  ├─ Send images to Llama 4 Scout
  ├─ Get medical analysis
  ├─ Format responses
  └─ Handle API errors

Configuration:
  ├─ API Key: GROQ_API_KEY
  ├─ Model: meta-llama/llama-4-scout-17b-16e-instruct
  └─ Endpoint: api.groq.com
```

### **File Handling: werkzeug**

```
Package: werkzeug (included with Flask)
Version: Latest
Purpose: WSGI utilities and file handling
Key Features:
  ├─ Secure filename handling
  ├─ File upload handling
  ├─ Data structures
  └─ Utilities

Usage in Project:
  ├─ secure_filename() for uploads
  ├─ File validation
  └─ Request parsing
```

---

## ⚛️ Frontend Stack

### **Framework: React**

```
Package: react
Version: 18+
Purpose: UI library for building components
Key Features:
  ├─ Component-based architecture
  ├─ Virtual DOM
  ├─ Hooks API
  ├─ State management
  └─ Lifecycle methods

Usage in Project:
  ├─ App.js: Main component
  ├─ State: page, selectedFile, preview, loading, result, error
  ├─ Hooks: useState, useEffect
  └─ Conditional rendering
```

### **Styling: Tailwind CSS**

```
Package: tailwindcss
Version: Latest
Purpose: Utility-first CSS framework
Key Features:
  ├─ Utility classes
  ├─ Responsive design
  ├─ Dark mode support
  ├─ Customization
  └─ PurgeCSS optimization

Usage in Project:
  ├─ Dark theme (bg-gray-900, etc.)
  ├─ Responsive grid (grid-cols-1, lg:grid-cols-4)
  ├─ Animations (animate-spin, animate-pulse)
  ├─ Spacing & sizing
  └─ Custom animations (@keyframes)

Custom Animations:
  ├─ @keyframes gradient-shift
  ├─ @keyframes float
  ├─ @keyframes glow
  ├─ @keyframes slideIn
  ├─ @keyframes pulse-glow
  ├─ @keyframes rotate-slow
  ├─ @keyframes bounce-gentle
  └─ @keyframes scan-line
```

### **Icons: Lucide React**

```
Package: lucide-react
Version: Latest
Purpose: Icon library for React
Key Features:
  ├─ 400+ icons
  ├─ SVG-based
  ├─ Customizable size/color
  ├─ Tree-shakeable
  └─ TypeScript support

Usage in Project:
  ├─ Upload icon
  ├─ Loader icon
  ├─ AlertCircle icon
  ├─ CheckCircle icon
  ├─ Sparkles icon
  └─ ArrowRight icon
```

### **HTTP Client: Axios**

```
Package: axios
Version: Latest
Purpose: Promise-based HTTP client
Key Features:
  ├─ Request/response interceptors
  ├─ Automatic JSON transformation
  ├─ Timeout support
  ├─ Cancel tokens
  └─ FormData support

Usage in Project:
  ├─ POST /api/ml-analyze
  ├─ POST /api/analyze
  ├─ FormData for file upload
  └─ Error handling
```

### **Build Tool: Create React App**

```
Package: react-scripts
Version: Latest
Purpose: Zero-config React app setup
Key Features:
  ├─ Webpack bundling
  ├─ Babel transpilation
  ├─ Development server
  ├─ Production build
  └─ Testing setup

Usage in Project:
  ├─ npm start: Development
  ├─ npm run build: Production
  ├─ npm test: Testing
  └─ npm eject: Customization
```

---

## 🤖 ML/AI Stack

### **Deep Learning: TensorFlow**

```
Package: tensorflow
Version: ≥2.13.0
Purpose: Deep learning framework
Key Features:
  ├─ Keras API
  ├─ Pre-trained models
  ├─ GPU support
  ├─ Model optimization
  └─ Inference optimization

Usage in Project:
  ├─ Load DenseNet121
  ├─ Load ResNet50
  ├─ Image preprocessing
  ├─ Model inference
  └─ Feature extraction

Models Used:
  ├─ DenseNet121 (7.97M parameters)
  ├─ ResNet50 (25.6M parameters)
  └─ Both pre-trained on ImageNet
```

### **Image Processing: OpenCV**

```
Package: opencv-python
Version: ≥4.8.0
Purpose: Computer vision library
Key Features:
  ├─ Image reading/writing
  ├─ Image transformations
  ├─ Color space conversion
  ├─ Feature detection
  └─ Image analysis

Usage in Project:
  ├─ Image loading (cv2.imread)
  ├─ Resizing
  ├─ Color conversion
  └─ Preprocessing
```

### **Image Library: Pillow**

```
Package: Pillow
Version: ≥10.0.0
Purpose: Python Imaging Library
Key Features:
  ├─ Image opening/saving
  ├─ Format conversion
  ├─ Image operations
  ├─ Thumbnail generation
  └─ Metadata handling

Usage in Project:
  ├─ Image.open() for loading
  ├─ Format conversion
  ├─ Resizing to 224x224
  └─ RGB conversion
```

### **Numerical Computing: NumPy**

```
Package: numpy
Version: ≥1.24.0
Purpose: Numerical computing library
Key Features:
  ├─ N-dimensional arrays
  ├─ Mathematical functions
  ├─ Linear algebra
  ├─ Random number generation
  └─ Broadcasting

Usage in Project:
  ├─ Array operations
  ├─ Image data manipulation
  ├─ Statistical calculations
  ├─ Feature extraction
  └─ Ensemble aggregation
```

### **ML Utilities: scikit-learn**

```
Package: scikit-learn
Version: ≥1.3.0
Purpose: Machine learning library
Key Features:
  ├─ Classification algorithms
  ├─ Preprocessing utilities
  ├─ Model evaluation
  ├─ Dimensionality reduction
  └─ Feature engineering

Usage in Project:
  ├─ Preprocessing utilities
  ├─ Statistical functions
  ├─ Feature scaling (optional)
  └─ Metrics calculation
```

---

## 🚀 DevOps & Deployment

### **Package Management: pip**

```
Tool: pip
Version: Latest
Purpose: Python package manager
Usage:
  ├─ pip install -r requirements.txt
  ├─ pip freeze > requirements.txt
  └─ Virtual environment management
```

### **Node Package Manager: npm**

```
Tool: npm
Version: 8+
Purpose: JavaScript package manager
Usage:
  ├─ npm install
  ├─ npm run build
  ├─ npm start
  └─ Dependency management
```

### **Virtual Environment: venv**

```
Tool: Python venv
Purpose: Isolated Python environment
Usage:
  ├─ python -m venv .venv
  ├─ .\.venv\Scripts\Activate.ps1 (Windows)
  ├─ source .venv/bin/activate (Unix)
  └─ Dependency isolation
```

### **Version Control: Git**

```
Tool: Git
Purpose: Source code management
Files:
  ├─ .gitignore: Exclude files
  ├─ .git/: Repository data
  └─ Commit history
```

### **Production Server: Gunicorn** (Recommended)

```
Package: gunicorn
Purpose: WSGI HTTP Server
Usage:
  ├─ gunicorn app:app
  ├─ gunicorn -w 4 app:app
  └─ Production deployment
```

### **Reverse Proxy: Nginx** (Recommended)

```
Tool: Nginx
Purpose: Web server & reverse proxy
Configuration:
  ├─ Static file serving
  ├─ Request forwarding
  ├─ SSL/TLS termination
  └─ Load balancing
```

### **Containerization: Docker** (Optional)

```
Tool: Docker
Purpose: Container orchestration
Files:
  ├─ Dockerfile: Image definition
  ├─ docker-compose.yml: Multi-container
  └─ .dockerignore: Exclude files
```

---

## 📊 Version Matrix

### **Python Ecosystem**

| Package | Version | Purpose |
|---------|---------|---------|
| Python | 3.8+ | Runtime |
| Flask | Latest | Web framework |
| flask-cors | Latest | CORS support |
| TensorFlow | ≥2.13.0 | Deep learning |
| OpenCV | ≥4.8.0 | Image processing |
| Pillow | ≥10.0.0 | Image library |
| NumPy | ≥1.24.0 | Numerical computing |
| scikit-learn | ≥1.3.0 | ML utilities |
| python-dotenv | Latest | Environment config |
| markdown | Latest | Markdown processing |
| markupsafe | Latest | HTML safety |
| groq | Latest | LLM API client |

### **JavaScript Ecosystem**

| Package | Version | Purpose |
|---------|---------|---------|
| Node.js | 14+ | Runtime |
| React | 18+ | UI framework |
| Tailwind CSS | Latest | Styling |
| Lucide React | Latest | Icons |
| Axios | Latest | HTTP client |
| react-scripts | Latest | Build tool |

---

## 🌳 Dependency Tree

### **Backend Dependencies**

```
requirements.txt
├── flask (web framework)
│   ├── Werkzeug (WSGI)
│   ├── Jinja2 (templating)
│   └── click (CLI)
│
├── flask-cors (CORS support)
│   └── flask
│
├── tensorflow (deep learning)
│   ├── numpy
│   ├── h5py
│   ├── protobuf
│   └── keras
│
├── opencv-python (image processing)
│   └── numpy
│
├── Pillow (image library)
│   └── numpy (optional)
│
├── numpy (numerical computing)
│   └── (C/Fortran libraries)
│
├── scikit-learn (ML utilities)
│   ├── numpy
│   ├── scipy
│   └── joblib
│
├── python-dotenv (environment config)
│   └── (no dependencies)
│
├── markdown (markdown processing)
│   └── (no dependencies)
│
├── markupsafe (HTML safety)
│   └── (no dependencies)
│
└── groq (LLM API)
    ├── httpx
    ├── pydantic
    └── typing-extensions
```

### **Frontend Dependencies**

```
package.json
├── react (UI framework)
│   ├── react-dom
│   └── prop-types
│
├── tailwindcss (styling)
│   ├── postcss
│   └── autoprefixer
│
├── lucide-react (icons)
│   └── react
│
├── axios (HTTP client)
│   └── (no dependencies)
│
└── react-scripts (build tool)
    ├── webpack
    ├── babel
    ├── eslint
    └── jest
```

---

## 📦 Installation Guide

### **Step 1: Backend Setup**

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import tensorflow; print(tensorflow.__version__)"
```

### **Step 2: Frontend Setup**

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Build for production
npm run build

# Return to root
cd ..
```

### **Step 3: Configuration**

```bash
# Create .env file
echo "GROQ_API_KEY=your_key_here" > .env

# Or set environment variable
# Windows PowerShell:
$env:GROQ_API_KEY = "your_key_here"
# macOS/Linux:
export GROQ_API_KEY="your_key_here"
```

### **Step 4: Run Application**

```bash
# Start Flask server
python app.py

# Open browser
# http://localhost:5000
```

---

## 🔍 Dependency Analysis

### **Size Impact**

| Package | Size | Impact |
|---------|------|--------|
| TensorFlow | ~500MB | Large (models) |
| OpenCV | ~100MB | Medium |
| NumPy | ~50MB | Medium |
| React | ~5MB | Small |
| Tailwind CSS | ~2MB | Small |
| Others | ~50MB | Small |
| **Total** | **~700MB** | **Large** |

### **Performance Impact**

| Component | Load Time | Inference Time |
|-----------|-----------|-----------------|
| DenseNet121 | 2-3s | ~150ms |
| ResNet50 | 2-3s | ~150ms |
| Groq API | - | ~2-5s |
| React Frontend | <1s | - |
| **Total** | ~5s | ~300ms-5s |

---

## 🔐 Security Considerations

### **Dependency Security**

```
Best Practices:
├─ Regular updates
├─ Security audits
├─ Vulnerability scanning
├─ Pinned versions
└─ Minimal dependencies
```

### **Known Vulnerabilities**

```
Check with:
├─ pip-audit
├─ npm audit
├─ Dependabot
└─ Snyk
```

---

## 📚 Learning Resources

### **Backend**

- Flask: https://flask.palletsprojects.com/
- TensorFlow: https://www.tensorflow.org/
- OpenCV: https://opencv.org/
- NumPy: https://numpy.org/

### **Frontend**

- React: https://react.dev/
- Tailwind CSS: https://tailwindcss.com/
- Lucide Icons: https://lucide.dev/
- Axios: https://axios-http.com/

### **ML/AI**

- DenseNet: https://arxiv.org/abs/1608.06993
- ResNet: https://arxiv.org/abs/1512.03385
- Transfer Learning: https://cs231n.github.io/transfer-learning/
- ImageNet: https://www.image-net.org/

---

## 🎯 Recommended Versions

### **For Development**

```
Python: 3.10+
Node.js: 18+
TensorFlow: 2.13+
React: 18+
```

### **For Production**

```
Python: 3.10 (LTS)
Node.js: 18 LTS
TensorFlow: 2.13 (stable)
React: 18 (stable)
```

---

**Last Updated**: October 27, 2025  
**Version**: 2.0
