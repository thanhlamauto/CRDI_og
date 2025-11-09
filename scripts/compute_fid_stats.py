#!/usr/bin/env python3
"""
Compute FID statistics (mu and sigma) from a directory of images and save as .npz file.
Usage: python compute_fid_stats.py --image_dir <path> --output <output.npz>
"""

import argparse
import os
import sys
import numpy as np
from pathlib import Path
from PIL import Image

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from tqdm import tqdm

from src.fs_gradients.fid_score import InceptionV3


class ImageFolderDataset(Dataset):
    """Dataset for loading images from a folder"""
    
    def __init__(self, image_dir, transform=None):
        self.image_dir = Path(image_dir)
        self.image_files = []
        
        # Find all image files
        for ext in ['*.png', '*.jpg', '*.jpeg', '*.PNG', '*.JPG', '*.JPEG']:
            self.image_files.extend(self.image_dir.glob(ext))
        
        self.image_files = sorted(self.image_files)
        self.transform = transform
        
        print(f"Found {len(self.image_files)} images in {image_dir}")
    
    def __len__(self):
        return len(self.image_files)
    
    def __getitem__(self, idx):
        img_path = self.image_files[idx]
        image = Image.open(img_path).convert('RGB')
        
        if self.transform:
            image = self.transform(image)
        
        return image


def calculate_activation_statistics(dataloader, model, dims, device):
    """Calculate mean and covariance of activations"""
    model.eval()
    
    activations = []
    
    with torch.no_grad():
        for batch in tqdm(dataloader, desc="Computing activations"):
            batch = batch.to(device)
            pred = model(batch)[0]
            
            # If model output is not scalar, apply global spatial average pooling
            if pred.size(2) != 1 or pred.size(3) != 1:
                pred = torch.nn.functional.adaptive_avg_pool2d(pred, output_size=(1, 1))
            
            pred = pred.squeeze(3).squeeze(2).cpu().numpy()
            activations.append(pred)
    
    activations = np.concatenate(activations, axis=0)
    mu = np.mean(activations, axis=0)
    sigma = np.cov(activations, rowvar=False)
    
    return mu, sigma


def main():
    parser = argparse.ArgumentParser(description='Compute FID statistics from image directory')
    parser.add_argument('--image_dir', type=str, required=True,
                        help='Directory containing images')
    parser.add_argument('--output', type=str, required=True,
                        help='Output .npz file path')
    parser.add_argument('--batch_size', type=int, default=50,
                        help='Batch size for processing')
    parser.add_argument('--image_size', type=int, default=256,
                        help='Image size (default: 256)')
    parser.add_argument('--dims', type=int, default=2048,
                        help='Dimensionality of Inception features')
    args = parser.parse_args()
    
    print("=" * 70)
    print("FID Statistics Computation")
    print("=" * 70)
    print(f"Image directory: {args.image_dir}")
    print(f"Output file: {args.output}")
    print(f"Batch size: {args.batch_size}")
    print(f"Image size: {args.image_size}")
    print("=" * 70)
    
    # Setup device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Setup transform
    transform = transforms.Compose([
        transforms.Resize((args.image_size, args.image_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])
    
    # Load dataset
    dataset = ImageFolderDataset(args.image_dir, transform=transform)
    
    if len(dataset) == 0:
        print("Error: No images found in directory!")
        return
    
    dataloader = DataLoader(dataset, batch_size=args.batch_size, 
                           shuffle=False, num_workers=4)
    
    # Setup InceptionV3 model
    block_idx = InceptionV3.BLOCK_INDEX_BY_DIM[args.dims]
    model = InceptionV3([block_idx]).to(device)
    model.eval()
    
    # Compute statistics
    print("\nComputing FID statistics...")
    mu, sigma = calculate_activation_statistics(dataloader, model, args.dims, device)
    
    # Save to npz file
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    np.savez(args.output, mu=mu, sigma=sigma)
    
    print(f"\n✓ Statistics saved to: {args.output}")
    print(f"  - mu shape: {mu.shape}")
    print(f"  - sigma shape: {sigma.shape}")
    print("=" * 70)


if __name__ == "__main__":
    main()

