# Deployment Guide - AI Medical Imaging Diagnosis Agent

**Version**: 2.0 (Trained Medical Models)  
**Status**: ✅ Ready for Deployment  
**Date**: October 28, 2025

---

## Quick Start (Local Development)

### 1. Install Dependencies
```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### 2. Download Trained Models
```bash
python download_models.py
```

### 3. Start Backend
```bash
python app.py
```
Backend will run on: `http://localhost:5000`

### 4. Start Frontend (Development)
```bash
cd frontend
npm start
```
Frontend will run on: `http://localhost:3000`

### 5. Access Application
Open browser: `http://localhost:3000`

---

## Production Deployment

### Option 1: Local Production Build

#### Build Frontend
```bash
cd frontend
npm run build
```

#### Serve Frontend (Production)
```bash
npm install -g serve
serve -s build
```

#### Run Backend (Production)
```bash
python app.py
```

#### Access Application
```
http://localhost:3000
```

### Option 2: Docker Deployment

#### Create Dockerfile (Backend)
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

#### Create Dockerfile (Frontend)
```dockerfile
FROM node:16-alpine AS build

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install

COPY frontend .
RUN npm run build

FROM node:16-alpine

WORKDIR /app

RUN npm install -g serve

COPY --from=build /app/build ./build

EXPOSE 3000

CMD ["serve", "-s", "build"]
```

#### Build and Run Docker Images
```bash
# Backend
docker build -t mediscanner-backend .
docker run -p 5000:5000 mediscanner-backend

# Frontend
docker build -f Dockerfile.frontend -t mediscanner-frontend .
docker run -p 3000:3000 mediscanner-frontend
```

### Option 3: Vercel Deployment (Frontend)

#### Install Vercel CLI
```bash
npm install -g vercel
```

#### Deploy
```bash
cd frontend
vercel --prod
```

#### Configure Environment Variables
```
REACT_APP_API_URL=https://your-backend-url.com
```

### Option 4: Netlify Deployment (Frontend)

#### Install Netlify CLI
```bash
npm install -g netlify-cli
```

#### Deploy
```bash
cd frontend
netlify deploy --prod --dir=build
```

#### Configure Environment Variables
In Netlify dashboard:
```
REACT_APP_API_URL=https://your-backend-url.com
```

### Option 5: Railway Deployment

#### Backend Deployment
1. Connect GitHub repository to Railway
2. Select Python as runtime
3. Set environment variables:
   ```
   GROQ_API_KEY=your_key_here
   ```
4. Deploy

#### Frontend Deployment
1. Connect GitHub repository to Railway
2. Select Node.js as runtime
3. Set build command: `cd frontend && npm run build`
4. Set start command: `serve -s frontend/build`
5. Deploy

---

## Environment Variables

### Backend (.env)
```bash
# Optional: Groq API Key for LLM analysis
GROQ_API_KEY=your_groq_api_key

# Flask Configuration
FLASK_ENV=production
DEBUG=False
```

### Frontend (.env)
```bash
# API URL
REACT_APP_API_URL=http://localhost:5000
# or for production
REACT_APP_API_URL=https://your-backend-url.com
```

---

## Pre-Deployment Checklist

### Backend
- [ ] Python 3.8+ installed
- [ ] All dependencies in requirements.txt
- [ ] Trained models downloaded (`python download_models.py`)
- [ ] GROQ_API_KEY set (optional)
- [ ] Port 5000 available
- [ ] No hardcoded paths

### Frontend
- [ ] Node.js 14+ installed
- [ ] npm dependencies installed
- [ ] Build successful (`npm run build`)
- [ ] Environment variables configured
- [ ] API URL correct
- [ ] No console errors

### General
- [ ] Git repository initialized
- [ ] .gitignore configured
- [ ] README.md updated
- [ ] Documentation complete
- [ ] Security headers configured
- [ ] CORS properly configured

---

## Production Configuration

### CORS Setup (Backend)
```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-frontend-url.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

### Security Headers (Backend)
```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

### Performance Optimization (Frontend)
- Gzip compression enabled
- Code splitting configured
- Lazy loading implemented
- Caching headers set
- CDN recommended

---

## Monitoring & Logging

### Backend Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Frontend Error Tracking
```javascript
// Add error tracking service
// Example: Sentry, LogRocket, etc.
```

### Health Check Endpoint
```bash
curl http://localhost:5000/health
```

---

## Scaling Considerations

### Horizontal Scaling
- Use load balancer (nginx, HAProxy)
- Multiple backend instances
- Shared model cache
- Database for results

### Vertical Scaling
- Increase server resources
- GPU acceleration for inference
- Larger memory for model loading
- SSD for faster I/O

