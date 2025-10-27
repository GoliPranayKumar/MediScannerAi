# Medical Imaging Diagnosis Agent - Setup Instructions

## Overview
This is a modern web application for AI-powered medical image analysis using the Grok API. It features a responsive React frontend and a Flask backend.

## Prerequisites
- Python 3.8+
- Node.js 14+ and npm
- Grok API Key (already configured in `.env`)

## Backend Setup

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Configuration
Create a `.env` file in the root directory with your Groq API key:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your free API key from: https://console.groq.com

## Frontend Setup

### 1. Install Node Dependencies
```bash
cd frontend
npm install
```

### 2. Build React Application
```bash
npm run build
```

This creates an optimized production build in `frontend/build/`.

## Running the Application

### Production Mode (Recommended)
```bash
# From project root
python app.py
```
Visit `http://localhost:5000` in your browser.

### Development Mode (with hot reload)

**Terminal 1 - React Development Server:**
```bash
cd frontend
npm start
```

**Terminal 2 - Flask Backend:**
```bash
python app.py
```

React dev server runs on `http://localhost:3000` and proxies API calls to Flask.

## Features

✨ **Modern UI**
- Responsive design for desktop, tablet, and mobile
- Real-time image preview
- Loading states and error handling
- Beautiful Lucide React icons

🔍 **Medical Analysis**
- Upload medical images (PNG, JPG, JPEG, DICOM)
- AI-powered analysis using Grok API
- Concise, focused results
- Disease names highlighted in bold

🔒 **Security**
- API key stored in `.env` (not exposed in UI)
- `.gitignore` prevents accidental commits of sensitive files
- CORS enabled for safe API communication

## Project Structure

```
.
├── app.py                      # Flask backend
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (API key)
├── .gitignore                  # Git ignore rules
├── templates/
│   └── index.html             # Flask template
├── uploads/                    # Uploaded images
├── frontend/
│   ├── package.json           # Node dependencies
│   ├── public/
│   │   └── index.html         # React HTML template
│   ├── src/
│   │   ├── index.js           # React entry point
│   │   └── App.js             # Main React component
│   └── build/                 # Production build (generated)
├── REACT_SETUP.md             # React setup guide
└── SETUP_INSTRUCTIONS.md      # This file
```

## API Endpoints

### POST /api/analyze
Analyzes a medical image.

**Request:**
- Content-Type: multipart/form-data
- Body: `image` (file)

**Response:**
```json
{
  "result": "<html>Analysis results in HTML format</html>"
}
```

**Error Response:**
```json
{
  "error": "Error message"
}
```

## Troubleshooting

### Python dependencies not installing
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Node modules issues
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Port already in use
- Flask: Change port in `app.py` (default 5000)
- React: Set PORT environment variable (default 3000)

### API key not working
- Verify `.env` file exists in project root
- Check API key is correct in `.env`
- Restart Flask backend after changing `.env`

## Security Notes

⚠️ **Important:**
- Never commit `.env` file to version control
- `.gitignore` is configured to prevent this
- Keep your Grok API key confidential
- Don't share `.env` file with others

## Support

For issues or questions:
1. Check error messages in browser console
2. Check Flask backend logs in terminal
3. Verify `.env` file configuration
4. Ensure all dependencies are installed

---

**Last Updated:** October 27, 2025
