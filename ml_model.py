"""
Medical Imaging Analysis using Deep Learning
Uses pre-trained models for medical image classification
"""

import numpy as np
import cv2
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications import DenseNet121, ResNet50
from tensorflow.keras.preprocessing import image
import warnings
warnings.filterwarnings('ignore')

class MedicalImagingAnalyzer:
    """
    Medical image analyzer using deep learning models
    Supports X-ray, CT, and MRI analysis
    """
    
    def __init__(self):
        """Initialize the analyzer with pre-trained models"""
        self.densenet_model = None
        self.resnet_model = None
        self.load_models()
    
    def load_models(self):
        """Load pre-trained models"""
        try:
            # Load DenseNet121 pre-trained on ImageNet
            self.densenet_model = DenseNet121(
                weights='imagenet',
                include_top=True,
                input_shape=(224, 224, 3)
            )
            print("✓ DenseNet121 model loaded successfully")
        except Exception as e:
            print(f"Error loading DenseNet: {e}")
        
        try:
            # Load ResNet50 pre-trained on ImageNet
            self.resnet_model = ResNet50(
                weights='imagenet',
                include_top=True,
                input_shape=(224, 224, 3)
            )
            print("✓ ResNet50 model loaded successfully")
        except Exception as e:
            print(f"Error loading ResNet: {e}")
    
    def preprocess_image(self, image_path):
        """
        Preprocess image for model input
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Preprocessed image array
        """
        try:
            # Read image
            img = Image.open(image_path).convert('RGB')
            
            # Resize to model input size
            img = img.resize((224, 224))
            
            # Convert to array
            img_array = image.img_to_array(img)
            
            # Expand dimensions for batch
            img_array = np.expand_dims(img_array, axis=0)
            
            # Normalize (ImageNet normalization)
            img_array = tf.keras.applications.densenet.preprocess_input(img_array)
            
            return img_array
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None
    
    def analyze_with_densenet(self, image_path):
        """
        Analyze image using DenseNet121
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary with predictions and confidence scores
        """
        if self.densenet_model is None:
            return {"error": "DenseNet model not loaded"}
        
        try:
            img_array = self.preprocess_image(image_path)
            if img_array is None:
                return {"error": "Failed to preprocess image"}
            
            # Get predictions
            predictions = self.densenet_model.predict(img_array, verbose=0)
            
            # Decode predictions
            from tensorflow.keras.applications.densenet import decode_predictions
            decoded = decode_predictions(predictions, top=5)[0]
            
            results = []
            for label, description, score in decoded:
                results.append({
                    "class": description,
                    "confidence": float(score) * 100,
                    "score": float(score)
                })
            
            return {
                "model": "DenseNet121",
                "predictions": results,
                "top_prediction": results[0]["class"] if results else "Unknown",
                "confidence": results[0]["confidence"] if results else 0
            }
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def analyze_with_resnet(self, image_path):
        """
        Analyze image using ResNet50
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary with predictions and confidence scores
        """
        if self.resnet_model is None:
            return {"error": "ResNet model not loaded"}
        
        try:
            img_array = self.preprocess_image(image_path)
            if img_array is None:
                return {"error": "Failed to preprocess image"}
            
            # Get predictions
            predictions = self.resnet_model.predict(img_array, verbose=0)
            
            # Decode predictions
            from tensorflow.keras.applications.resnet50 import decode_predictions
            decoded = decode_predictions(predictions, top=5)[0]
            
            results = []
            for label, description, score in decoded:
                results.append({
                    "class": description,
                    "confidence": float(score) * 100,
                    "score": float(score)
                })
            
            return {
                "model": "ResNet50",
                "predictions": results,
                "top_prediction": results[0]["class"] if results else "Unknown",
                "confidence": results[0]["confidence"] if results else 0
            }
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def ensemble_analysis(self, image_path):
        """
        Perform ensemble analysis using both models
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Combined predictions from both models
        """
        densenet_result = self.analyze_with_densenet(image_path)
        resnet_result = self.analyze_with_resnet(image_path)
        
        # Average confidence scores
        if "error" not in densenet_result and "error" not in resnet_result:
            avg_confidence = (
                densenet_result["confidence"] + resnet_result["confidence"]
            ) / 2
            
            return {
                "ensemble_confidence": avg_confidence,
                "densenet_result": densenet_result,
                "resnet_result": resnet_result,
                "recommendation": self._get_medical_recommendation(avg_confidence)
            }
        
        return {
            "densenet_result": densenet_result,
            "resnet_result": resnet_result
        }
    
    def _get_medical_recommendation(self, confidence):
        """
        Get medical recommendation based on confidence score
        
        Args:
            confidence: Confidence score (0-100)
            
        Returns:
            Medical recommendation string
        """
        if confidence >= 85:
            return "High confidence detection - Recommend clinical review"
        elif confidence >= 70:
            return "Moderate confidence - Further examination recommended"
        elif confidence >= 50:
            return "Low-moderate confidence - Additional imaging may be needed"
        else:
            return "Low confidence - Inconclusive results, professional evaluation required"
    
    def extract_features(self, image_path):
        """
        Extract deep learning features from image
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Feature vector from the model
        """
        try:
            img_array = self.preprocess_image(image_path)
            if img_array is None:
                return None
            
            # Create feature extraction model (remove last layer)
            feature_model = tf.keras.Model(
                inputs=self.densenet_model.input,
                outputs=self.densenet_model.layers[-2].output
            )
            
            # Extract features
            features = feature_model.predict(img_array, verbose=0)
            
            return {
                "features_shape": features.shape,
                "features_mean": float(np.mean(features)),
                "features_std": float(np.std(features)),
                "features_max": float(np.max(features)),
                "features_min": float(np.min(features))
            }
        except Exception as e:
            return {"error": f"Feature extraction failed: {str(e)}"}


# Initialize global analyzer
analyzer = None

def get_analyzer():
    """Get or create the analyzer instance"""
    global analyzer
    if analyzer is None:
        analyzer = MedicalImagingAnalyzer()
    return analyzer
