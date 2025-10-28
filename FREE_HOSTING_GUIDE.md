# Free Hosting Platforms Guide - Backend + Frontend + ML Models

**Date**: October 28, 2025  
**Purpose**: Deploy full-stack application with trained ML models on free platforms

---

## Best Free Hosting Options

### 1. **Render.com** ⭐ RECOMMENDED
**Best for**: Full-stack applications with backend + frontend

#### Pros
- ✅ Free tier with generous limits
- ✅ Supports Python/Flask backend
- ✅ Supports Node.js frontend
- ✅ Free SSL certificate
- ✅ Auto-deploy from GitHub
- ✅ 750 hours/month free
- ✅ Can host both backend and frontend
- ✅ Supports environment variables
- ✅ Easy deployment process

#### Cons
- ❌ Spins down after 15 minutes of inactivity (free tier)
- ❌ Limited to 512MB RAM
- ❌ Limited storage

#### Deployment Steps

**1. Create Render Account**
- Go to: https://render.com
- Sign up with GitHub

**2. Deploy Backend**
- Click "New +" → "Web Service"
- Connect GitHub repository
- Select branch: main
- Environment: Python 3
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Plan: Free
- Deploy

**3. Deploy Frontend**
- Click "New +" → "Static Site"
- Connect GitHub repository
- Build command: `cd frontend && npm install && npm run build`
- Publish directory: `frontend/build`
- Deploy

**4. Configure Environment Variables**
Backend:
```
GROQ_API_KEY=your_key_here
FLASK_ENV=production
```

Frontend (.env):
```
REACT_APP_API_URL=https://your-backend-url.onrender.com
```

---

### 2. **Heroku** (With Free Tier Alternatives)
**Note**: Heroku removed free tier in Nov 2022

**Alternative**: Use Heroku CLI with GitHub Actions for free deployment

---

### 3. **PythonAnywhere** ⭐ GOOD FOR BACKEND
**Best for**: Python backend hosting

#### Pros
- ✅ Free tier available
- ✅ Python-specific hosting
- ✅ Easy Flask deployment
- ✅ 100MB storage free
- ✅ 1 web app free

#### Cons
- ❌ Limited to Python backend only
- ❌ No Node.js support
- ❌ Limited storage

#### Deployment Steps
1. Go to: https://www.pythonanywhere.com
2. Create free account
3. Upload code
4. Configure Flask app
5. Set environment variables
6. Deploy

---

### 4. **Replit** ⭐ GOOD FOR TESTING
**Best for**: Quick testing and prototyping

#### Pros
- ✅ Free tier available
- ✅ Supports Python + Node.js
- ✅ Easy to use
- ✅ Built-in IDE
- ✅ Can run both backend and frontend

#### Cons
- ❌ Spins down after inactivity
- ❌ Limited resources
- ❌ Not ideal for production

#### Deployment Steps
1. Go to: https://replit.com
2. Create new Repl
3. Select Python
4. Upload code
5. Run application
6. Share public URL

---

### 5. **Fly.io** ⭐ RECOMMENDED
**Best for**: Full-stack applications

#### Pros
- ✅ Free tier with 3 shared-cpu-1x 256MB VMs
- ✅ Supports Docker
- ✅ Global deployment
- ✅ Easy scaling
- ✅ Good for ML models

#### Cons
- ❌ Requires Docker knowledge
- ❌ Limited free resources

#### Deployment Steps
1. Install Fly CLI: `brew install flyctl`
2. Create account: `flyctl auth signup`
3. Initialize app: `flyctl launch`
4. Deploy: `flyctl deploy`

---

### 6. **Railway.app** (Your Current Platform)
**Issue**: Backend not running properly

**Solutions**:
1. Check Dockerfile configuration
2. Verify environment variables
3. Check build logs for errors
4. Ensure gunicorn is installed

---

### 7. **Glitch.com**
**Best for**: Quick prototyping

#### Pros
- ✅ Free tier
- ✅ Supports Node.js and Python
- ✅ Easy to use
- ✅ Live editing

#### Cons
- ❌ Limited resources
- ❌ Spins down after inactivity

---

## Recommended Setup: Render.com

### Why Render?
✅ Best free tier for full-stack apps  
✅ Supports both backend and frontend  
✅ Easy GitHub integration  
✅ Good documentation  
✅ Reliable uptime  

### Step-by-Step Deployment

#### 1. Prepare Your Code

**Backend (app.py)**:
```python
import os
from flask import Flask

app = Flask(__name__)

# Use environment variables
DEBUG = os.getenv('FLASK_ENV') != 'production'
PORT = int(os.getenv('PORT', 5000))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
```

**Frontend (.env.production)**:
```
REACT_APP_API_URL=https://your-backend.onrender.com
```

#### 2. Create Render Account
- Go to: https://render.com
- Sign up with GitHub
- Authorize GitHub access

#### 3. Deploy Backend

**Create Web Service**:
1. Click "New +" → "Web Service"
2. Select your GitHub repository
3. Configure:
   - Name: `mediscanner-backend`
   - Environment: Python 3
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
   - Plan: Free
4. Click "Create Web Service"

**Add Environment Variables**:
1. Go to "Environment"
2. Add:
   ```
   GROQ_API_KEY=your_key
   FLASK_ENV=production
   ```

#### 4. Deploy Frontend

**Create Static Site**:
1. Click "New +" → "Static Site"
2. Select your GitHub repository
3. Configure:
   - Name: `mediscanner-frontend`
   - Build command: `cd frontend && npm install && npm run build`
   - Publish directory: `frontend/build`
4. Click "Create Static Site"

