"""
Generate a tiny synthetic image dataset for demo/training.

Creates an images directory (default: uploads_demo/) and a labels.csv file with simple labels
based on brightness/contrast so the lightweight features are predictive.

Usage:
    python generate_demo_dataset.py --out_dir uploads_demo --count 20
"""
from PIL import Image, ImageDraw
import numpy as np
import os
import csv
import argparse


def make_image(path, size=(224,224), mean=128, noise=20):
    arr = np.clip(np.random.normal(loc=mean, scale=noise, size=(size[1], size[0])), 0, 255).astype('uint8')
    img = Image.fromarray(arr)
    img.save(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out_dir', default='uploads_demo')
    parser.add_argument('--count', type=int, default=20)
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    labels_path = os.path.join(args.out_dir, 'labels.csv')

    # Create images and labels. We'll create two classes: normal and abnormal
    n = args.count
    half = n // 2
    rows = []
    for i in range(n):
        if i < half:
            # normal: mean around 120-140
            mean = int(120 + np.random.rand()*20)
            label = 'normal'
        else:
            # abnormal: either too dark or too bright
            if np.random.rand() < 0.5:
                mean = int(30 + np.random.rand()*20)  # dark
            else:
                mean = int(220 - np.random.rand()*20)  # bright
            label = 'abnormal'

        fname = f'img_{i:03d}.png'
        path = os.path.join(args.out_dir, fname)
        make_image(path, mean=mean, noise=15)
        rows.append({'filename': fname, 'label': label})

    # write labels CSV at the root (train_model expects labels path separate)
    labels_csv = os.path.join(args.out_dir, 'labels.csv')
    with open(labels_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['filename','label'])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print(f'Created {n} images in {args.out_dir} and labels at {labels_csv}')


if __name__ == '__main__':
    main()
