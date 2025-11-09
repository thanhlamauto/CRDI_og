"""
Script to list face images of children under 3 years old from FFHQ dataset.
This version only creates a list/CSV without copying files.
"""

import json
import os
import pandas as pd
from typing import List, Dict


def load_and_filter_children(metadata_path: str, age_threshold: float = 3.0) -> pd.DataFrame:
    """
    Load metadata and filter for children under specified age.
    
    Args:
        metadata_path: Path to ffhq-dataset-v2.json
        age_threshold: Maximum age to filter (default: 3.0 years)
    
    Returns:
        DataFrame with filtered children image information
    """
    print(f"Loading metadata from {metadata_path}...")
    
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    print(f"Metadata loaded! Total images: {len(metadata)}")
    
    # Filter for children
    children_data = []
    
    for image_id, image_data in metadata.items():
        if 'category' in image_data and 'age' in image_data['category']:
            age = image_data['category']['age']
            
            if age is not None and age < age_threshold:
                # Extract additional useful information
                row = {
                    'image_id': image_id,
                    'filename': f"{image_id}.png",
                    'age': age
                }
                
                # Add gender if available
                if 'gender' in image_data['category']:
                    row['gender'] = image_data['category']['gender']
                
                # Add other metadata if available
                if 'in_the_wild' in image_data:
                    row['in_the_wild'] = image_data['in_the_wild']
                
                children_data.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(children_data)
    
    # Sort by age
    if not df.empty:
        df = df.sort_values('age').reset_index(drop=True)
    
    return df


def main():
    # Configuration
    METADATA_PATH = "/Users/nguyenthanhlam/Downloads/CRDI/ffhq-dataset-v2.json"
    OUTPUT_CSV = "/kaggle/working/ffhq_children_under3.csv"
    AGE_THRESHOLD = 3.0
    
    print("=" * 60)
    print("FFHQ Children Image List Generator")
    print("=" * 60)
    print(f"Age threshold: < {AGE_THRESHOLD} years")
    print("=" * 60)
    
    # Load and filter
    try:
        df = load_and_filter_children(METADATA_PATH, age_threshold=AGE_THRESHOLD)
    except Exception as e:
        print(f"Error: {e}")
        return
    
    # Display results
    print(f"\n✓ Found {len(df)} images of children under {AGE_THRESHOLD} years old")
    
    if not df.empty:
        # Statistics
        print(f"\nAge statistics:")
        print(f"  Minimum age: {df['age'].min():.2f} years")
        print(f"  Maximum age: {df['age'].max():.2f} years")
        print(f"  Average age: {df['age'].mean():.2f} years")
        print(f"  Median age: {df['age'].median():.2f} years")
        
        if 'gender' in df.columns:
            print(f"\nGender distribution:")
            print(df['gender'].value_counts())
        
        # Show first few examples
        print(f"\nFirst 10 examples:")
        print(df.head(10).to_string(index=False))
        
        # Save to CSV
        os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"\n✓ List saved to: {OUTPUT_CSV}")
        
        # Also save image IDs as text file
        txt_output = OUTPUT_CSV.replace('.csv', '_ids.txt')
        with open(txt_output, 'w') as f:
            for img_id in df['image_id']:
                f.write(f"{img_id}\n")
        print(f"✓ Image IDs saved to: {txt_output}")
        
    else:
        print("\nNo images found matching the criteria.")


if __name__ == "__main__":
    main()

