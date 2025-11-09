# How to Use on Kaggle

This guide explains how to select face images of children under 3 years old from the FFHQ dataset on Kaggle.

## Quick Start

### 1. Clone the Repository on Kaggle

In a Kaggle notebook code cell, run:

```bash
!git clone https://github.com/thanhlamauto/CRDI_og.git
!cd CRDI_og
```

### 2. Add the Aging Labels Dataset

The script uses the `ffhq_aging_labels.csv` file which contains age group and gender information:

**Add Dataset to Kaggle Notebook**
1. Go to Kaggle and create a new dataset named "aging-labels"
2. Upload the `ffhq_aging_labels.csv` file
3. Add the dataset to your notebook (use "Add Data" → select your dataset)
4. The script expects the file at: `/kaggle/input/aging-labels/ffhq_aging_labels.csv`

**Note**: The script filters for age group "0-2" which represents children under 3 years old

### 3. Ensure Your Images are in the Correct Location

Make sure your FFHQ images are located at:
```
/kaggle/working/ffhq/Part1/
```

The images should be named as: `00000.png`, `00001.png`, etc.

### 4. Run the Selection Script

```bash
!cd CRDI_og && python select_children_under3.py
```

## Output

The script will create:

1. **Output directory**: `/kaggle/working/children_under3/`
2. **Metadata CSV**: `/kaggle/working/children_under3/children_metadata.csv`
   - Contains: image_id, image_number, filename, age_group, age_group_confidence, gender, gender_confidence
3. **Image IDs list**: `/kaggle/working/children_under3/children_ids.txt`
   - Simple text file with one image ID per line
4. **Copied images**: All selected children images (*.png files) from age group "0-2"

## Customization

To change the age threshold or paths, edit the configuration section in `select_children_under3.py`:

```python
# Configuration
CSV_PATH = "/kaggle/input/aging-labels/ffhq_aging_labels.csv"  # Path to CSV file
SOURCE_DIR = "/kaggle/working/ffhq/Part1"  # Source directory with images
OUTPUT_DIR = "/kaggle/working/children_under3"  # Output directory
AGE_GROUP = "0-2"  # Age group for children under 3 years (0-2 years)
```

## Example Kaggle Notebook

Here's a complete example for use in Kaggle:

```python
# Cell 1: Clone repository
!git clone https://github.com/thanhlamauto/CRDI_og.git
%cd CRDI_og

# Cell 2: Verify CSV file exists
import os
csv_path = "/kaggle/input/aging-labels/ffhq_aging_labels.csv"
if os.path.exists(csv_path):
    print(f"✓ CSV file found: {csv_path}")
else:
    print(f"✗ CSV file not found. Please add 'aging-labels' dataset to your notebook.")

# Cell 3: Run the selection script
!python select_children_under3.py

# Cell 4: Check the results
import pandas as pd

df = pd.read_csv('/kaggle/working/children_under3/children_metadata.csv')
print(f"Total children images found: {len(df)}")
print(f"\nAge group: {df['age_group'].unique()}")
print(f"\nGender distribution:")
print(df['gender'].value_counts())
print(f"\nAverage age group confidence: {df['age_group_confidence'].astype(float).mean():.4f}")

# Display first few rows
df.head(10)

# Cell 5: Preview some images (optional)
import matplotlib.pyplot as plt
from PIL import Image
import os

fig, axes = plt.subplots(2, 4, figsize=(16, 8))
axes = axes.flatten()

for idx, (_, row) in enumerate(df.sample(n=8).iterrows()):
    img_path = f"/kaggle/working/children_under3/{row['filename']}"
    if os.path.exists(img_path):
        img = Image.open(img_path)
        axes[idx].imshow(img)
        axes[idx].set_title(f"Age: {row['age']:.2f} years")
    axes[idx].axis('off')

plt.tight_layout()
plt.show()
```

## Alternative: Using the Jupyter Notebook

You can also use the interactive Jupyter notebook:

```bash
# Open the notebook in Kaggle
!jupyter notebook select_ffhq_children.ipynb
```

Or simply upload `select_ffhq_children.ipynb` to your Kaggle notebook interface.

## Troubleshooting

### Issue: CSV file not found
**Solution**: Make sure you've added the "aging-labels" dataset to your Kaggle notebook inputs. The file should be at `/kaggle/input/aging-labels/ffhq_aging_labels.csv`. If your dataset has a different name, update the `CSV_PATH` variable in the script.

### Issue: Source directory not found
**Solution**: Verify that your images are located at `/kaggle/working/ffhq/Part1/` or update the `SOURCE_DIR` variable.

### Issue: Out of memory
**Solution**: The script processes images one at a time, so memory shouldn't be an issue. If it occurs, make sure you're not loading all images into memory at once.

## Files in This Repository

- **`select_children_under3.py`**: Main standalone script (recommended for Kaggle)
- **`select_ffhq_children.ipynb`**: Interactive Jupyter notebook
- **`scripts/select_children_images.py`**: Alternative implementation with more features
- **`scripts/list_children_images.py`**: Script that only generates lists without copying files

## Support

For issues or questions, please open an issue on the GitHub repository:
https://github.com/thanhlamauto/CRDI_og/issues

