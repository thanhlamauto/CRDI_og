#!/usr/bin/env python3
"""
Select face images of children under 3 years old from FFHQ dataset.
Usage: python select_children_under3.py
"""

import csv
import os
import shutil
from pathlib import Path

# Configuration
CSV_PATH = "/kaggle/input/aging-labels/ffhq_aging_labels.csv"  # Path to CSV file
SOURCE_DIR = "/kaggle/working/ffhq/Part1"  # Source directory with images
OUTPUT_DIR = "/kaggle/working/children_under3"  # Output directory
AGE_GROUP = "0-2"  # Age group for children under 3 years (0-2 years)

def main():
    print("=" * 70)
    print("FFHQ Children Image Selection Tool")
    print("=" * 70)
    print(f"CSV file: {CSV_PATH}")
    print(f"Source directory: {SOURCE_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Age group: {AGE_GROUP} (children under 3 years)")
    print("=" * 70)
    
    # Load CSV metadata
    print("\n[1/4] Loading CSV metadata...")
    try:
        with open(CSV_PATH, 'r') as f:
            csv_reader = csv.DictReader(f)
            all_data = list(csv_reader)
        print(f"✓ Loaded metadata for {len(all_data)} images")
    except FileNotFoundError:
        print(f"✗ Error: CSV file not found: {CSV_PATH}")
        return
    except Exception as e:
        print(f"✗ Error loading CSV: {e}")
        return
    
    # Filter for children in age group 0-2 (under 3 years old)
    print(f"\n[2/4] Filtering children in age group '{AGE_GROUP}'...")
    children_images = []
    
    for row in all_data:
        if row['age_group'] == AGE_GROUP:
            image_number = int(row['image_number'])
            # Convert image number to 5-digit padded format (e.g., 0 -> 00000)
            image_id = f"{image_number:05d}"
            
            children_images.append({
                'image_id': image_id,
                'image_number': image_number,
                'filename': f"{image_id}.png",
                'age_group': row['age_group'],
                'age_group_confidence': row['age_group_confidence'],
                'gender': row['gender'],
                'gender_confidence': row['gender_confidence']
            })
    
    # Sort by image number
    children_images.sort(key=lambda x: x['image_number'])
    
    print(f"✓ Found {len(children_images)} children in age group '{AGE_GROUP}'")
    
    if not children_images:
        print("\n✗ No images found matching the criteria.")
        return
    
    # Display statistics
    print(f"\n   Statistics:")
    print(f"   - Total images: {len(children_images)}")
    print(f"   - Age group: {AGE_GROUP} years")
    
    # Gender distribution
    gender_count = {}
    for item in children_images:
        gender = item['gender']
        gender_count[gender] = gender_count.get(gender, 0) + 1
    
    print(f"   - Gender distribution:")
    for gender, count in sorted(gender_count.items()):
        print(f"     {gender}: {count}")
    
    # Create output directory
    print(f"\n[3/4] Creating output directory...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"✓ Output directory: {OUTPUT_DIR}")
    
    # Save metadata CSV
    csv_path = os.path.join(OUTPUT_DIR, 'children_metadata.csv')
    with open(csv_path, 'w') as f:
        f.write("image_id,image_number,filename,age_group,age_group_confidence,gender,gender_confidence\n")
        for item in children_images:
            f.write(f"{item['image_id']},{item['image_number']},{item['filename']},{item['age_group']},{item['age_group_confidence']},{item['gender']},{item['gender_confidence']}\n")
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
    print(f"{'Image ID':<10} {'Image #':<10} {'Age Group':<12} {'Gender':<10} {'Confidence':<12}")
    print("-" * 54)
    for item in children_images[:10]:
        print(f"{item['image_id']:<10} {item['image_number']:<10} {item['age_group']:<12} {item['gender']:<10} {item['age_group_confidence']:<12}")

if __name__ == "__main__":
    main()

