# Render.com Deployment Guide

**Platform**: Render.com  
**Status**: ✅ Recommended for your project  
**Date**: October 28, 2025

---

## Why Render.com?

✅ **Free Tier**: 750 hours/month free  
✅ **Full Stack**: Supports backend + frontend  
✅ **Easy Setup**: GitHub integration  
✅ **Reliable**: Good uptime  
✅ **Scalable**: Easy to upgrade  
✅ **No Credit Card**: For free tier  

---

## Step 1: Delete Current Deployments

### Delete from Vercel

**Via Dashboard**:
1. Go to: https://vercel.com/dashboard
2. Find "MediScannerAi" project
3. Click "Settings"
4. Scroll to "Danger Zone"
5. Click "Delete Project"
6. Confirm deletion

**Via CLI**:
```bash
vercel remove
```

### Delete from Railway

**Via Dashboard**:
1. Go to: https://railway.app/dashboard
2. Find your project
3. Click "Settings"
4. Click "Delete Project"
5. Confirm deletion

**Via CLI**:
```bash
railway down
```

---

## Step 2: Create Render Account

1. Go to: https://render.com
2. Click "Sign up"
3. Choose "Sign up with GitHub"
4. Authorize GitHub access
5. Complete profile setup

---

## Step 3: Deploy Backend on Render

### Create Web Service

1. **Go to Dashboard**
   - Click "New +"
   - Select "Web Service"

2. **Connect Repository**
   - Select your GitHub repository
   - Select branch: `main`
   - Click "Connect"

3. **Configure Service**
   - **Name**: `mediscanner-backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:5000`
   - **Plan**: Free
   - Click "Create Web Service"

4. **Add Environment Variables**
   - Go to "Environment"
   - Add variables:
     ```
     FLASK_ENV=production
     GROQ_API_KEY=your_groq_api_key_here
     ```
   - Click "Save"

5. **Wait for Deployment**
   - Monitor build logs
   - Should complete in 2-5 minutes
   - Check for errors

### Verify Backend

```bash
# Test health endpoint
curl https://mediscanner-backend.onrender.com/health

# Expected response:
# {"status": "ok", "message": "Backend is running"}
```

---

## Step 4: Deploy Frontend on Render

### Create Static Site

1. **Go to Dashboard**
   - Click "New +"
   - Select "Static Site"

2. **Connect Repository**
   - Select your GitHub repository
   - Select branch: `main`
   - Click "Connect"

3. **Configure Site**
   - **Name**: `mediscanner-frontend`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/build`
   - Click "Create Static Site"

4. **Add Environment Variables**
   - Go to "Environment"
   - Add:
     ```
     REACT_APP_API_URL=https://mediscanner-backend.onrender.com
     ```
   - Click "Save"

5. **Wait for Deployment**
   - Monitor build logs
   - Should complete in 2-5 minutes
   - Check for errors

### Verify Frontend

- Go to: `https://mediscanner-frontend.onrender.com`
- Should see MediScanner AI interface
- Check browser console for errors

---

## Step 5: Connect Frontend to Backend

### Update Frontend Configuration

**File**: `frontend/src/App.js`

```javascript
// Line 348 - Update API URL
const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Use in API calls
const response = await axios.post(`${apiUrl}/api/ml-analyze`, formData, {
  headers: {
    'Content-Type': 'multipart/form-data',
  },
  timeout: 30000,
});
```

### Update Environment Variables

**Frontend Environment** (Render Dashboard):
```
REACT_APP_API_URL=https://mediscanner-backend.onrender.com
```

**Backend Environment** (Render Dashboard):
```
FLASK_ENV=production
GROQ_API_KEY=your_key_here
```

---

## Step 6: Test Deployment

### Test Backend

```bash
# Health check
curl https://mediscanner-backend.onrender.com/health

# Test ML endpoint
curl -X POST \
  -F "image=@test_image.jpg" \
  https://mediscanner-backend.onrender.com/api/ml-analyze
```

### Test Frontend

1. Go to: `https://mediscanner-frontend.onrender.com`
2. Upload a medical image
3. Click "Analyze Image"
4. Check results appear
5. Check browser console for errors

### Check Logs

**Backend Logs**:
1. Go to Render Dashboard
2. Click "mediscanner-backend"
3. Click "Logs"
4. Monitor for errors

**Frontend Logs**:
1. Go to Render Dashboard
2. Click "mediscanner-frontend"
3. Click "Logs"
4. Monitor for errors

---

## Handling ML Models

### Challenge
Models are large (150MB+), free tier has limited storage

### Solution 1: Download at Runtime (Recommended)

**Update app.py**:
```python
import os
from pathlib import Path

def ensure_models_exist():
    """Download models if they don't exist"""
    model_dir = Path("models")
    
    if not model_dir.exists():
        print("Downloading models...")
        os.system("python download_models.py")
    
    # Check if models exist
    if not (model_dir / "densenet_chexpert.h5").exists():
        print("Models not found, downloading...")
        os.system("python download_models.py")

# Call before loading models
ensure_models_exist()

# Then load models
analyzer = get_analyzer()
```