### Caching Strategy
- Cache model predictions
- Cache frequent analyses
- Redis for distributed cache
- CDN for static assets

---

## Troubleshooting

### Backend Issues

**Port already in use**:
```bash
# Find process using port 5000
lsof -i :5000
# Kill process
kill -9 <PID>
```

**Models not loading**:
```bash
# Download models
python download_models.py

# Verify models exist
ls -la models/
```

**API errors**:
```bash
# Check logs
tail -f app.log

# Test endpoint
curl http://localhost:5000/health
```

### Frontend Issues

**Build fails**:
```bash
# Clear cache
npm cache clean --force

# Reinstall
rm -rf node_modules package-lock.json
npm install

# Rebuild
npm run build
```

**API connection fails**:
```bash
# Check backend running
curl http://localhost:5000/health

# Check environment variable
echo $REACT_APP_API_URL

# Update .env if needed
REACT_APP_API_URL=http://localhost:5000
```

**Port 3000 in use**:
```bash
# Use different port
PORT=3001 npm start
```

---

## Performance Benchmarks

### Expected Performance
- **Frontend Load Time**: < 2 seconds
- **API Response Time**: 1-3 seconds
- **Model Inference**: ~270ms (ensemble)
- **Memory Usage**: ~2GB (models loaded)
- **CPU Usage**: 20-40% during inference

### Optimization Tips
1. Use GPU for faster inference
2. Implement caching layer
3. Use CDN for static assets
4. Enable gzip compression
5. Minimize API calls
6. Lazy load components

---

## Backup & Recovery

### Database Backup
```bash
# If using database
mysqldump -u user -p database > backup.sql
```

### Model Backup
```bash
# Backup trained models
tar -czf models_backup.tar.gz models/
```

### Configuration Backup
```bash
# Backup environment files
cp .env .env.backup
```

---

## Security Considerations

### API Security
- [ ] HTTPS enabled
- [ ] API rate limiting
- [ ] Input validation
- [ ] SQL injection prevention
- [ ] CORS properly configured
- [ ] Authentication if needed

### Data Security
- [ ] Uploaded images deleted after processing
- [ ] No sensitive data logged
- [ ] Secure file storage
- [ ] Encryption for sensitive data
- [ ] Regular security audits

### Infrastructure Security
- [ ] Firewall configured
- [ ] SSH key authentication
- [ ] Regular backups
- [ ] Security patches updated
- [ ] Monitoring enabled

---

## Maintenance

### Regular Tasks
- [ ] Monitor logs daily
- [ ] Check disk space weekly
- [ ] Update dependencies monthly
- [ ] Security patches immediately
- [ ] Performance monitoring continuous

### Backup Schedule
- [ ] Daily: Configuration
- [ ] Weekly: Models and data
- [ ] Monthly: Full system backup

---

## Support & Resources

### Documentation
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick commands
- [SETUP_TRAINED_MODELS.md](SETUP_TRAINED_MODELS.md) - Setup guide
- [MEDICAL_MODELS.md](MEDICAL_MODELS.md) - Model documentation
- [README_TRAINED_MODELS.md](README_TRAINED_MODELS.md) - Main documentation

### External Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [TensorFlow Documentation](https://www.tensorflow.org/)
- [Docker Documentation](https://docs.docker.com/)

---

## Deployment Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] Environment variables set
- [ ] Security checks passed
- [ ] Performance benchmarks met

### Deployment
- [ ] Backend deployed
- [ ] Frontend deployed
- [ ] Environment variables configured
- [ ] Health checks passing
- [ ] Monitoring enabled
- [ ] Backups created

### Post-Deployment
- [ ] Smoke tests passed
- [ ] User acceptance testing
- [ ] Performance monitoring
- [ ] Error tracking active
- [ ] Documentation updated
- [ ] Team notified

---

## Rollback Plan

If deployment fails:

1. **Identify Issue**
   - Check logs
   - Monitor metrics
   - User reports

2. **Rollback**
   ```bash
   # Revert to previous version
   git revert <commit>
   
   # Rebuild and deploy
   npm run build
   python app.py
   ```

3. **Investigate**
   - Root cause analysis
   - Fix issue
   - Test thoroughly

4. **Redeploy**
   - Deploy fix
   - Monitor closely
   - Verify functionality

---

## Success Criteria

✅ Application loads in < 2 seconds  
✅ API responds in < 3 seconds  
✅ Model inference in ~270ms  
✅ No console errors  
✅ All features working  
✅ Mobile responsive  
✅ Health check passing  
✅ Monitoring active  

---

**Deployment Status**: ✅ Ready  
**Last Updated**: October 28, 2025  
**Version**: 2.0 (Trained Medical Models)
