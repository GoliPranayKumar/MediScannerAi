"""
Training script for medical imaging models
Train DenseNet121 and MobileNetV2 on medical imaging datasets
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import DenseNet121, MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from pathlib import Path
import argparse
import json

class MedicalModelTrainer:
    """Train medical imaging models on custom datasets"""
    
    def __init__(self, dataset_path, model_type="densenet"):
        """
        Initialize trainer
        
        Args:
            dataset_path: Path to dataset directory
            model_type: "densenet" or "mobilenet"
        """
        self.dataset_path = Path(dataset_path)
        self.model_type = model_type
        self.model = None
        self.history = None
        
    def prepare_dataset(self, img_size=224, batch_size=32):
        """
        Prepare dataset for training
        
        Expected directory structure:
        dataset/
        ├── train/
        │   ├── class1/
        │   ├── class2/
        │   └── ...
        ├── val/
        │   ├── class1/
        │   ├── class2/
        │   └── ...
        └── test/
            ├── class1/
            ├── class2/
            └── ...
        """
        print("Preparing dataset...")
        
        # Data augmentation for training
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest'
        )
        
        # Only rescaling for validation/test
        val_datagen = ImageDataGenerator(rescale=1./255)
        
        # Load training data
        train_dir = self.dataset_path / "train"
        train_generator = train_datagen.flow_from_directory(
            train_dir,
            target_size=(img_size, img_size),
            batch_size=batch_size,
            class_mode='categorical'
        )
        
        # Load validation data
        val_dir = self.dataset_path / "val"
        val_generator = val_datagen.flow_from_directory(
            val_dir,
            target_size=(img_size, img_size),
            batch_size=batch_size,
            class_mode='categorical'
        )
        
        # Load test data
        test_dir = self.dataset_path / "test"
        test_generator = val_datagen.flow_from_directory(
            test_dir,
            target_size=(img_size, img_size),
            batch_size=batch_size,
            class_mode='categorical',
            shuffle=False
        )
        
        print(f"✓ Training samples: {train_generator.samples}")
        print(f"✓ Validation samples: {val_generator.samples}")
        print(f"✓ Test samples: {test_generator.samples}")
        print(f"✓ Classes: {train_generator.num_classes}")
        
        return train_generator, val_generator, test_generator
    
    def build_model(self, num_classes):
        """Build medical imaging model"""
        print(f"\nBuilding {self.model_type} model for {num_classes} classes...")
        
        if self.model_type == "densenet":
            # Load DenseNet121 pre-trained on ImageNet
            base_model = DenseNet121(
                weights='imagenet',
                include_top=False,
                input_shape=(224, 224, 3)
            )
            
            # Add medical-specific layers
            x = base_model.output
            x = GlobalAveragePooling2D()(x)
            x = Dense(512, activation='relu')(x)
            x = Dropout(0.5)(x)
            predictions = Dense(num_classes, activation='softmax')(x)
            
            self.model = Model(inputs=base_model.input, outputs=predictions)
            
            # Freeze base layers for transfer learning
            for layer in base_model.layers:
                layer.trainable = False
            
            print("✓ DenseNet121 model built with transfer learning")
            
        elif self.model_type == "mobilenet":
            # Load MobileNetV2 pre-trained on ImageNet
            base_model = MobileNetV2(
                weights='imagenet',
                include_top=False,
                input_shape=(224, 224, 3)
            )
            
            # Add medical-specific layers
            x = base_model.output
            x = GlobalAveragePooling2D()(x)
            x = Dense(256, activation='relu')(x)
            x = Dropout(0.4)(x)
            predictions = Dense(num_classes, activation='softmax')(x)
            
            self.model = Model(inputs=base_model.input, outputs=predictions)
            
            # Freeze base layers
            for layer in base_model.layers:
                layer.trainable = False
            
            print("✓ MobileNetV2 model built with transfer learning")
        
        # Compile model
        self.model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy', tf.keras.metrics.AUC()]
        )
        
        print(f"✓ Model compiled")
        print(f"  Total parameters: {self.model.count_params():,}")
    
    def train(self, train_generator, val_generator, epochs=50, save_path="models"):
        """Train the model"""
        print(f"\nTraining {self.model_type} model for {epochs} epochs...")
        
        # Callbacks
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=5,
                restore_best_weights=True
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=3,
                min_lr=1e-7
            ),
            tf.keras.callbacks.ModelCheckpoint(
                f"{save_path}/best_{self.model_type}.h5",
                monitor='val_accuracy',
                save_best_only=True
            )
        ]
        
        # Train
        self.history = self.model.fit(
            train_generator,
            validation_data=val_generator,
            epochs=epochs,
            callbacks=callbacks,
            verbose=1
        )
        
        print("✓ Training complete")
        return self.history
    
    def evaluate(self, test_generator):
        """Evaluate model on test set"""
        print("\nEvaluating model on test set...")
        
        results = self.model.evaluate(test_generator, verbose=0)
        
        print(f"✓ Test Loss: {results[0]:.4f}")
        print(f"✓ Test Accuracy: {results[1]:.4f}")
        if len(results) > 2:
            print(f"✓ Test AUC: {results[2]:.4f}")
        
        return results
    
    def save_model(self, save_path="models"):
        """Save trained model"""
        Path(save_path).mkdir(exist_ok=True)
        
        if self.model_type == "densenet":
            filename = f"{save_path}/densenet_chexpert.h5"
        else:
            filename = f"{save_path}/mobilenet_mimic.h5"
        
        self.model.save(filename)
        print(f"✓ Model saved to {filename}")
        
        return filename
    
    def save_training_info(self, save_path="models"):
        """Save training information"""
        if self.history is None:
            return
        
        info = {
            "model_type": self.model_type,
            "epochs_trained": len(self.history.history['loss']),
            "final_train_loss": float(self.history.history['loss'][-1]),
            "final_val_loss": float(self.history.history['val_loss'][-1]),
            "final_train_accuracy": float(self.history.history['accuracy'][-1]),
            "final_val_accuracy": float(self.history.history['val_accuracy'][-1]),
            "best_val_accuracy": float(max(self.history.history['val_accuracy']))
        }
        
        info_file = f"{save_path}/{self.model_type}_training_info.json"
        with open(info_file, 'w') as f:
            json.dump(info, f, indent=2)
        
        print(f"✓ Training info saved to {info_file}")

def main():
    parser = argparse.ArgumentParser(description="Train medical imaging models")
    parser.add_argument("--dataset", required=True, help="Path to dataset directory")
    parser.add_argument("--model", choices=["densenet", "mobilenet"], default="densenet",
                       help="Model type to train")
    parser.add_argument("--epochs", type=int, default=50, help="Number of epochs")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size")
    parser.add_argument("--output", default="models", help="Output directory for models")
    
    args = parser.parse_args()
    
    print("="*60)
    print("MEDICAL IMAGING MODEL TRAINER")
    print("="*60)
    
    # Initialize trainer
    trainer = MedicalModelTrainer(args.dataset, args.model)
    
    # Prepare dataset
    train_gen, val_gen, test_gen = trainer.prepare_dataset(batch_size=args.batch_size)
    
    # Build model
    trainer.build_model(train_gen.num_classes)
    
    # Train
    trainer.train(train_gen, val_gen, epochs=args.epochs, save_path=args.output)
    
    # Evaluate
    trainer.evaluate(test_gen)
    
    # Save
    trainer.save_model(args.output)
    trainer.save_training_info(args.output)
    
    print("\n" + "="*60)
    print("TRAINING COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