**Add Environment Variables**:
1. Go to "Environment"
2. Add:
   ```
   REACT_APP_API_URL=https://mediscanner-backend.onrender.com
   ```

#### 5. Connect Frontend to Backend
Update `frontend/src/App.js`:
```javascript
const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:5000';
```

#### 6. Test Deployment
- Frontend: `https://mediscanner-frontend.onrender.com`
- Backend: `https://mediscanner-backend.onrender.com/health`

---

## Handling ML Models on Free Tier

### Challenge
ML models are large (150MB+) and free tier has limited storage

### Solutions

#### Option 1: Download Models at Runtime
```python
# In app.py
import os
from pathlib import Path

def download_models_if_needed():
    if not Path("models/densenet_chexpert.h5").exists():
        print("Downloading models...")
        os.system("python download_models.py")

# Call before loading models
download_models_if_needed()
```

#### Option 2: Use Model Caching
```python
# Cache models in memory
import functools

@functools.lru_cache(maxsize=1)
def load_models():
    # Load models once
    return get_analyzer()
```

#### Option 3: Use Smaller Models
- Use MobileNetV2 instead of DenseNet121
- Quantize models for smaller size
- Use model compression

#### Option 4: Use External Storage
- Upload models to GitHub LFS
- Download from cloud storage (Google Drive, AWS S3)
- Use model serving platforms

---

## Deleting Current Deployments

### Delete from Vercel

**Method 1: Via Dashboard**
1. Go to: https://vercel.com/dashboard
2. Find your project
3. Click "Settings"
4. Scroll to "Danger Zone"
5. Click "Delete Project"

**Method 2: Via CLI**
```bash
vercel remove
```

### Delete from Railway

**Method 1: Via Dashboard**
1. Go to: https://railway.app/dashboard
2. Find your project
3. Click "Settings"
4. Click "Delete Project"

**Method 2: Via CLI**
```bash
railway down
```

---

## Comparison Table

| Platform | Backend | Frontend | Free Tier | Models | Recommendation |
|----------|---------|----------|-----------|--------|-----------------|
| Render | ✅ | ✅ | ✅ Good | ⚠️ Limited | ⭐⭐⭐⭐⭐ |
| Fly.io | ✅ | ✅ | ✅ Good | ✅ Good | ⭐⭐⭐⭐ |
| Railway | ✅ | ✅ | ✅ Limited | ⚠️ Limited | ⭐⭐⭐ |
| PythonAnywhere | ✅ | ❌ | ✅ Limited | ⚠️ Limited | ⭐⭐⭐ |
| Replit | ✅ | ✅ | ✅ Limited | ⚠️ Limited | ⭐⭐⭐ |
| Glitch | ✅ | ✅ | ✅ Limited | ⚠️ Limited | ⭐⭐ |

---

## Configuration Files for Render

### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
```

### render.yaml
```yaml
services:
  - type: web
    name: mediscanner-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --bind 0.0.0.0:5000
    envVars:
      - key: FLASK_ENV
        value: production
      - key: GROQ_API_KEY
        scope: secret

  - type: static
    name: mediscanner-frontend
    buildCommand: cd frontend && npm install && npm run build
    staticPublishPath: frontend/build
    envVars:
      - key: REACT_APP_API_URL
        value: https://mediscanner-backend.onrender.com
```

---

## Recommended Deployment Plan

### Step 1: Delete Current Deployments
```bash
# Delete Vercel
vercel remove

# Delete Railway
railway down
```

### Step 2: Deploy on Render
1. Create Render account
2. Deploy backend as Web Service
3. Deploy frontend as Static Site
4. Configure environment variables
5. Test both services

### Step 3: Update GitHub
```bash
git add render.yaml
git commit -m "Add Render deployment configuration"
git push origin main
```

### Step 4: Monitor Deployment
- Check Render dashboard
- Monitor logs
- Test API endpoints
- Verify frontend loads

---

## Troubleshooting

### Backend Not Starting
1. Check build logs
2. Verify Python version
3. Check requirements.txt
4. Verify gunicorn installation
5. Check environment variables

### Frontend Not Loading
1. Check build logs
2. Verify npm dependencies
3. Check build command
4. Verify publish directory
5. Check API URL configuration

### Models Not Loading
1. Check storage space
2. Verify model files exist
3. Check download script
4. Monitor memory usage
5. Consider model compression

---

## Cost Comparison

| Platform | Monthly Cost (Free) | Storage | Bandwidth |
|----------|-------------------|---------|-----------|
| Render | $0 | 512MB | Unlimited |
| Fly.io | $0 | 3GB | Limited |
| Railway | $0 | Limited | Limited |
| PythonAnywhere | $0 | 100MB | Limited |
| Replit | $0 | Limited | Limited |

---

## Next Steps

1. **Delete Current Deployments**
   - Remove from Vercel
   - Remove from Railway

2. **Choose Platform**
   - Recommended: Render.com

3. **Prepare Code**
   - Update environment variables
   - Create configuration files
   - Test locally

4. **Deploy**
   - Create accounts
   - Deploy backend
   - Deploy frontend
   - Configure variables

5. **Test**
   - Check backend health
   - Test API endpoints
   - Verify frontend loads
   - Test model inference

6. **Monitor**
   - Check logs
   - Monitor performance
   - Watch for errors

---

## Support Resources

- **Render Docs**: https://render.com/docs
- **Fly.io Docs**: https://fly.io/docs
- **Flask Deployment**: https://flask.palletsprojects.com/deployment/
- **React Deployment**: https://create-react-app.dev/deployment/

---

**Recommendation**: Use **Render.com** for best free tier experience with both backend and frontend support.

**Status**: Ready to deploy  
**Date**: October 28, 2025
