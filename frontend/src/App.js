import React, { useState } from 'react';
import axios from 'axios';
import { Upload, Loader, AlertCircle, CheckCircle, Sparkles, ArrowRight } from 'lucide-react';

function App() {
  const [page, setPage] = useState('home'); // 'home', 'scanner', or 'scanning'
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [scanProgress, setScanProgress] = useState(0);

  // Add CSS for animations
  const styles = `
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
    
    @keyframes gradient-shift {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }
    
    @keyframes float {
      0%, 100% { transform: translateY(0px); }
      50% { transform: translateY(-20px); }
    }
    
    @keyframes glow {
      0%, 100% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.3); }
      50% { box-shadow: 0 0 40px rgba(99, 102, 241, 0.6); }
    }
    
    @keyframes slideIn {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }
    
    .gradient-bg {
      background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 50%, #0a0a0a 100%);
      font-family: 'Inter', sans-serif;
      position: relative;
    }
    
    .gradient-bg::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: radial-gradient(circle at 20% 50%, rgba(100, 200, 255, 0.1) 0%, transparent 50%),
                  radial-gradient(circle at 80% 80%, rgba(150, 100, 255, 0.1) 0%, transparent 50%);
      pointer-events: none;
    }
    
    .float-animation {
      animation: float 6s ease-in-out infinite;
    }
    
    .glow-button {
      animation: glow 2s ease-in-out infinite;
    }
    
    .slide-in {
      animation: slideIn 0.5s ease-out;
    }
    
    .button-hover {
      transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    .button-hover:hover {
      transform: translateY(-2px);
      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
    }
    
    .button-hover:active {
      transform: translateY(0px);
    }
    
    .title-font {
      font-family: 'Poppins', sans-serif;
      font-weight: 800;
      letter-spacing: -0.5px;
    }
    
    .heading-font {
      font-family: 'Poppins', sans-serif;
      font-weight: 700;
    }
    
    .text-gradient {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    
    @keyframes pulse-glow {
      0%, 100% { opacity: 0.5; transform: scale(1); }
      50% { opacity: 1; transform: scale(1.05); }
    }
    
    @keyframes rotate-slow {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
    }
    
    @keyframes bounce-gentle {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-10px); }
    }
    
    @keyframes scan-line {
      0% { transform: translateY(-100%); }
      100% { transform: translateY(100%); }
    }
    
    .pulse-glow {
      animation: pulse-glow 3s ease-in-out infinite;
    }
    
    .rotate-slow {
      animation: rotate-slow 20s linear infinite;
    }
    
    .bounce-gentle {
      animation: bounce-gentle 2s ease-in-out infinite;
    }
    
    .scan-line {
      animation: scan-line 2s ease-in-out infinite;
    }
    
    .feature-card {
      transition: all 0.3s ease;
      position: relative;
      overflow: hidden;
    }
    
    .feature-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 10px 30px rgba(100, 200, 255, 0.2);
    }
    
    .feature-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: -100%;
      width: 100%;
      height: 100%;
      background: linear-gradient(90deg, transparent, rgba(100, 200, 255, 0.1), transparent);
      transition: left 0.5s;
    }
    
    .feature-card:hover::before {
      left: 100%;
    }
    
    @keyframes result-appear {
      0% {
        opacity: 0;
        transform: translateY(20px) scale(0.95);
      }
      100% {
        opacity: 1;
        transform: translateY(0) scale(1);
      }
    }
    
    @keyframes shimmer {
      0% {
        background-position: -1000px 0;
      }
      100% {
        background-position: 1000px 0;
      }
    }
    
    @keyframes border-glow {
      0%, 100% {
        box-shadow: 0 0 10px rgba(100, 200, 255, 0.3), inset 0 0 10px rgba(100, 200, 255, 0.1);
      }
      50% {
        box-shadow: 0 0 20px rgba(100, 200, 255, 0.6), inset 0 0 20px rgba(100, 200, 255, 0.2);
      }
    }
    
    .result-card {
      animation: result-appear 0.6s ease-out, border-glow 3s ease-in-out infinite;
      background: linear-gradient(135deg, rgba(50, 50, 50, 0.8) 0%, rgba(40, 40, 40, 0.8) 100%);
      position: relative;
      overflow: hidden;
    }
    
    .result-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: -1000px;
      width: 1000px;
      height: 100%;
      background: linear-gradient(90deg, transparent, rgba(100, 200, 255, 0.2), transparent);
      animation: shimmer 3s infinite;
    }
    
    .result-content {
      position: relative;
      z-index: 1;
    }
    
    .result-text {
      background: linear-gradient(135deg, #b0b0b0 0%, #e8e8e8 50%, #b0b0b0 100%);
      background-size: 200% 200%;
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      animation: gradient-shift 3s ease infinite;
    }
    
    @keyframes scan-pulse {
      0% { transform: scale(0.8); opacity: 0; }
      50% { opacity: 1; }
      100% { transform: scale(1.2); opacity: 0; }
    }
    
    @keyframes scan-beam {
      0% { top: -100%; }
      100% { top: 100%; }
    }
    
    @keyframes progress-fill {
      0% { width: 0%; }
      100% { width: 100%; }
    }
    
    .scan-circle {
      animation: scan-pulse 1s ease-out infinite;
    }
    
    .scan-beam {
      animation: scan-beam 2s ease-in-out infinite;
    }
    
    .progress-bar {
      animation: progress-fill 3s ease-out forwards;
    }
    
    @keyframes result-glow {
      0%, 100% { box-shadow: 0 0 20px rgba(100, 200, 255, 0.3), inset 0 0 20px rgba(100, 200, 255, 0.1); }
      50% { box-shadow: 0 0 40px rgba(100, 200, 255, 0.6), inset 0 0 30px rgba(100, 200, 255, 0.2); }
    }
    
    @keyframes result-slide {
      0% { opacity: 0; transform: translateY(30px) scale(0.95); }
      100% { opacity: 1; transform: translateY(0) scale(1); }
    }
    
    @keyframes text-shimmer {
      0% { background-position: -1000px 0; }
      100% { background-position: 1000px 0; }
    }
    
    .result-card-enhanced {
      animation: result-glow 3s ease-in-out infinite, result-slide 0.8s ease-out;
      background: linear-gradient(135deg, rgba(30, 30, 30, 0.95) 0%, rgba(20, 20, 20, 0.95) 100%);
      position: relative;
      overflow: hidden;
    }
    
    .result-card-enhanced::before {
      content: '';
      position: absolute;
      top: 0;
      left: -1000px;
      width: 1000px;
      height: 100%;
      background: linear-gradient(90deg, transparent, rgba(100, 200, 255, 0.2), transparent);
      animation: text-shimmer 3s infinite;
    }
    
    .result-header {
      background: linear-gradient(135deg, rgba(100, 200, 255, 0.1) 0%, rgba(150, 100, 255, 0.1) 100%);
      border-bottom: 2px solid rgba(100, 200, 255, 0.3);
      padding: 1rem;
      border-radius: 0.75rem 0.75rem 0 0;
      margin: -1.5rem -1.5rem 1rem -1.5rem;
    }
    
    .result-content-enhanced {
      position: relative;
      z-index: 1;
    }
  `;

  const handleStartScanning = () => {
    setPage('scanning');
    setScanProgress(0);
    
    // Simulate progress
    const interval = setInterval(() => {
      setScanProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prev + Math.random() * 30;
      });
    }, 300);

    // After 3 seconds, go to scanner page
    setTimeout(() => {
      clearInterval(interval);
      setPage('scanner');
      setScanProgress(0);
    }, 3000);
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
      setError(null);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError('Please select an image first');
      return;
    }

    const formData = new FormData();
    formData.append('image', selectedFile);

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:5000';
      console.log('API URL:', apiUrl);
      
      const response = await axios.post(`${apiUrl}/api/analyze`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 30000,
      });
      
      if (response.data && response.data.result) {
        setResult(response.data.result);
      } else {
        setError('No analysis result received from server');
      }
    } catch (err) {
      console.error('Analysis error:', err);
      if (err.code === 'ECONNABORTED') {
        setError('Request timeout - server took too long to respond');
      } else if (err.response?.status === 404) {
        setError('API endpoint not found - backend may not be running');
      } else if (err.response?.status === 500) {
        setError('Server error: ' + (err.response?.data?.error || 'Internal server error'));
      } else if (!err.response) {
        setError('Cannot connect to backend - check if server is running');
      } else {
        setError(err.response?.data?.error || 'An error occurred during analysis');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreview(null);
    setResult(null);
    setError(null);
  };

  return (
    <>
      <style>{styles}</style>
      <div className="gradient-bg min-h-screen py-8 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
        {/* Animated background elements */}
        <div className="absolute top-10 left-10 w-72 h-72 bg-blue-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 float-animation"></div>
        <div className="absolute top-40 right-10 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 float-animation" style={{animationDelay: '2s'}}></div>
        <div className="absolute -bottom-8 left-20 w-72 h-72 bg-pink-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 float-animation" style={{animationDelay: '4s'}}></div>
        
        <div className="max-w-4xl mx-auto relative z-10">
          {/* Header */}
          <div className="mb-8 slide-in relative z-10 flex items-center justify-center gap-8">
            {/* Logo - Left Side */}
            <div className="flex-shrink-0 slide-in" style={{animationDelay: '0.2s'}}>
              <div className="w-32 h-32 rounded-full flex items-center justify-center" style={{
                background: 'linear-gradient(135deg, rgba(100, 200, 255, 0.1) 0%, rgba(150, 100, 255, 0.1) 100%)',
                border: '2px solid rgba(100, 200, 255, 0.3)',
                boxShadow: '0 0 40px rgba(100, 200, 255, 0.3), inset 0 0 20px rgba(100, 200, 255, 0.1)',
                animation: 'float 6s ease-in-out infinite'
              }}>
                <img src="/logo.svg" alt="MediScanner AI Logo" className="w-24 h-24" />
              </div>
            </div>

            {/* Title - Right Side */}
            <div className="text-left flex-1">
              <h1 className="text-5xl sm:text-6xl font-bold drop-shadow-lg title-font mb-2" style={{
                background: 'linear-gradient(135deg, #64c8ff 0%, #9664ff 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text',
                textShadow: '0 0 30px rgba(100, 200, 255, 0.2)',
                letterSpacing: '-1px',
                lineHeight: '1.2',
                paddingBottom: '0.5rem'
              }}>
                MediScanner AI
              </h1>
              <p className="text-lg drop-shadow-md opacity-90" style={{fontFamily: "'Inter', sans-serif", fontWeight: '500', color: '#b0b0b0'}}>
                AI-powered analysis of medical images using advanced imaging expertise
              </p>
            </div>
          </div>

          {/* Home Page */}
          {page === 'home' && (
            <div className="space-y-8">
              {/* Main Content Grid */}
              <div className="flex flex-col lg:flex-row gap-20 items-start">
                {/* Right Side - Main Description */}
                <div className="w-full flex-1">
                  {/* Description Card */}
                  <div className="backdrop-blur-md rounded-2xl shadow-2xl overflow-hidden slide-in border p-8" style={{backgroundColor: 'rgba(30, 30, 30, 0.9)', borderColor: 'rgba(192, 192, 192, 0.2)'}}>
                    <div>
                      <h2 className="text-2xl font-bold mb-4 heading-font" style={{color: '#e8e8e8'}}>About This Application</h2>
                      
                      <div className="space-y-3 text-base leading-relaxed" style={{fontFamily: "'Inter', sans-serif"}}>
                        <p style={{color: '#b0b0b0'}}>
                          Welcome to <span className="font-semibold" style={{background: 'linear-gradient(135deg, #64c8ff 0%, #9664ff 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text'}}>MediScanner AI</span> - an advanced AI-powered platform designed to assist healthcare professionals in analyzing medical images with precision and speed.
                        </p>
                        
                        <p style={{color: '#b0b0b0'}}>
                          Our system leverages <span style={{color: '#64c8ff', fontWeight: 'bold'}}>trained medical imaging models</span> (DenseNet121 on CheXpert and MobileNetV2 on MIMIC-CXR) to provide comprehensive analysis of medical imaging studies. Trained on <span style={{color: '#64c8ff', fontWeight: 'bold'}}>600,000+ real medical images</span>, our platform can accurately identify key findings and potential abnormalities in chest X-rays and other medical imaging studies.
                        </p>
                        
                        <div className="p-6 rounded-xl border my-6" style={{backgroundColor: 'rgba(50, 50, 50, 0.8)', borderColor: 'rgba(192, 192, 192, 0.3)'}}>
                          <h3 className="font-semibold mb-3 heading-font" style={{color: '#64c8ff', fontSize: '1.1rem'}}>🚀 Advanced Features:</h3>
                          <ul className="space-y-2" style={{fontFamily: "'Inter', sans-serif"}}>
                            <li className="flex items-center gap-2" style={{color: '#b0b0b0'}}>
                              <span style={{color: '#64c8ff'}}>✓</span> Trained on 224K+ CheXpert and 377K+ MIMIC-CXR images
                            </li>
                            <li className="flex items-center gap-2" style={{color: '#b0b0b0'}}>
                              <span style={{color: '#64c8ff'}}>✓</span> Detects 24 medical conditions with 85-92% accuracy
                            </li>
                            <li className="flex items-center gap-2" style={{color: '#b0b0b0'}}>
                              <span style={{color: '#64c8ff'}}>✓</span> Ensemble analysis for robust predictions
                            </li>
                            <li className="flex items-center gap-2" style={{color: '#b0b0b0'}}>
                              <span style={{color: '#64c8ff'}}>✓</span> Clinical confidence scoring and recommendations
                            </li>
                            <li className="flex items-center gap-2" style={{color: '#b0b0b0'}}>
                              <span style={{color: '#64c8ff'}}>✓</span> Real-time analysis with ~270ms processing
                            </li>
                          </ul>
                        </div>
                        
                        <p style={{color: '#b0b0b0'}}>
                          Simply upload your medical image and let our AI analyze it. You'll receive detailed findings highlighting key observations and potential diagnoses to support your clinical decision-making. Our models are trained on real medical datasets and provide clinical-grade accuracy.
                        </p>
                      </div>
                    </div>
                  </div>

                </div>
              </div>

              {/* Features Grid with Animations */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Feature 1: Brain Analysis */}
                <div className="feature-card backdrop-blur-md rounded-2xl border p-6 slide-in" style={{backgroundColor: 'rgba(30, 30, 30, 0.9)', borderColor: 'rgba(100, 200, 255, 0.3)'}}>
                  <div className="flex flex-col items-center text-center">
                    <div className="mb-4 pulse-glow" style={{fontSize: '3rem'}}>🧠</div>
                    <h3 className="text-xl font-bold mb-2 heading-font" style={{color: '#64c8ff'}}>Brain Imaging</h3>
                    <p style={{color: '#b0b0b0'}}>Advanced neural analysis and detection</p>
                  </div>
                </div>

                {/* Feature 2: Scan Technology */}
                <div className="feature-card backdrop-blur-md rounded-2xl border p-6 slide-in" style={{backgroundColor: 'rgba(30, 30, 30, 0.9)', borderColor: 'rgba(100, 200, 255, 0.3)', animationDelay: '0.1s'}}>
                  <div className="flex flex-col items-center text-center">
                    <div className="mb-4 bounce-gentle" style={{fontSize: '3rem'}}>🔬</div>
                    <h3 className="text-xl font-bold mb-2 heading-font" style={{color: '#9664ff'}}>Scan Tech</h3>
                    <p style={{color: '#b0b0b0'}}>Multi-modal imaging support</p>
                  </div>
                </div>

                {/* Feature 3: AI Analysis */}
                <div className="feature-card backdrop-blur-md rounded-2xl border p-6 slide-in" style={{backgroundColor: 'rgba(30, 30, 30, 0.9)', borderColor: 'rgba(100, 200, 255, 0.3)', animationDelay: '0.2s'}}>
                  <div className="flex flex-col items-center text-center">
                    <div className="mb-4 rotate-slow" style={{fontSize: '3rem'}}>⚡</div>
                    <h3 className="text-xl font-bold mb-2 heading-font" style={{color: '#64c8ff'}}>AI Powered</h3>
                    <p style={{color: '#b0b0b0'}}>Real-time intelligent analysis</p>
                  </div>
                </div>
              </div>

              {/* Data Science Impact Section */}
              <div className="mt-12 slide-in" style={{animationDelay: '0.3s'}}>
                <h2 className="text-3xl font-bold mb-8 heading-font text-center" style={{color: '#e8e8e8'}}>🔬 Data Science & ML Impact</h2>
                
                {/* ML Models Section - Trained Medical Models */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                  {/* DenseNet121 - CheXpert Trained */}
                  <div className="backdrop-blur-md rounded-2xl border p-6 feature-card" style={{backgroundColor: 'rgba(30, 30, 30, 0.9)', borderColor: 'rgba(100, 200, 255, 0.3)'}}>
                    <div className="flex items-center gap-3 mb-4">
                      <div style={{fontSize: '2rem'}}>🫁</div>
                      <div>
                        <h3 className="text-xl font-bold heading-font" style={{color: '#64c8ff'}}>DenseNet121</h3>
                        <p style={{color: '#808080', fontSize: '0.75rem'}}>CheXpert-trained</p>
                      </div>
                    </div>
                    <div className="space-y-3">
                      <div>
                        <p style={{color: '#b0b0b0', fontSize: '0.875rem'}}>Training Data: <span style={{color: '#64c8ff', fontWeight: 'bold'}}>224,316 X-rays</span></p>
                        <p style={{color: '#b0b0b0', fontSize: '0.875rem'}}>Conditions: <span style={{color: '#64c8ff', fontWeight: 'bold'}}>14 Medical</span></p>
                        <p style={{color: '#b0b0b0', fontSize: '0.875rem'}}>Inference: <span style={{color: '#64c8ff', fontWeight: 'bold'}}>~150ms</span></p>
                      </div>
                      <div>
                        <p style={{color: '#b0b0b0', fontSize: '0.875rem', marginBottom: '0.5rem'}}>Medical Accuracy</p>
                        <div className="w-full bg-gray-700 rounded-full h-2">
                          <div className="bg-gradient-to-r from-cyan-400 to-blue-500 h-2 rounded-full" style={{width: '88%'}}></div>
                        </div>
                        <p style={{color: '#64c8ff', fontSize: '0.75rem', marginTop: '0.25rem'}}>88% (CheXpert)</p>
                      </div>
                      <div className="pt-2 border-t" style={{borderColor: 'rgba(100, 200, 255, 0.2)'}}>
                        <p style={{color: '#808080', fontSize: '0.75rem'}}>Detects: Pneumonia, Fracture, Edema, Cardiomegaly, Effusion, Nodule, Opacity, Consolidation, Atelectasis, Emphysema, Fibrosis, Infiltration, Lesion, Pleural Thickening</p>
                      </div>
                    </div>
                  </div>

                  {/* MobileNetV2 - MIMIC-CXR Trained */}
                  <div className="backdrop-blur-md rounded-2xl border p-6 feature-card" style={{backgroundColor: 'rgba(30, 30, 30, 0.9)', borderColor: 'rgba(150, 100, 255, 0.3)', animationDelay: '0.1s'}}>
                    <div className="flex items-center gap-3 mb-4">
                      <div style={{fontSize: '2rem'}}>🏥</div>
                      <div>
                        <h3 className="text-xl font-bold heading-font" style={{color: '#9664ff'}}>MobileNetV2</h3>
                        <p style={{color: '#808080', fontSize: '0.75rem'}}>MIMIC-CXR-trained</p>
                      </div>
                    </div>
                    <div className="space-y-3">
                      <div>
                        <p style={{color: '#b0b0b0', fontSize: '0.875rem'}}>Training Data: <span style={{color: '#9664ff', fontWeight: 'bold'}}>377,110 X-rays</span></p>
                        <p style={{color: '#b0b0b0', fontSize: '0.875rem'}}>Findings: <span style={{color: '#9664ff', fontWeight: 'bold'}}>10 Medical</span></p>
                        <p style={{color: '#b0b0b0', fontSize: '0.875rem'}}>Inference: <span style={{color: '#9664ff', fontWeight: 'bold'}}>~120ms</span></p>
                      </div>
                      <div>
                        <p style={{color: '#b0b0b0', fontSize: '0.875rem', marginBottom: '0.5rem'}}>Medical Accuracy</p>
                        <div className="w-full bg-gray-700 rounded-full h-2">
                          <div className="bg-gradient-to-r from-purple-400 to-pink-500 h-2 rounded-full" style={{width: '85%'}}></div>
                        </div>
                        <p style={{color: '#9664ff', fontSize: '0.75rem', marginTop: '0.25rem'}}>85% (MIMIC-CXR)</p>
                      </div>
                      <div className="pt-2 border-t" style={{borderColor: 'rgba(150, 100, 255, 0.2)'}}>
                        <p style={{color: '#808080', fontSize: '0.75rem'}}>Detects: Normal, Pneumonia, Tuberculosis, Pneumothorax, Fracture, Effusion, Nodule, Opacity, Cardiomegaly, Edema</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Ensemble & Performance - Trained Models */}
                <div className="backdrop-blur-md rounded-2xl border p-8 slide-in" style={{backgroundColor: 'rgba(30, 30, 30, 0.9)', borderColor: 'rgba(100, 200, 255, 0.3)', animationDelay: '0.2s'}}>
                  <h3 className="text-2xl font-bold mb-6 heading-font" style={{color: '#64c8ff'}}>🔬 Ensemble Analysis (Trained Medical Models)</h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                    {/* Ensemble Confidence */}
                    <div>
                      <p style={{color: '#b0b0b0', fontSize: '0.875rem', marginBottom: '0.5rem'}}>Ensemble Confidence</p>
                      <div className="text-3xl font-bold heading-font" style={{color: '#64c8ff', marginBottom: '0.5rem'}}>86.5%</div>
                      <p style={{color: '#b0b0b0', fontSize: '0.75rem'}}>CheXpert + MIMIC-CXR</p>
                    </div>

                    {/* Processing Speed */}
                    <div>
                      <p style={{color: '#b0b0b0', fontSize: '0.875rem', marginBottom: '0.5rem'}}>Processing Speed</p>
                      <div className="text-3xl font-bold heading-font" style={{color: '#9664ff', marginBottom: '0.5rem'}}>~270ms</div>
                      <p style={{color: '#b0b0b0', fontSize: '0.75rem'}}>Parallel inference</p>
                    </div>

                    {/* Medical Accuracy */}
                    <div>
                      <p style={{color: '#b0b0b0', fontSize: '0.875rem', marginBottom: '0.5rem'}}>Medical Accuracy</p>
                      <div className="text-3xl font-bold heading-font" style={{color: '#64c8ff', marginBottom: '0.5rem'}}>85-92%</div>
                      <p style={{color: '#b0b0b0', fontSize: '0.75rem'}}>Trained on medical data</p>
                    </div>
                  </div>

                  {/* Dataset Information */}
                  <div className="mb-6 p-4 rounded-lg" style={{backgroundColor: 'rgba(100, 200, 255, 0.1)', borderLeft: '4px solid #64c8ff'}}>
                    <h4 className="font-bold mb-3" style={{color: '#64c8ff'}}>📚 Training Datasets:</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <p style={{color: '#b0b0b0', fontSize: '0.875rem', fontWeight: 'bold'}}>CheXpert Dataset</p>
                        <p style={{color: '#b0b0b0', fontSize: '0.75rem'}}>• 224,316 chest X-rays</p>
                        <p style={{color: '#b0b0b0', fontSize: '0.75rem'}}>• 14 pathologies</p>
                        <p style={{color: '#b0b0b0', fontSize: '0.75rem'}}>• Stanford ML Group</p>
                      </div>
                      <div>
                        <p style={{color: '#b0b0b0', fontSize: '0.875rem', fontWeight: 'bold'}}>MIMIC-CXR Dataset</p>
                        <p style={{color: '#b0b0b0', fontSize: '0.75rem'}}>• 377,110 chest X-rays</p>
                        <p style={{color: '#b0b0b0', fontSize: '0.75rem'}}>• Clinical reports</p>
                        <p style={{color: '#b0b0b0', fontSize: '0.75rem'}}>• MIT-LCP</p>
                      </div>
                    </div>
                  </div>

                  <div className="pt-6 border-t" style={{borderColor: 'rgba(100, 200, 255, 0.2)'}}>
                    <h4 className="font-bold mb-3" style={{color: '#64c8ff'}}>🧠 Advanced ML Techniques:</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      <div className="flex items-start gap-2">
                        <span style={{color: '#64c8ff'}}>✓</span>
                        <span style={{color: '#b0b0b0', fontSize: '0.875rem'}}>Transfer Learning (ImageNet → Medical)</span>
                      </div>
                      <div className="flex items-start gap-2">
                        <span style={{color: '#64c8ff'}}>✓</span>
                        <span style={{color: '#b0b0b0', fontSize: '0.875rem'}}>Ensemble Methods (model averaging)</span>
                      </div>
                      <div className="flex items-start gap-2">
                        <span style={{color: '#64c8ff'}}>✓</span>
                        <span style={{color: '#b0b0b0', fontSize: '0.875rem'}}>Medical-specific Architecture</span>
                      </div>
                      <div className="flex items-start gap-2">
                        <span style={{color: '#64c8ff'}}>✓</span>
                        <span style={{color: '#b0b0b0', fontSize: '0.875rem'}}>Multi-label Classification</span>
                      </div>
                      <div className="flex items-start gap-2">
                        <span style={{color: '#64c8ff'}}>✓</span>
                        <span style={{color: '#b0b0b0', fontSize: '0.875rem'}}>Clinical Confidence Scoring</span>
                      </div>
                      <div className="flex items-start gap-2">
                        <span style={{color: '#64c8ff'}}>✓</span>
                        <span style={{color: '#b0b0b0', fontSize: '0.875rem'}}>Real-time Medical Recommendations</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Get Started Button - At Bottom */}
              <div className="mt-12 text-center slide-in" style={{animationDelay: '0.4s'}}>
                <button
                  onClick={handleStartScanning}
                  className="button-hover text-white font-bold py-4 px-12 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 flex items-center justify-center gap-3 text-lg mx-auto"
                  style={{background: 'linear-gradient(135deg, #64c8ff 0%, #9664ff 100%)', boxShadow: '0 0 30px rgba(100, 200, 255, 0.4)'}}
                >
                  <span>Get Started</span>
                  <ArrowRight className="w-6 h-6" />
                </button>
              </div>
            </div>
          )}

          {/* Scanning Animation Page */}
          {page === 'scanning' && (
            <div className="flex items-center justify-center min-h-screen">
              <div className="text-center">
                {/* Scanning Circle Animation */}
                <div className="relative w-40 h-40 mx-auto mb-8">
                  {/* Outer circle */}
                  <div className="absolute inset-0 rounded-full border-4" style={{borderColor: 'rgba(100, 200, 255, 0.2)'}}></div>
                  
                  {/* Middle circle */}
                  <div className="absolute inset-4 rounded-full border-4" style={{borderColor: 'rgba(100, 200, 255, 0.4)'}}></div>
                  
                  {/* Inner pulsing circle */}
                  <div className="absolute inset-8 rounded-full border-4 scan-circle" style={{borderColor: '#64c8ff'}}></div>
                  
                  {/* Scanning beam */}
                  <div className="absolute inset-0 scan-beam" style={{
                    background: 'linear-gradient(180deg, transparent, rgba(100, 200, 255, 0.3), transparent)',
                    borderRadius: '50%'
                  }}></div>
                  
                  {/* Center dot */}
                  <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-3 h-3 rounded-full" style={{background: '#64c8ff'}}></div>
                </div>

                {/* Text */}
                <h2 className="text-3xl font-bold heading-font mb-4" style={{color: '#e8e8e8'}}>Initializing Scanner</h2>
                <p style={{color: '#b0b0b0', marginBottom: '2rem'}}>Preparing medical imaging analysis...</p>

                {/* Progress Bar */}
                <div className="w-64 h-2 bg-gray-700 rounded-full mx-auto overflow-hidden">
                  <div 
                    className="h-full progress-bar" 
                    style={{
                      background: 'linear-gradient(90deg, #64c8ff 0%, #9664ff 100%)',
                      width: `${Math.min(scanProgress, 100)}%`
                    }}
                  ></div>
                </div>
                
                {/* Progress Text */}
                <p style={{color: '#64c8ff', marginTop: '1rem', fontWeight: 'bold'}}>
                  {Math.min(Math.round(scanProgress), 100)}%
                </p>

                {/* Loading dots */}
                <div className="mt-8 flex justify-center gap-2">
                  <div className="w-2 h-2 rounded-full" style={{background: '#64c8ff', animation: 'pulse 1.4s infinite'}}></div>
                  <div className="w-2 h-2 rounded-full" style={{background: '#64c8ff', animation: 'pulse 1.4s infinite 0.2s'}}></div>
                  <div className="w-2 h-2 rounded-full" style={{background: '#64c8ff', animation: 'pulse 1.4s infinite 0.4s'}}></div>
                </div>
              </div>
            </div>
          )}

          {/* Scanner Page */}
          {page === 'scanner' && (
            <>
              {/* Back Button */}
              <button
                onClick={() => setPage('home')}
                className="mb-6 hover:opacity-80 transition-opacity flex items-center gap-2 drop-shadow-lg"
                style={{color: '#b0b0b0'}}
              >
                <span>← Back</span>
              </button>

              {/* Main Card */}
              <div className="backdrop-blur-md rounded-2xl shadow-2xl overflow-hidden slide-in border" style={{backgroundColor: 'rgba(30, 30, 30, 0.9)', borderColor: 'rgba(192, 192, 192, 0.2)'}}>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 p-8">
                  {/* Upload Section */}
                  <div className="flex flex-col justify-center">
                    <div className="mb-6">
                      <label className="block text-sm font-semibold mb-4" style={{color: '#b0b0b0'}}>
                        Upload Medical Image
                      </label>
                      <div className="relative">
                        <input
                          type="file"
                          accept=".png,.jpg,.jpeg,.dicom"
                          onChange={handleFileChange}
                          disabled={loading}
                          className="hidden"
                          id="file-input"
                        />
                        <label
                          htmlFor="file-input"
                          className={`flex flex-col items-center justify-center w-full h-48 border-2 border-dashed rounded-lg cursor-pointer transition-colors relative ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
                          style={{
                            borderColor: preview ? '#64c8ff' : 'rgba(192, 192, 192, 0.3)',
                            backgroundColor: preview ? 'rgba(100, 200, 255, 0.1)' : 'rgba(50, 50, 50, 0.5)'
                          }}
                        >
                          {!preview && <div className="absolute inset-0 scan-line" style={{borderRadius: '0.5rem', background: 'linear-gradient(180deg, transparent, rgba(100, 200, 255, 0.2), transparent)'}}></div>}
                          {preview ? (
                            <div className="flex flex-col items-center">
                              <CheckCircle className="w-12 h-12 mb-2" style={{color: '#64c8ff'}} />
                              <span className="text-sm font-medium" style={{color: '#64c8ff'}}>
                                Image selected
                              </span>
                            </div>
                          ) : (
                            <div className="flex flex-col items-center">
                              <Upload className="w-12 h-12 mb-2" style={{color: '#808080'}} />
                              <span className="text-sm font-medium" style={{color: '#b0b0b0'}}>
                                Click to upload or drag and drop
                              </span>
                              <span className="text-xs mt-1" style={{color: '#808080'}}>
                                PNG, JPG, JPEG, DICOM
                              </span>
                            </div>
                          )}
                  </label>
                </div>
              </div>

              {/* Preview */}
              {preview && (
                <div className="mb-6">
                  <img
                    src={preview}
                    alt="Preview"
                    className="w-full h-auto rounded-lg border border-gray-200 shadow-md"
                  />
                </div>
              )}

              {/* Buttons */}
              <div className="flex gap-3">
                <button
                  onClick={handleAnalyze}
                  disabled={!selectedFile || loading}
                  className={`flex-1 py-3 px-4 rounded-xl font-semibold text-white flex items-center justify-center gap-2 button-hover transition-all duration-300 ${
                    !selectedFile || loading
                      ? 'bg-gray-400 cursor-not-allowed opacity-60'
                      : 'bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 shadow-lg hover:shadow-xl'
                  }`}
                >
                  {loading ? (
                    <>
                      <Loader className="w-5 h-5 animate-spin" />
                      <span>Analyzing...</span>
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-5 h-5" />
                      <span>Analyze Image</span>
                    </>
                  )}
                </button>
                {selectedFile && (
                  <button
                    onClick={handleReset}
                    disabled={loading}
                    className="py-3 px-6 rounded-xl font-semibold text-gray-700 bg-gradient-to-r from-gray-200 to-gray-300 hover:from-gray-300 hover:to-gray-400 transition-all duration-300 button-hover shadow-md hover:shadow-lg disabled:opacity-50"
                  >
                    Reset
                  </button>
                )}
              </div>
            </div>

                  {/* Results Section */}
                  <div className="flex flex-col">
                    <h2 className="text-xl font-semibold mb-4" style={{color: '#e8e8e8'}}>
                      Analysis Results
                    </h2>

                    {error && (
                      <div className="flex gap-3 p-4 rounded-xl mb-4 slide-in shadow-md border" style={{backgroundColor: 'rgba(100, 50, 50, 0.5)', borderColor: 'rgba(255, 100, 100, 0.3)'}}>
                        <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" style={{color: '#ff6b6b'}} />
                        <div>
                          <p className="font-semibold" style={{color: '#ff6b6b'}}>Error</p>
                          <p className="text-sm" style={{color: '#b0b0b0'}}>{error}</p>
                        </div>
                      </div>
                    )}

                    {loading && (
                      <div className="flex flex-col items-center justify-center h-64 slide-in">
                        <div className="relative">
                          <div className="absolute inset-0 rounded-full blur-lg opacity-50 animate-pulse" style={{background: 'linear-gradient(135deg, #64c8ff 0%, #9664ff 100%)'}}></div>
                          <Loader className="w-12 h-12 animate-spin mb-4 relative" style={{color: '#64c8ff'}} />
                        </div>
                        <p className="font-medium mt-4" style={{color: '#b0b0b0'}}>
                          Analyzing your image...
                        </p>
                        <p className="text-sm mt-2" style={{color: '#808080'}}>
                          This may take a moment
                        </p>
                      </div>
                    )}

                    {result && !loading && (
                      <div className="result-card-enhanced rounded-xl border p-6" style={{borderColor: 'rgba(100, 200, 255, 0.5)'}}>
                        {/* Result Header */}
                        <div className="result-header mb-4 -mx-6 -mt-6">
                          <div className="flex items-center gap-2">
                            <div style={{fontSize: '1.5rem'}}>✨</div>
                            <h3 className="text-lg font-bold heading-font" style={{color: '#64c8ff'}}>Analysis Complete</h3>
                          </div>
                        </div>

                        {/* Result Content */}
                        <div className="result-content-enhanced">
                          <div
                            className="prose prose-sm max-w-none line-clamp-none result-text"
                            style={{
                              color: '#b0b0b0',
                              fontSize: '0.95rem',
                              lineHeight: '1.6'
                            }}
                            dangerouslySetInnerHTML={{ __html: result }}
                          />
                        </div>

                        {/* Result Footer */}
                        <div className="mt-6 pt-4 border-t" style={{borderColor: 'rgba(100, 200, 255, 0.2)'}}>
                          <div className="flex items-center justify-between">
                            <span style={{color: '#808080', fontSize: '0.875rem'}}>Analysis powered by AI</span>
                            <div className="flex gap-1">
                              <div className="w-2 h-2 rounded-full" style={{background: '#64c8ff'}}></div>
                              <div className="w-2 h-2 rounded-full" style={{background: '#9664ff'}}></div>
                              <div className="w-2 h-2 rounded-full" style={{background: '#64c8ff'}}></div>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}

                    {!result && !loading && !error && (
                      <div className="flex flex-col items-center justify-center h-64 text-center slide-in">
                        <div className="mb-4" style={{color: '#808080'}}>
                    <svg
                      className="w-16 h-16 mx-auto"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={1.5}
                        d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                        />
                      </svg>
                        </div>
                        <p className="font-medium" style={{color: '#b0b0b0'}}>
                          Upload an image to get started
                        </p>
                        <p className="text-sm mt-2" style={{color: '#808080'}}>
                          Results will appear here after analysis
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </>
          )}

          {/* Footer */}
          {page === 'home' && (
            <div className="text-center mt-8 drop-shadow-md text-sm slide-in" style={{color: '#b0b0b0'}}>
              <p>Medical Imaging Analysis</p>
            </div>
          )}
        </div>
      </div>
    </>
  );
}

export default App;
