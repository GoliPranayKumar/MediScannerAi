"""
Train a simple ML model from image statistics produced by `ml_model_lite`.

Usage:
    # create CSV with columns: filename,label
    python train_model.py --images_dir uploads --labels labels.csv --output model.joblib

This script extracts lightweight features (mean, std, contrast, size) and trains a RandomForest classifier.
"""
import argparse
import os
import csv
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import numpy as np

from ml_model_lite import extract_features_for_ml


def load_dataset(images_dir, labels_csv):
    X = []
    y = []
    with open(labels_csv, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = row['filename']
            label = row['label']
            img_path = os.path.join(images_dir, filename)
            if not os.path.exists(img_path):
                print(f"Warning: image not found {img_path}, skipping")
                continue
            feats = extract_features_for_ml(img_path)
            X.append([feats['mean_intensity'], feats['std_intensity'], feats['contrast'], feats['width'], feats['height']])
            y.append(label)
    return np.array(X), np.array(y)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--images_dir', required=True)
    parser.add_argument('--labels', required=True, help='CSV with columns filename,label')
    parser.add_argument('--output', default='model.joblib')
    args = parser.parse_args()

    X, y = load_dataset(args.images_dir, args.labels)
    if len(X) == 0:
        print('No training data found. Exiting.')
        return

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    print('Classification report:')
    print(classification_report(y_test, preds))

    joblib.dump(clf, args.output)
    print(f'Saved model to {args.output}')


if __name__ == '__main__':
    main()
