# 🏥 MediScanner AI

**AI-powered medical image analysis using Deep Learning + LLM**

An advanced platform that combines deep learning models (DenseNet121, ResNet50) with Groq's LLM for comprehensive medical image analysis. Provides ensemble predictions, confidence scores, and clinical recommendations.

---

## 📋 Table of Contents

1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Architecture](#architecture)
4. [Installation](#installation)
5. [Quick Start](#quick-start)
6. [Usage](#usage)
7. [API Endpoints](#api-endpoints)
8. [Project Structure](#project-structure)
9. [Workflow](#workflow)
10. [Troubleshooting](#troubleshooting)

---

## 📸 Screenshots

### **Home Page**
```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  [Logo]  MediScanner AI                                │
│          AI-powered analysis of medical images         │
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │  About This Application                         │  │
│  │  Welcome to MediScanner AI - an advanced        │  │
│  │  AI-powered platform designed to assist         │  │
│  │  healthcare professionals in analyzing          │  │
│  │  medical images with precision and speed.       │  │
│  │                                                 │  │
│  │  Key Features:                                  │  │
│  │  ✓ Identification of diseases                   │  │
│  │  ✓ Clear, concise medical insights             │  │
│  │  ✓ Support for multiple image formats          │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
│  [🧠 Brain Imaging] [🔬 Scan Tech] [⚡ AI Powered]   │
│                                                         │
│  🔬 Data Science & ML Impact                          │
│  ┌──────────────────────┬──────────────────────┐      │
│  │ 🧠 DenseNet121       │ ⚙️ ResNet50          │      │
│  │ 7.97M Parameters     │ 25.6M Parameters     │      │
│  │ ~150ms Inference     │ ~150ms Inference     │      │
│  │ 76% Accuracy         │ 76% Accuracy         │      │
│  └──────────────────────┴──────────────────────┘      │
│                                                         │
│  Ensemble Analysis                                     │
│  Confidence: 87.5% | Speed: ~300ms | Boost: +5-8%    │
│                                                         │
│  [Get Started →]                                       │
└─────────────────────────────────────────────────────────┘
```

### **Scanner Page**
```
┌─────────────────────────────────────────────────────────┐
│  ← Back                                                │
│                                                         │
│  ┌──────────────────────┬──────────────────────────┐  │
│  │                      │  Upload Medical Image    │  │
│  │                      │  ┌────────────────────┐  │  │
│  │  Image Preview       │  │ Click to upload    │  │  │
│  │  [Image shown here]  │  │ PNG, JPG, DICOM    │  │  │
│  │                      │  └────────────────────┘  │  │
│  │                      │                          │  │
│  │                      │  [Analyze] [Reset]      │  │
│  └──────────────────────┴──────────────────────────┘  │
│                                                         │
│  Analysis Results                                      │
│  ┌─────────────────────────────────────────────────┐  │
│  │ ✨ Analysis Complete                           │  │
│  │                                                 │  │
│  │ [Detailed analysis results with confidence     │  │
│  │  scores, predictions, and medical             │  │
│  │  recommendations displayed here]               │  │
│  │                                                 │  │
│  │ Analysis powered by AI ● ● ●                   │  │
│  └─────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### **Scanning Animation**
```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│              Initializing Scanner                      │
│              Preparing medical imaging analysis...     │
│                                                         │
│                    ◯ ◯ ◯                              │
│                   ◯     ◯                             │
│                  ◯   ◯   ◯                            │
│                   ◯     ◯                             │
│                    ◯ ◯ ◯                              │
│                                                         │
│              ████████░░░░░░░░░░ 45%                   │
│                                                         │
│                  ● ● ●                                │
│                 (loading dots)                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### **Key Visual Features:**
- 🎨 **Dark Theme**: Professional dark background with cyan/purple gradients
- ✨ **Animations**: Smooth transitions, glowing effects, floating elements
- 🎯 **Logo**: Professional medical AI logo with eye and heartbeat symbols
- 📱 **Responsive**: Works on desktop, tablet, and mobile
- 🌈 **Gradients**: Cyan (#64c8ff) to Purple (#9664ff) color scheme
- 💫 **Effects**: Glowing borders, shimmer animations, pulsing elements

---

## ✨ Features

### 🤖 **Dual Analysis System**
- **Deep Learning Models**: DenseNet121 + ResNet50 ensemble
- **LLM Analysis**: Groq API with Llama 4 Scout model
- **Hybrid Approach**: Combines computer vision + NLP

### 📊 **Advanced Analysis**
- Ensemble confidence scoring (average of 2 models)
- Top-5 predictions from each model
- Medical recommendations based on confidence
- Feature extraction and statistical analysis

### 🎨 **Modern UI**
- Dark theme with cyan/purple gradients
- Real-time image preview
- Loading animations and smooth transitions
- Responsive design (mobile + desktop)
- Beautiful glassmorphic cards

### 📁 **Multiple Format Support**
- PNG, JPG, JPEG, DICOM (medical imaging)
- Automatic preprocessing and normalization
- Base64 encoding for API transmission

---

## 🛠️ Tech Stack

### **Backend**
| Component | Technology | Version |
|-----------|-----------|---------|
| Web Framework | Flask | Latest |
| CORS | flask-cors | Latest |
| Deep Learning | TensorFlow | ≥2.13.0 |
| Image Processing | OpenCV | ≥4.8.0 |
| Image Library | Pillow | ≥10.0.0 |
| ML Utils | scikit-learn | ≥1.3.0 |
| Numerical | NumPy | ≥1.24.0 |
| LLM API | Groq | Latest |
| Markdown | markdown | Latest |
| Env Config | python-dotenv | Latest |

### **Frontend**
| Component | Technology | Version |
|-----------|-----------|---------|
| Framework | React | 18+ |
| Styling | Tailwind CSS | Latest |
| Icons | Lucide React | Latest |
| Build Tool | Create React App | Latest |
| HTTP Client | Axios | Latest |

### **Models**
| Model | Type | Pre-trained | Parameters |
|-------|------|-----------|-----------|
| DenseNet121 | CNN | ImageNet | 7.97M |
| ResNet50 | CNN | ImageNet | 25.6M |
| Llama 4 Scout | LLM | Custom | 17B |

---

## 🏗️ Architecture

### **System Architecture**
```
┌─────────────────────────────────────────────────────────┐
│                    React Frontend                        │
│  (Dark Theme, Real-time Preview, Animations)            │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/CORS
                     ↓
┌─────────────────────────────────────────────────────────┐
│                  Flask Backend                           │
│  ┌──────────────────────────────────────────────────┐  │
│  │  /api/analyze (Groq LLM Analysis)                │  │
│  │  /api/ml-analyze (Deep Learning Analysis)        │  │
│  └──────────────────────────────────────────────────┘  │
└────┬──────────────────────────────────────────────┬────┘
     │                                              │
     ↓                                              ↓
┌──────────────────┐                    ┌──────────────────┐
│  Groq API        │                    │  ML Models       │
│  (Llama 4)       │                    │  (DenseNet+      │
│                  │                    │   ResNet)        │
└──────────────────┘                    └──────────────────┘
```

### **Data Flow**
```
User Upload Image
    ↓
React Frontend (Preview)
    ↓
Flask Backend (Validation)
    ↓
┌─────────────────────────────────────┐
│  Parallel Analysis                  │
├─────────────────────────────────────┤
│ ├─ DenseNet121 (224x224 input)      │
│ ├─ ResNet50 (224x224 input)         │
│ └─ Groq LLM (Base64 image)          │
└─────────────────────────────────────┘
    ↓
Results Aggregation
    ↓
HTML Formatting
    ↓
React Frontend (Display Results)
```

---

## 📦 Installation

### **Prerequisites**
- Python 3.8+
- Node.js 14+ (for frontend)
- 2GB RAM minimum
- 1GB disk space (for models)
- Internet connection (for first run)

### **Step 1: Clone/Setup Project**
```bash
cd "AI Medical Imaging Diagnosis Agent"
```

### **Step 2: Create Virtual Environment (Optional but Recommended)**
```powershell
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### **Step 3: Install Backend Dependencies**
```bash
pip install -r requirements.txt
```

**First install will:**
- Download TensorFlow (~500MB)
- Download pre-trained models (~500MB)
- Install all dependencies
- **Total: ~1GB download**

### **Step 4: Install Frontend Dependencies**
```bash
cd frontend
npm install
npm run build
cd ..
```

### **Step 5: Configure Groq API Key**
```powershell
# Windows PowerShell
$env:GROQ_API_KEY = "your_groq_api_key_here"

# Windows CMD
set GROQ_API_KEY=your_groq_api_key_here

# macOS/Linux
export GROQ_API_KEY="your_groq_api_key_here"
```

Or create `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```

### **Step 6: Start the Application**
```bash
python app.py
```

**Output:**
```
 * Running on http://127.0.0.1:5000
 * WARNING: This is a development server. Do not use it in production.
```

### **Step 7: Open in Browser**
```
http://localhost:5000
```

---

## 🚀 Quick Start

### **Minimal Setup (5 minutes)**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set API key
$env:GROQ_API_KEY = "your_key"

# 3. Start app
python app.py

# 4. Open browser
# http://localhost:5000
```

### **First Run Notes**
- ⏳ Models download on first run (~2-3 minutes)
- 📊 First inference takes ~3 seconds
- ⚡ Subsequent inferences: ~200-300ms
- 💾 Models cached in TensorFlow cache directory

---

## 💻 Usage

### **Web Interface**
1. **Home Page**
   - View application description
   - See key features
   - Click "Get Started"

2. **Scanner Page**
   - Upload medical image (PNG, JPG, JPEG, DICOM)
   - See real-time preview
   - Click "Analyze"
   - View results with confidence scores

3. **Results Display**
   - Ensemble confidence score
   - DenseNet121 predictions (top-5)
   - ResNet50 predictions (top-5)
   - Medical recommendations
   - Groq LLM analysis (if configured)

### **Keyboard Shortcuts**
- `Ctrl+L` - Focus upload area
- `Ctrl+R` - Reset form

---

## 🔌 API Endpoints

### **1. ML Analysis Endpoint**
```
POST /api/ml-analyze
```

**Request:**
```bash
curl -X POST http://localhost:5000/api/ml-analyze \
  -F "image=@medical_image.jpg"
```

**Response:**
```json
{
  "result": "<HTML formatted results>",
  "analysis": {
    "ensemble_confidence": 87.5,
    "densenet_result": {
      "model": "DenseNet121",
      "top_prediction": "chest X-ray",
      "confidence": 89.2,
      "predictions": [
        {"class": "chest X-ray", "confidence": 89.2},
        {"class": "X-ray", "confidence": 7.8}
      ]
    },
    "resnet_result": {
      "model": "ResNet50",
      "top_prediction": "X-ray",
      "confidence": 85.8,
      "predictions": [...]
    },
    "recommendation": "High confidence detection - Recommend clinical review"
  }
  }

  ## 🧪 ML Training (Optional)

  You can train a simple classifier using lightweight image statistics (mean, std, contrast, size) and then use it in the app.

  1. Prepare a CSV `labels.csv` with columns: `filename,label` (filename relative to images directory).
  2. Put images in a folder (for example `uploads/` or `train_images/`).
  3. Install training deps and run:

  ```powershell
  python -m pip install -r requirements.txt
  python train_model.py --images_dir uploads --labels labels.csv --output model.joblib
  ```

  4. Once `model.joblib` exists in the project root, the `/api/ml-analyze` endpoint will attempt to run the classifier and include a `model_info` field in responses.

  Notes:
  - The training script uses simple handcrafted features and a RandomForest classifier as a scaffold for experimentation; it's not a clinical model. You should collect labeled data and validate thoroughly before using in any decision-making.
}
```

### **2. Groq LLM Analysis Endpoint**
```
POST /api/analyze
```

**Request:**
```bash
curl -X POST http://localhost:5000/api/analyze \
  -F "image=@medical_image.jpg"
```

**Response:**
```json
{
  "result": "<HTML formatted markdown analysis>"
}
```

### **3. Health Check**
```
GET /
```

Returns React app or 404 if not built.

---

## 📁 Project Structure

```
AI Medical Imaging Diagnosis Agent/
├── app.py                          # Flask backend
├── ml_model.py                     # Deep learning models
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables
├── .gitignore                     # Git ignore rules
├── README.md                      # This file
├── ML_IMPLEMENTATION.md           # ML details
├── ARCHITECTURE.md                # System design
│
├── frontend/                      # React frontend
│   ├── package.json              # NPM dependencies
│   ├── public/
│   │   └── index.html            # HTML template
│   ├── src/
│   │   ├── index.js              # React entry point
│   │   ├── App.js                # Main component
│   │   └── App.css               # Styles
│   └── build/                    # Production build
│
├── uploads/                       # Uploaded images (temp)
│   └── *.jpg, *.png, *.dicom
│
└── templates/                     # Old templates (deprecated)
    └── index.html
```

---

## 🔄 Workflow

### **Complete User Journey**

```
1. USER OPENS APP
   ↓
   [React Frontend Loads]
   - Dark theme UI renders
   - Animations initialize
   - Home page displays

2. USER CLICKS "GET STARTED"
   ↓
   [Navigate to Scanner]
   - Upload area appears
   - Real-time preview ready

3. USER UPLOADS IMAGE
   ↓
   [Frontend Validation]
   - Check file type
   - Generate preview
   - Show file size

4. USER CLICKS "ANALYZE"
   ↓
   [Backend Processing]
   ├─ Save uploaded file
   ├─ Validate image
   ├─ Preprocess image (224x224)
   ├─ Run DenseNet121 inference
   ├─ Run ResNet50 inference
   ├─ Calculate ensemble score
   ├─ (Optional) Call Groq API
   └─ Format results as HTML

5. RESULTS DISPLAYED
   ├─ Ensemble Confidence: 87.5%
   ├─ DenseNet Predictions
   ├─ ResNet Predictions
   ├─ Medical Recommendations
   └─ Groq Analysis (if available)

6. USER ACTIONS
   ├─ Download results
   ├─ Analyze another image
   └─ Go back to home
```

### **Backend Processing Flow**

```
Image Upload
    ↓
[app.py: ml_analyze_image()]
    ↓
[File Validation]
- Check extension
- Check file size
- Save to uploads/
    ↓
[ml_model.py: get_analyzer()]
- Load DenseNet121 (if not loaded)
- Load ResNet50 (if not loaded)
    ↓
[Image Preprocessing]
- Read image (PIL)
- Resize to 224x224
- Convert to RGB
- Normalize (ImageNet)
- Batch expand
    ↓
[DenseNet121 Inference]
- Forward pass
- Get softmax output
- Decode predictions
- Top-5 results
    ↓
[ResNet50 Inference]
- Forward pass
- Get softmax output
- Decode predictions
- Top-5 results
    ↓
[Ensemble Aggregation]
- Average confidence scores
- Generate recommendation
- Format as HTML
    ↓
[Return JSON Response]
{
  "result": "<HTML>",
  "analysis": {...}
}
    ↓
[React Frontend]
- Display results
- Show animations
- Enable interactions
```

---

## 🎯 Key Technologies Explained

### **DenseNet121**
- **What**: Dense Convolutional Network with 121 layers
- **Why**: Efficient feature reuse, fewer parameters
- **Input**: 224x224 RGB image
- **Output**: 1000 class probabilities
- **Speed**: ~150ms inference

### **ResNet50**
- **What**: Residual Network with 50 layers
- **Why**: Deep architecture with skip connections
- **Input**: 224x224 RGB image
- **Output**: 1000 class probabilities
- **Speed**: ~150ms inference

### **Ensemble Method**
- **What**: Combine predictions from multiple models
- **Why**: Reduces variance, improves robustness
- **How**: Average confidence scores
- **Benefit**: More reliable predictions

### **Transfer Learning**
- **What**: Use pre-trained models on new task
- **Why**: Leverage ImageNet knowledge
- **How**: Fine-tune or use as-is
- **Benefit**: No need for large datasets

### **Groq API**
- **What**: Fast LLM inference service
- **Why**: Quick medical analysis
- **How**: Send base64 image + prompt
- **Benefit**: Detailed text analysis

---

## 🐛 Troubleshooting

### **Issue: Models not downloading**
```
Error: Failed to download model
```
**Solution:**
```bash
# Check internet connection
# Try manual download:
python -c "from tensorflow.keras.applications import DenseNet121; DenseNet121(weights='imagenet')"
```

### **Issue: Out of memory**
```
Error: CUDA out of memory
```
**Solution:**
```bash
# Use CPU instead
export CUDA_VISIBLE_DEVICES=""
python app.py
```

### **Issue: Slow inference**
```
First inference takes 5+ seconds
```
**Solution:**
- This is normal (model loading)
- Subsequent inferences are faster
- Use GPU for better performance

### **Issue: Groq API key error**
```
Error: Groq API Key not configured
```
**Solution:**
```powershell
$env:GROQ_API_KEY = "your_key"
python app.py
```

### **Issue: Port 5000 already in use**
```
Error: Address already in use
```
**Solution:**
```bash
# Use different port
python -c "from app import app; app.run(port=5001)"
```

### **Issue: CORS errors**
```
Error: Access-Control-Allow-Origin
```
**Solution:**
- Already configured in app.py
- Check browser console for details
- Ensure frontend and backend URLs match

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| DenseNet Inference | ~150ms |
| ResNet Inference | ~150ms |
| Ensemble Processing | ~300ms |
| Groq API Call | ~2-5s |
| Total Analysis | ~5-8s |
| Model Download | ~500MB |
| Model Load Time | ~2-3s (first run) |

---

## 🔐 Security Notes

- ⚠️ **Development Only**: Flask debug mode enabled
- 🔑 **API Key**: Store in environment variable, never commit
- 📁 **Uploads**: Temporary files in `uploads/` directory
- 🛡️ **CORS**: Enabled for development
- ✅ **File Validation**: Extension and size checks

---

## 📝 License

This project is provided as-is for educational and research purposes.

---

## 🤝 Support

For issues or questions:
1. Check troubleshooting section
2. Review ML_IMPLEMENTATION.md
3. Check error logs in console

---

## 🎓 Learning Resources

- **Transfer Learning**: https://cs231n.github.io/transfer-learning/
- **DenseNet Paper**: https://arxiv.org/abs/1608.06993
- **ResNet Paper**: https://arxiv.org/abs/1512.03385
- **ImageNet**: https://www.image-net.org/
- **Flask**: https://flask.palletsprojects.com/
- **React**: https://react.dev/
- **TensorFlow**: https://www.tensorflow.org/

---

**Last Updated**: October 27, 2025  
**Version**: 2.0 (with ML models)

