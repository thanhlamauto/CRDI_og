# CRDI Kaggle Pipeline

This document explains how to run the complete CRDI pipeline on Kaggle to train on 10 baby images, generate 100 synthetic images, and compute FID against a reference dataset.

## Prerequisites

Before running the pipeline, make sure you have:

1. **FFHQ Dataset** - Images in `/kaggle/working/ffhq/Part1/`
2. **Aging Labels CSV** - Upload as a Kaggle dataset named "aging-labels"
3. **DDPM Checkpoint** - Download the pre-trained FFHQ model

## Setup on Kaggle

### Step 1: Clone the Repository

```bash
!git clone https://github.com/thanhlamauto/CRDI_og.git
%cd CRDI_og
```

### Step 2: Install Dependencies

```bash
!pip install -r requirements.txt
%cd guided_diffusion
!pip install -e .
%cd ..
```

### Step 3: Download Pre-trained Model

```bash
# Create checkpoints directory
!mkdir -p checkpoints/ddpm

# Download FFHQ DDPM checkpoint (256x256)
!wget -O checkpoints/ddpm/ffhq.pt https://openaipublic.blob.core.windows.net/diffusion/jul-2021/256x256_diffusion_uncond.pt
```

### Step 4: Select Children Images (Under 3 Years)

```bash
# Run the selection script to filter children under 3 years old
!python select_children_under3.py
```

This will create `/kaggle/working/children_under3/` with:
- Filtered children images (age group 0-2)
- Metadata CSV with age and gender information
- Image IDs list

### Step 5: Run the Complete Pipeline

```bash
# Make the script executable
!chmod +x main.sh

# Run the pipeline
!bash main.sh
```

## What the Pipeline Does

The `main.sh` script runs three steps:

### Step 1: Compute FID Reference Statistics
- Reads images from `/kaggle/working/children_under3/`
- Computes InceptionV3 activation statistics (mu and sigma)
- Saves to `/kaggle/working/children_under3_stats.npz`

### Step 2: Training
- Trains on 10 baby images from `/kaggle/working/CRDI_og/datasets/babies_target/`
- Uses CRDI few-shot learning approach
- Parameters:
  - Epochs: 50
  - Learning rate: 0.05
  - Timesteps: 5-20
  - Number of gradients: 15
- Saves model to `checkpoints/model_babies.pth`

### Step 3: Generation & Evaluation
- Generates 100 synthetic baby images
- Computes FID score against the children_under3 reference dataset
- Computes Intra-LPIPS for diversity measurement

## Expected Output

```
=========================================
Step 1: Compute FID statistics for reference dataset
=========================================
Found X images in /kaggle/working/children_under3
Computing activations: 100%
✓ Statistics saved to: /kaggle/working/children_under3_stats.npz

=========================================
Step 2: Training on 10 baby images
=========================================
Training Progress: ...
✓ Model saved to checkpoints/model_babies.pth

=========================================
Step 3: Generating 100 images and computing FID
=========================================
Generating samples: 100%
FID reference path: /kaggle/working/children_under3_stats.npz
FID: XX.XX
Intra-LPIPS: X.XXXX

=========================================
Pipeline completed successfully!
=========================================
```

## Output Files

After running the pipeline:

1. **`/kaggle/working/children_under3/`** - Reference dataset (children under 3)
2. **`/kaggle/working/children_under3_stats.npz`** - FID statistics 
3. **`checkpoints/model_babies.pth`** - Trained CRDI model
4. **`arr.npy`** - Generated 100 synthetic images (numpy array)

## Customization

### Change Training Parameters

Edit `main.sh` to modify:
- `--epochs`: Number of training epochs
- `--learning_rate`: Learning rate for gradient optimization
- `--t_start`, `--t_end`: Diffusion timestep range
- `--num_gradient`: Number of gradient vectors to learn

### Change Generation Count

Modify `--num_evaluate` in Step 3:
```bash
--num_evaluate 200  # Generate 200 images instead of 100
```

### Change Reference Dataset

To use a different reference dataset:
1. Update `--image_dir` in Step 1
2. Update `--fid_reference_path` in Step 3

## Troubleshooting

### Issue: CUDA out of memory
**Solution**: Reduce `--batch_size` in the training or evaluation commands.

### Issue: children_under3 directory not found
**Solution**: Make sure you run `select_children_under3.py` first and that the aging-labels dataset is properly added to your Kaggle notebook.

### Issue: DDPM checkpoint not found
**Solution**: Verify the checkpoint was downloaded correctly to `checkpoints/ddpm/ffhq.pt`.

### Issue: Import errors
**Solution**: Make sure you installed the guided_diffusion package:
```bash
%cd guided_diffusion
!pip install -e .
%cd ..
```

## Complete Kaggle Notebook Example

Here's a complete notebook setup:

```python
# Cell 1: Setup
!git clone https://github.com/thanhlamauto/CRDI_og.git
%cd CRDI_og
!pip install -r requirements.txt -q
%cd guided_diffusion && !pip install -e . -q && %cd ..

# Cell 2: Download model
!mkdir -p checkpoints/ddpm
!wget -q -O checkpoints/ddpm/ffhq.pt https://openaipublic.blob.core.windows.net/diffusion/jul-2021/256x256_diffusion_uncond.pt
print("✓ Model downloaded")

# Cell 3: Select children images
!python select_children_under3.py

# Cell 4: Run pipeline
!chmod +x main.sh
!bash main.sh

# Cell 5: Visualize results
import numpy as np
import matplotlib.pyplot as plt

# Load generated images
arr = np.load('arr.npy')
print(f"Generated {len(arr)} images")

# Display sample
fig, axes = plt.subplots(2, 5, figsize=(15, 6))
for i, ax in enumerate(axes.flat):
    if i < len(arr):
        img = arr[i].transpose(1, 2, 0)
        img = (img + 1) / 2  # Denormalize from [-1, 1] to [0, 1]
        ax.imshow(img)
        ax.axis('off')
plt.tight_layout()
plt.show()
```

## Citation

If you use this code, please cite the original CRDI paper.

## Support

For issues or questions:
- GitHub Issues: https://github.com/thanhlamauto/CRDI_og/issues
- Check the logs for detailed error messages

