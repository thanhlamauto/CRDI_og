"""
Script to select face images of children under 3 years old from FFHQ dataset
based on the ffhq-dataset-v2.json metadata file.
"""

import json
import os
import shutil
from pathlib import Path
from typing import List, Dict


def load_metadata(metadata_path: str) -> Dict:
    """Load the FFHQ metadata JSON file."""
    print(f"Loading metadata from {metadata_path}...")
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    print(f"Metadata loaded successfully!")
    return metadata


def filter_children_under_3(metadata: Dict, age_threshold: float = 3.0) -> List[Dict]:
    """
    Filter images of children under the specified age threshold.
    
    Args:
        metadata: The FFHQ metadata dictionary
        age_threshold: Maximum age to filter (default: 3.0 years)
    
    Returns:
        List of image metadata for children under the age threshold
    """
    children_images = []
    
    print(f"\nFiltering images for children under {age_threshold} years old...")
    
    for image_id, image_data in metadata.items():
        # Check if age information exists
        if 'category' in image_data and 'age' in image_data['category']:
            age = image_data['category']['age']
            
            # Filter for children under the age threshold
            if age is not None and age < age_threshold:
                children_images.append({
                    'image_id': image_id,
                    'age': age,
                    'data': image_data
                })
    
    return children_images


def get_image_filename(image_id: str, source_dir: str) -> str:
    """
    Get the full path to the image file.
    
    Args:
        image_id: The image ID (e.g., "00000")
        source_dir: The directory containing the images
    
    Returns:
        Full path to the image file
    """
    # FFHQ images are typically named as 5-digit numbers with .png extension
    filename = f"{image_id}.png"
    return os.path.join(source_dir, filename)


def copy_selected_images(children_images: List[Dict], 
                         source_dir: str, 
                         output_dir: str,
                         create_csv: bool = True):
    """
    Copy selected children images to output directory.
    
    Args:
        children_images: List of filtered children image metadata
        source_dir: Source directory containing FFHQ images
        output_dir: Output directory to copy selected images
        create_csv: Whether to create a CSV file with metadata
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\nCopying {len(children_images)} images to {output_dir}...")
    
    copied_count = 0
    missing_count = 0
    metadata_list = []
    
    for item in children_images:
        image_id = item['image_id']
        age = item['age']
        
        source_path = get_image_filename(image_id, source_dir)
        dest_path = os.path.join(output_dir, f"{image_id}.png")
        
        if os.path.exists(source_path):
            shutil.copy2(source_path, dest_path)
            copied_count += 1
            metadata_list.append({
                'image_id': image_id,
                'filename': f"{image_id}.png",
                'age': age
            })
            
            if copied_count % 10 == 0:
                print(f"  Copied {copied_count} images...")
        else:
            missing_count += 1
            print(f"  Warning: Image not found - {source_path}")
    
    print(f"\nCompleted!")
    print(f"  Successfully copied: {copied_count} images")
    print(f"  Missing images: {missing_count}")
    
    # Create CSV file with metadata
    if create_csv and metadata_list:
        csv_path = os.path.join(output_dir, 'children_metadata.csv')
        with open(csv_path, 'w') as f:
            f.write("image_id,filename,age\n")
            for item in metadata_list:
                f.write(f"{item['image_id']},{item['filename']},{item['age']}\n")
        print(f"\nMetadata saved to: {csv_path}")
    
    return copied_count, missing_count


def main():
    # Configuration
    METADATA_PATH = "/Users/nguyenthanhlam/Downloads/CRDI/ffhq-dataset-v2.json"
    SOURCE_DIR = "/kaggle/working/ffhq/Part1"
    OUTPUT_DIR = "/kaggle/working/ffhq_children_under3"
    AGE_THRESHOLD = 3.0
    
    print("=" * 60)
    print("FFHQ Children Image Selection")
    print("=" * 60)
    print(f"Metadata file: {METADATA_PATH}")
    print(f"Source directory: {SOURCE_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Age threshold: < {AGE_THRESHOLD} years")
    print("=" * 60)
    
    # Load metadata
    try:
        metadata = load_metadata(METADATA_PATH)
    except Exception as e:
        print(f"Error loading metadata: {e}")
        return
    
    # Filter for children under 3 years old
    children_images = filter_children_under_3(metadata, age_threshold=AGE_THRESHOLD)
    
    print(f"\nFound {len(children_images)} images of children under {AGE_THRESHOLD} years old")
    
    if children_images:
        # Sort by age for easier review
        children_images.sort(key=lambda x: x['age'])
        
        # Print some statistics
        ages = [item['age'] for item in children_images]
        print(f"\nAge statistics:")
        print(f"  Minimum age: {min(ages):.2f} years")
        print(f"  Maximum age: {max(ages):.2f} years")
        print(f"  Average age: {sum(ages)/len(ages):.2f} years")
        
        # Print first few examples
        print(f"\nFirst 10 examples:")
        for item in children_images[:10]:
            print(f"  Image {item['image_id']}: age {item['age']:.2f} years")
        
        # Copy images to output directory
        copied, missing = copy_selected_images(
            children_images, 
            SOURCE_DIR, 
            OUTPUT_DIR,
            create_csv=True
        )
    else:
        print("\nNo images found matching the criteria.")


if __name__ == "__main__":
    main()

