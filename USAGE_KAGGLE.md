# How to Use on Kaggle

This guide explains how to select face images of children under 3 years old from the FFHQ dataset on Kaggle.

## Quick Start

### 1. Clone the Repository on Kaggle

In a Kaggle notebook code cell, run:

```bash
!git clone https://github.com/thanhlamauto/CRDI_og.git
!cd CRDI_og
```

### 2. Upload the Metadata File

Since `ffhq-dataset-v2.json` is too large for GitHub (>200MB), you need to:

**Option A: Upload as Kaggle Dataset**
1. Go to Kaggle and create a new dataset
2. Upload the `ffhq-dataset-v2.json` file
3. Add the dataset to your notebook

**Option B: Download from FFHQ Source**
```bash
# Download the metadata file from the official FFHQ repository
!wget https://github.com/NVlabs/ffhq-dataset/raw/master/ffhq-dataset-v2.json
```

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
   - Contains: image_id, filename, age, gender
3. **Image IDs list**: `/kaggle/working/children_under3/children_ids.txt`
   - Simple text file with one image ID per line
4. **Copied images**: All selected children images (*.png files)

## Customization

To change the age threshold or paths, edit the configuration section in `select_children_under3.py`:

```python
# Configuration
METADATA_PATH = "ffhq-dataset-v2.json"  # Path to metadata file
SOURCE_DIR = "/kaggle/working/ffhq/Part1"  # Source directory with images
OUTPUT_DIR = "/kaggle/working/children_under3"  # Output directory
AGE_THRESHOLD = 3.0  # Maximum age in years
```

## Example Kaggle Notebook

Here's a complete example for use in Kaggle:

```python
# Cell 1: Clone repository
!git clone https://github.com/thanhlamauto/CRDI_og.git
%cd CRDI_og

# Cell 2: Download metadata (if needed)
# If you haven't uploaded it as a dataset
!wget https://github.com/NVlabs/ffhq-dataset/raw/master/ffhq-dataset-v2.json

# Cell 3: Run the selection script
!python select_children_under3.py

# Cell 4: Check the results
import pandas as pd

df = pd.read_csv('/kaggle/working/children_under3/children_metadata.csv')
print(f"Total children images found: {len(df)}")
print(f"\nAge statistics:")
print(df['age'].describe())
print(f"\nGender distribution:")
print(df['gender'].value_counts())

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

### Issue: Metadata file not found
**Solution**: Make sure the `ffhq-dataset-v2.json` file is in the same directory as the script, or update the `METADATA_PATH` variable.

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

