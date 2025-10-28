# Deployment Migration Plan

**Current Status**: Vercel + Railway (Issues)  
**Target**: Render.com (Free, Full-Stack)  
**Date**: October 28, 2025

---

## Executive Summary

You want to:
1. ✅ Delete Vercel deployment (frontend only)
2. ✅ Delete Railway deployment (backend issues)
3. ✅ Deploy on new free platform supporting backend + frontend + models
4. ✅ Keep all trained models and data

**Solution**: Migrate to **Render.com**

---

## Why Render.com?

| Feature | Vercel | Railway | Render |
|---------|--------|---------|--------|
| Backend Support | ❌ No | ⚠️ Issues | ✅ Yes |
| Frontend Support | ✅ Yes | ✅ Yes | ✅ Yes |
| Free Tier | ✅ Yes | ✅ Yes | ✅ Yes (750h/mo) |
| ML Models | ❌ Limited | ⚠️ Limited | ✅ Good |
| Ease of Use | ✅ Easy | ⚠️ Complex | ✅ Easy |
| GitHub Integration | ✅ Yes | ✅ Yes | ✅ Yes |
| Recommendation | ❌ Frontend only | ⚠️ Problematic | ✅⭐ BEST |

---

## Migration Steps

### Phase 1: Delete Current Deployments (5 minutes)

#### Delete from Vercel
```bash
# Option 1: Via CLI
vercel remove

# Option 2: Via Dashboard
# 1. Go to https://vercel.com/dashboard
# 2. Find "MediScannerAi" project
# 3. Settings → Danger Zone → Delete Project
```

#### Delete from Railway
```bash
# Option 1: Via CLI
railway down

# Option 2: Via Dashboard
# 1. Go to https://railway.app/dashboard
# 2. Find your project
# 3. Settings → Delete Project
```

### Phase 2: Prepare Code (5 minutes)

**Ensure these files exist**:
- ✅ `requirements.txt` - Python dependencies
- ✅ `app.py` - Flask backend
- ✅ `frontend/package.json` - Node dependencies
- ✅ `frontend/src/App.js` - React frontend
- ✅ `ml_model.py` - Trained models
- ✅ `download_models.py` - Model downloader

**Update environment variables**:
```bash
# Create .env.production
FLASK_ENV=production
GROQ_API_KEY=your_key_here
REACT_APP_API_URL=https://mediscanner-backend.onrender.com
```

### Phase 3: Create Render Account (2 minutes)

1. Go to: https://render.com
2. Click "Sign up"
3. Choose "Sign up with GitHub"
4. Authorize GitHub access
5. Complete profile

### Phase 4: Deploy Backend (5 minutes)

1. **Create Web Service**
   - Click "New +" → "Web Service"
   - Select your GitHub repository
   - Select branch: `main`

2. **Configure**
   - Name: `mediscanner-backend`
   - Environment: Python 3
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app --bind 0.0.0.0:5000`
   - Plan: Free

3. **Environment Variables**
   - `FLASK_ENV=production`
   - `GROQ_API_KEY=your_key`

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (2-5 minutes)

### Phase 5: Deploy Frontend (5 minutes)

1. **Create Static Site**
   - Click "New +" → "Static Site"
   - Select your GitHub repository
   - Select branch: `main`

2. **Configure**
   - Name: `mediscanner-frontend`
   - Build: `cd frontend && npm install && npm run build`
   - Publish: `frontend/build`

3. **Environment Variables**
   - `REACT_APP_API_URL=https://mediscanner-backend.onrender.com`

4. **Deploy**
   - Click "Create Static Site"
   - Wait for deployment (2-5 minutes)

### Phase 6: Test & Verify (5 minutes)

**Test Backend**:
```bash
curl https://mediscanner-backend.onrender.com/health
# Expected: {"status": "ok", "message": "Backend is running"}
```

**Test Frontend**:
- Go to: `https://mediscanner-frontend.onrender.com`
- Should see MediScanner AI interface
- Upload image and test analysis

**Test API Connection**:
1. Open frontend
2. Upload medical image
3. Click "Analyze Image"
4. Check results appear
5. Check browser console (F12) for errors

---

## Handling ML Models

### Challenge
Models are ~150MB, free tier has limited storage

### Solution: Download at Runtime

**Update app.py**:
```python
import os
from pathlib import Path

def ensure_models_exist():
    """Download models if not present"""
    model_dir = Path("models")
    
    if not (model_dir / "densenet_chexpert.h5").exists():
        print("Downloading models...")
        os.system("python download_models.py")

# Call before loading models
ensure_models_exist()
analyzer = get_analyzer()
```

