"""
Lightweight Medical Imaging Analysis
Uses PIL for image processing without heavy dependencies
"""

import numpy as np
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

class MedicalImagingAnalyzer:
    """
    Lightweight medical image analyzer
    Analyzes image properties without heavy ML models
    """
    
    def __init__(self):
        """Initialize the analyzer"""
        self.model_loaded = True
    
    def analyze_image(self, image_path):
        """
        Analyze medical image and return findings
        """
        try:
            # Open image
            img = Image.open(image_path)
            img_array = np.array(img)
            
            # Image properties
            height, width = img_array.shape[:2]
            
            # Calculate statistics
            if len(img_array.shape) == 3:
                # Color image
                mean_intensity = np.mean(img_array)
                std_intensity = np.std(img_array)
                contrast = std_intensity / (mean_intensity + 1e-6)
            else:
                # Grayscale
                mean_intensity = np.mean(img_array)
                std_intensity = np.std(img_array)
                contrast = std_intensity / (mean_intensity + 1e-6)
            
            # Determine image type
            if mean_intensity < 50:
                image_type = "Dark/Low Intensity Image"
                characteristics = "Low brightness, may indicate underexposed scan"
            elif mean_intensity > 200:
                image_type = "Bright/High Intensity Image"
                characteristics = "High brightness, may indicate overexposed scan"
            else:
                image_type = "Normal Intensity Image"
                characteristics = "Optimal brightness levels detected"
            
            # Quality assessment
            if contrast < 0.3:
                quality = "Low Contrast - May affect diagnosis"
            elif contrast > 1.5:
                quality = "High Contrast - Good for analysis"
            else:
                quality = "Moderate Contrast - Acceptable quality"
            
            # Generate findings
            findings = {
                "image_type": image_type,
                "dimensions": f"{width}x{height} pixels",
                "mean_intensity": f"{mean_intensity:.2f}",
                "contrast_ratio": f"{contrast:.2f}",
                "characteristics": characteristics,
                "quality_assessment": quality,
                "recommendations": self._get_recommendations(mean_intensity, contrast)
            }
            
            return findings
            
        except Exception as e:
            return {"error": str(e)}
    
    def _get_recommendations(self, intensity, contrast):
        """Generate recommendations based on image analysis"""
        recommendations = []
        
        if intensity < 50:
            recommendations.append("Increase brightness/exposure for better visibility")
        elif intensity > 200:
            recommendations.append("Reduce brightness/exposure to prevent overexposure")
        
        if contrast < 0.3:
            recommendations.append("Improve contrast for better diagnostic accuracy")
        
        if not recommendations:
            recommendations.append("Image quality is suitable for analysis")
        
        return recommendations

def get_analyzer():
    """Get analyzer instance"""
    return MedicalImagingAnalyzer()
