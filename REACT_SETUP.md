# React Frontend Setup Guide

## Quick Start

### 1. Install Frontend Dependencies
```bash
cd frontend
npm install
```

### 2. Build React App for Production
```bash
npm run build
```

This will create a `build` folder with optimized production files.

### 3. Run Flask Backend
From the project root directory:
```bash
pip install flask-cors
python app.py
```

The app will be available at `http://localhost:5000`

## Development Mode

If you want to develop the React frontend with hot reload:

### Terminal 1 - Start React Development Server
```bash
cd frontend
npm start
```
This runs on `http://localhost:3000`

### Terminal 2 - Start Flask Backend
```bash
python app.py
```

The React dev server will proxy API calls to Flask on `http://localhost:5000`

## Features

- **Modern UI**: Built with React and Tailwind CSS
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Preview**: Image preview before analysis
- **Loading States**: Visual feedback during analysis
- **Error Handling**: Clear error messages
- **Beautiful Icons**: Using Lucide React icons

## File Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── index.js
│   └── App.js
├── package.json
└── build/          (generated after npm run build)
```

## Notes

- The Flask backend serves the React build from `frontend/build/static`
- API endpoint: `/api/analyze` (POST)
- All styling uses Tailwind CSS with no additional CSS files needed
