"""
Download and prepare trained medical imaging models
Supports CheXpert and MIMIC-CXR trained models
"""

import os
import sys
import urllib.request
import zipfile
from pathlib import Path

# Model URLs (these are example URLs - replace with actual trained model URLs)
MODELS = {
    "densenet_chexpert": {
        "url": "https://example.com/models/densenet_chexpert.h5",
        "filename": "densenet_chexpert.h5",
        "description": "DenseNet121 trained on CheXpert dataset (224,316 chest X-rays)",
        "size_mb": 150
    },
    "mobilenet_mimic": {
        "url": "https://example.com/models/mobilenet_mimic.h5",
        "filename": "mobilenet_mimic.h5",
        "description": "MobileNetV2 trained on MIMIC-CXR dataset (377,110 chest X-rays)",
        "size_mb": 85
    },
    "medical_classifier": {
        "url": "https://example.com/models/medical_classifier.h5",
        "filename": "medical_classifier.h5",
        "description": "Custom CNN trained on combined medical datasets",
        "size_mb": 120
    }
}

def create_models_directory():
    """Create models directory if it doesn't exist"""
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    print(f"✓ Models directory ready: {models_dir.absolute()}")
    return models_dir

def download_model(model_key, model_info, models_dir):
    """Download a trained model"""
    url = model_info["url"]
    filename = model_info["filename"]
    filepath = models_dir / filename
    
    # Check if model already exists
    if filepath.exists():
        print(f"✓ {filename} already exists (skipping download)")
        return True
    
    print(f"\n📥 Downloading {filename}...")
    print(f"   Description: {model_info['description']}")
    print(f"   Size: ~{model_info['size_mb']} MB")
    
    try:
        # Download with progress
        def download_progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = min(downloaded * 100 // total_size, 100)
            sys.stdout.write(f"\r   Progress: {percent}%")
            sys.stdout.flush()
        
        urllib.request.urlretrieve(url, filepath, download_progress)
        print(f"\n✓ Successfully downloaded {filename}")
        return True
    except Exception as e:
        print(f"\n✗ Error downloading {filename}: {e}")
        print(f"   Please download manually from: {url}")
        return False

def verify_models(models_dir):
    """Verify that models are available"""
    print("\n" + "="*60)
    print("MODEL VERIFICATION")
    print("="*60)
    
    available_models = []
    missing_models = []
    
    for model_key, model_info in MODELS.items():
        filepath = models_dir / model_info["filename"]
        if filepath.exists():
            size_mb = filepath.stat().st_size / (1024 * 1024)
            available_models.append(model_info["filename"])
            print(f"✓ {model_info['filename']} ({size_mb:.1f} MB)")
        else:
            missing_models.append(model_info["filename"])
            print(f"✗ {model_info['filename']} (NOT FOUND)")
    
    print("\n" + "-"*60)
    if available_models:
        print(f"Available Models: {len(available_models)}")
        for model in available_models:
            print(f"  • {model}")
    
    if missing_models:
        print(f"\nMissing Models: {len(missing_models)}")
        for model in missing_models:
            print(f"  • {model}")
        print("\nNote: The application will use fallback models if trained models are unavailable.")
    
    return len(available_models), len(missing_models)

def setup_models():
    """Main setup function"""
    print("="*60)
    print("MEDICAL IMAGING MODELS SETUP")
    print("="*60)
    print("\nThis script helps download trained medical imaging models")
    print("trained on CheXpert and MIMIC-CXR datasets.\n")
    
    # Create models directory
    models_dir = create_models_directory()
    
    # Download models
    print("\n" + "="*60)
    print("DOWNLOADING MODELS")
    print("="*60)
    
    downloaded = 0
    for model_key, model_info in MODELS.items():
        if download_model(model_key, model_info, models_dir):
            downloaded += 1
    
    # Verify
    available, missing = verify_models(models_dir)
    
    print("\n" + "="*60)
    print("SETUP COMPLETE")
    print("="*60)
    print(f"\nModels Ready: {available}/{len(MODELS)}")
    
    if missing > 0:
        print(f"\n⚠️  {missing} model(s) not available.")
        print("The application will use fallback models or create new ones.")
    else:
        print("\n✓ All trained medical models are ready!")
        print("Your application will use the trained models for analysis.")
    
    print("\nTo use custom trained models:")
    print("1. Place your .h5 model files in the 'models/' directory")
    print("2. Name them: densenet_chexpert.h5, mobilenet_mimic.h5, medical_classifier.h5")
    print("3. Restart the application")

def create_sample_model():
    """Create a sample model for testing (if no real models available)"""
    print("\n" + "="*60)
    print("CREATING SAMPLE MODELS FOR TESTING")
    print("="*60)
    
    try:
        import tensorflow as tf
        from tensorflow.keras.applications import DenseNet121, MobileNetV2
        from tensorflow.keras.models import Model
        
        models_dir = Path("models")
        models_dir.mkdir(exist_ok=True)
        
        # Create sample DenseNet model
        print("\nCreating sample DenseNet121 model...")
        base_model = DenseNet121(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        x = base_model.output
        x = tf.keras.layers.GlobalAveragePooling2D()(x)
        x = tf.keras.layers.Dense(512, activation='relu')(x)
        x = tf.keras.layers.Dropout(0.5)(x)
        predictions = tf.keras.layers.Dense(14, activation='sigmoid')(x)
        model = Model(inputs=base_model.input, outputs=predictions)
        model.save(models_dir / "densenet_chexpert.h5")
        print("✓ Sample DenseNet model created")
        
        # Create sample MobileNetV2 model
        print("Creating sample MobileNetV2 model...")
        base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        x = base_model.output
        x = tf.keras.layers.GlobalAveragePooling2D()(x)
        x = tf.keras.layers.Dense(256, activation='relu')(x)
        x = tf.keras.layers.Dropout(0.4)(x)
        predictions = tf.keras.layers.Dense(10, activation='sigmoid')(x)
        model = Model(inputs=base_model.input, outputs=predictions)
        model.save(models_dir / "mobilenet_mimic.h5")
        print("✓ Sample MobileNetV2 model created")
        
        print("\n✓ Sample models created successfully!")
        print("Note: These are untrained models for testing purposes only.")
        print("For production use, train on actual medical datasets.")
        
    except ImportError:
        print("✗ TensorFlow not installed. Cannot create sample models.")
        print("Install TensorFlow: pip install tensorflow")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Download and setup medical imaging models")
    parser.add_argument("--create-sample", action="store_true", 
                       help="Create sample models for testing (requires TensorFlow)")
    parser.add_argument("--verify-only", action="store_true",
                       help="Only verify existing models without downloading")
    
    args = parser.parse_args()
    
    if args.verify_only:
        models_dir = Path("models")
        models_dir.mkdir(exist_ok=True)
        verify_models(models_dir)
    elif args.create_sample:
        create_sample_model()
    else:
        setup_models()