**Benefits**:
- ✅ Models downloaded on first request
- ✅ Saves storage space
- ✅ Automatic updates
- ✅ Works on free tier

---

## Timeline

| Phase | Task | Time | Status |
|-------|------|------|--------|
| 1 | Delete Vercel & Railway | 5 min | Ready |
| 2 | Prepare code | 5 min | Ready |
| 3 | Create Render account | 2 min | Ready |
| 4 | Deploy backend | 5 min | Ready |
| 5 | Deploy frontend | 5 min | Ready |
| 6 | Test & verify | 5 min | Ready |
| **Total** | **Complete migration** | **27 min** | **Ready** |

---

## Costs

### Render.com Free Tier
- **Price**: $0/month
- **Hours**: 750 hours/month
- **Services**: 2 (backend + frontend)
- **Storage**: 512MB per service
- **Bandwidth**: Unlimited
- **SSL**: Free

### When to Upgrade
- If you need always-on (no spin-down)
- If you need more memory (>512MB)
- If you need more storage
- Paid plans start at $7/month

---

## Troubleshooting

### Backend Not Starting
**Check**:
1. Build logs for errors
2. requirements.txt is complete
3. gunicorn is installed
4. Port 5000 is used

**Fix**:
```bash
# Update requirements
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push origin main
# Render will auto-redeploy
```

### Frontend Not Loading
**Check**:
1. Build logs for errors
2. npm dependencies installed
3. API URL environment variable set
4. Build directory is correct

**Fix**:
```bash
# Test locally
cd frontend
npm install
npm run build

# Push to GitHub
git add .
git commit -m "Fix frontend"
git push origin main
```

### API Connection Failed
**Check**:
1. Backend is running
2. API URL is correct
3. CORS is enabled
4. Environment variable is set

**Fix**:
```python
# In app.py
from flask_cors import CORS
CORS(app)
```

### Models Not Loading
**Check**:
1. Storage space available
2. Download script works
3. Memory is sufficient

**Fix**:
```python
# Add to app.py
def ensure_models_exist():
    if not Path("models/densenet_chexpert.h5").exists():
        os.system("python download_models.py")
```

---

## Post-Deployment

### Monitor
- Check Render dashboard daily
- Monitor logs for errors
- Check performance metrics
- Watch for spin-downs

### Maintain
- Update dependencies monthly
- Check for security patches
- Monitor storage usage
- Backup important data

### Scale
- Upgrade plan if needed
- Add caching if slow
- Optimize models if needed
- Consider CDN for frontend

---

## Comparison: Before vs After

### Before (Current Issues)
- ❌ Vercel: Frontend only
- ❌ Railway: Backend not running
- ❌ Models not working
- ❌ API connection issues
- ❌ Deployment problems

### After (Render)
- ✅ Backend running properly
- ✅ Frontend loading correctly
- ✅ Models working
- ✅ API connected
- ✅ Full-stack working

---

## Success Criteria

After migration, you should have:
- ✅ Backend running at: `https://mediscanner-backend.onrender.com`
- ✅ Frontend running at: `https://mediscanner-frontend.onrender.com`
- ✅ API endpoints responding
- ✅ Models loading and working
- ✅ Image upload and analysis working
- ✅ No console errors
- ✅ Responsive design working

---

## Quick Reference

### Render Dashboard
https://render.com/dashboard

### Backend URL
`https://mediscanner-backend.onrender.com`

### Frontend URL
`https://mediscanner-frontend.onrender.com`

### Health Check
```bash
curl https://mediscanner-backend.onrender.com/health
```

### View Logs
1. Go to Render Dashboard
2. Click service name
3. Click "Logs"

---

## Next Actions

1. **Now**: Read this document
2. **5 min**: Delete Vercel & Railway deployments
3. **2 min**: Create Render account
4. **5 min**: Deploy backend
5. **5 min**: Deploy frontend
6. **5 min**: Test everything
7. **Done**: You have working full-stack app!

---

## Support

### Documentation
- `FREE_HOSTING_GUIDE.md` - All free hosting options
- `RENDER_DEPLOYMENT.md` - Detailed Render guide
- `DEPLOYMENT_GUIDE.md` - General deployment guide

### Resources
- Render Docs: https://render.com/docs
- Flask Docs: https://flask.palletsprojects.com
- React Docs: https://react.dev

---

## Summary

✅ **Migration Plan Ready**
- Delete Vercel & Railway
- Deploy on Render.com
- Full-stack support
- ML models included
- Free tier available
- ~27 minutes total

**Status**: Ready to execute  
**Recommendation**: Start migration now  
**Expected Result**: Working full-stack app with trained models

---

**Document**: Deployment Migration Plan  
**Date**: October 28, 2025  
**Status**: ✅ Ready for Implementation
