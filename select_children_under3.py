#!/usr/bin/env python3
"""
Select face images of children under 3 years old from FFHQ dataset.
Usage: python select_children_under3.py
"""

import json
import os
import shutil
from pathlib import Path

# Configuration
METADATA_PATH = "ffhq-dataset-v2.json"  # Path to metadata file
SOURCE_DIR = "/kaggle/working/ffhq/Part1"  # Source directory with images
OUTPUT_DIR = "/kaggle/working/children_under3"  # Output directory
AGE_THRESHOLD = 3.0  # Maximum age in years

def main():
    print("=" * 70)
    print("FFHQ Children Image Selection Tool")
    print("=" * 70)
    print(f"Metadata file: {METADATA_PATH}")
    print(f"Source directory: {SOURCE_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Age threshold: < {AGE_THRESHOLD} years")
    print("=" * 70)
    
    # Load metadata
    print("\n[1/4] Loading metadata...")
    try:
        with open(METADATA_PATH, 'r') as f:
            metadata = json.load(f)
        print(f"✓ Loaded metadata for {len(metadata)} images")
    except FileNotFoundError:
        print(f"✗ Error: Metadata file not found: {METADATA_PATH}")
        return
    except Exception as e:
        print(f"✗ Error loading metadata: {e}")
        return
    
    # Filter for children under 3 years old
    print(f"\n[2/4] Filtering children under {AGE_THRESHOLD} years...")
    children_images = []
    
    for image_id, image_data in metadata.items():
        if 'category' in image_data and 'age' in image_data['category']:
            age = image_data['category']['age']
            
            if age is not None and age < AGE_THRESHOLD:
                children_images.append({
                    'image_id': image_id,
                    'filename': f"{image_id}.png",
                    'age': age,
                    'gender': image_data['category'].get('gender', 'unknown')
                })
    
    # Sort by age
    children_images.sort(key=lambda x: x['age'])
    
    print(f"✓ Found {len(children_images)} children under {AGE_THRESHOLD} years")
    
    if not children_images:
        print("\n✗ No images found matching the criteria.")
        return
    
    # Display statistics
    ages = [item['age'] for item in children_images]
    print(f"\n   Statistics:")
    print(f"   - Minimum age: {min(ages):.2f} years")
    print(f"   - Maximum age: {max(ages):.2f} years")
    print(f"   - Average age: {sum(ages)/len(ages):.2f} years")
    print(f"   - Median age: {sorted(ages)[len(ages)//2]:.2f} years")
    
    # Create output directory
    print(f"\n[3/4] Creating output directory...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"✓ Output directory: {OUTPUT_DIR}")
    
    # Save metadata CSV
    csv_path = os.path.join(OUTPUT_DIR, 'children_metadata.csv')
    with open(csv_path, 'w') as f:
        f.write("image_id,filename,age,gender\n")
        for item in children_images:
            f.write(f"{item['image_id']},{item['filename']},{item['age']},{item['gender']}\n")
    print(f"✓ Saved metadata: {csv_path}")
    
    # Save image IDs list
    txt_path = os.path.join(OUTPUT_DIR, 'children_ids.txt')
    with open(txt_path, 'w') as f:
        for item in children_images:
            f.write(f"{item['image_id']}\n")
    print(f"✓ Saved image IDs: {txt_path}")
    
    # Copy images
    print(f"\n[4/4] Copying images to output directory...")
    if not os.path.exists(SOURCE_DIR):
        print(f"⚠ Warning: Source directory not found: {SOURCE_DIR}")
        print(f"   Metadata files have been created, but images cannot be copied.")
        print(f"   Please check the source directory path.")
        return
    
    copied_count = 0
    missing_count = 0
    
    for idx, item in enumerate(children_images, 1):
        image_id = item['image_id']
        source_path = os.path.join(SOURCE_DIR, f"{image_id}.png")
        dest_path = os.path.join(OUTPUT_DIR, f"{image_id}.png")
        
        if os.path.exists(source_path):
            shutil.copy2(source_path, dest_path)
            copied_count += 1
            
            if copied_count % 10 == 0 or copied_count == len(children_images):
                print(f"   Progress: {copied_count}/{len(children_images)} images copied...", end='\r')
        else:
            missing_count += 1
    
    print()  # New line after progress
    print(f"✓ Successfully copied: {copied_count} images")
    if missing_count > 0:
        print(f"⚠ Missing images: {missing_count}")
    
    # Final summary
    print("\n" + "=" * 70)
    print("COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print(f"Total images found: {len(children_images)}")
    print(f"Images copied: {copied_count}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Metadata CSV: {csv_path}")
    print(f"Image IDs list: {txt_path}")
    print("=" * 70)
    
    # Display first 10 examples
    print("\nFirst 10 examples:")
    print(f"{'Image ID':<10} {'Age (years)':<15} {'Gender':<10}")
    print("-" * 35)
    for item in children_images[:10]:
        print(f"{item['image_id']:<10} {item['age']:<15.2f} {item['gender']:<10}")

if __name__ == "__main__":
    main()