### Solution 2: Use Model Caching

```python
import functools

@functools.lru_cache(maxsize=1)
def get_cached_analyzer():
    """Cache models in memory"""
    return get_analyzer()

# Use cached version
analyzer = get_cached_analyzer()
```

### Solution 3: Use Smaller Models

- Use MobileNetV2 instead of DenseNet121
- Implement model quantization
- Use model compression

---

## Configuration Files

### Create render.yaml

**File**: `render.yaml`

```yaml
services:
  - type: web
    name: mediscanner-backend
    env: python
    region: oregon
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --bind 0.0.0.0:5000
    envVars:
      - key: FLASK_ENV
        value: production
      - key: GROQ_API_KEY
        scope: secret

  - type: static
    name: mediscanner-frontend
    staticPublishPath: frontend/build
    buildCommand: cd frontend && npm install && npm run build
    routes:
      - path: /*
        destination: /index.html
    envVars:
      - key: REACT_APP_API_URL
        value: https://mediscanner-backend.onrender.com
```

### Create Dockerfile

**File**: `Dockerfile`

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create models directory
RUN mkdir -p models

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--timeout", "120"]
```

---

## Troubleshooting

### Backend Not Starting

**Check Logs**:
1. Go to Render Dashboard
2. Click "mediscanner-backend"
3. Click "Logs"
4. Look for error messages

**Common Issues**:
- Missing dependencies: Check requirements.txt
- Python version: Ensure Python 3.9+
- Port binding: Ensure port 5000 is used
- Gunicorn: Ensure gunicorn is installed

**Solution**:
```bash
# Update requirements.txt
pip freeze > requirements.txt

# Push to GitHub
git add requirements.txt
git commit -m "Update dependencies"
git push origin main

# Render will auto-redeploy
```

### Frontend Not Loading

**Check Logs**:
1. Go to Render Dashboard
2. Click "mediscanner-frontend"
3. Click "Logs"
4. Look for build errors

**Common Issues**:
- Build command wrong: Check npm scripts
- API URL wrong: Check environment variable
- Missing files: Check build directory

**Solution**:
```bash
# Test build locally
cd frontend
npm install
npm run build

# Check build output
ls -la build/

# Push to GitHub
git add .
git commit -m "Fix frontend build"
git push origin main
```

### API Connection Failed

**Check**:
1. Backend URL is correct
2. Environment variable is set
3. Backend is running
4. CORS is enabled

**Solution**:
```python
# In app.py, ensure CORS is enabled
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

### Models Not Loading

**Check**:
1. Storage space available
2. Models directory exists
3. Download script works
4. Memory is sufficient

**Solution**:
```python
# Add error handling
try:
    analyzer = get_analyzer()
except Exception as e:
    print(f"Error loading models: {e}")
    # Download models
    os.system("python download_models.py")
    analyzer = get_analyzer()
```

---

## Performance Tips

### Optimize Backend
- Use caching for models
- Implement request timeout
- Monitor memory usage
- Use async processing

### Optimize Frontend
- Lazy load components
- Minimize bundle size
- Use compression
- Cache static assets

### Optimize Models
- Use smaller models
- Implement quantization
- Use model caching
- Batch predictions

---

## Monitoring

### Check Status

**Backend**:
```bash
curl https://mediscanner-backend.onrender.com/health
```

**Frontend**:
```bash
curl https://mediscanner-frontend.onrender.com
```

### Monitor Logs

1. Go to Render Dashboard
2. Click service name
3. Click "Logs"
4. Monitor for errors

### Check Metrics

1. Go to Render Dashboard
2. Click service name
3. Click "Metrics"
4. Monitor CPU, memory, requests

---

## Upgrading from Free Tier

If you need more resources:

1. **Paid Plans**:
   - Starter: $7/month
   - Standard: $12/month
   - Pro: $25/month

2. **Benefits**:
   - Always running (no spin-down)
   - More memory (1GB+)
   - More storage
   - Better performance

3. **Upgrade Steps**:
   - Go to Render Dashboard
   - Click service
   - Click "Settings"
   - Change plan
   - Confirm upgrade

---

## Summary

✅ **Delete Vercel & Railway deployments**  
✅ **Create Render account**  
✅ **Deploy backend as Web Service**  
✅ **Deploy frontend as Static Site**  
✅ **Configure environment variables**  
✅ **Test both services**  
✅ **Monitor logs**  
✅ **Ready for production**  

---

## Quick Links

- **Render Dashboard**: https://render.com/dashboard
- **Render Docs**: https://render.com/docs
- **GitHub Integration**: https://render.com/docs/github
- **Environment Variables**: https://render.com/docs/environment-variables

---

**Status**: ✅ Ready to Deploy  
**Estimated Time**: 15-20 minutes  
**Cost**: Free (750 hours/month)
