#!/bin/bash
# CRDI Pipeline: Train on 10 baby images, generate 100 images, compute FID
# Uses single GPU (CUDA_VISIBLE_DEVICES=0) and batch_size=1 to avoid distributed training issues

set -e  # Exit on error

echo "========================================="
echo "Step 1: Compute FID statistics for reference dataset"
echo "========================================="
python scripts/compute_fid_stats.py \
	--image_dir /kaggle/working/children_under3 \
	--output /kaggle/working/children_under3_stats.npz \
	--batch_size 50 \
	--image_size 256

echo ""
echo "========================================="
echo "Step 2: Training on 10 baby images"
echo "========================================="
CUDA_VISIBLE_DEVICES=0 python scripts/fs_gradient_train.py \
	--csv_file datasets/babies_target/babies.csv \
	--t_start 5 --t_end 20 --num_gradient 2 \
	--random_q_noise True --epochs 50 --learning_rate 0.05 \
	--category babies --print_config True \
	--batch_size 1 --num_samples 10

echo ""
echo "========================================="
echo "Step 3: Generating 100 images and computing FID"
echo "========================================="
CUDA_VISIBLE_DEVICES=0 python scripts/fs_gradient_evaluate.py \
	--csv_file datasets/babies_target/babies.csv \
	--t_start 5 --t_end 20 --num_gradient 2 \
	--anneal_ptb True --anneal_scale 0.05 \
	--use_x_0 True --random_q_noise True --print_config True \
	--category babies --num_evaluate 100 --lpips_cluster_size 50 \
	--experiment_gradient_path checkpoints/model_babies.pth \
	--fid_reference_path /kaggle/working/children_under3_stats.npz \
	--batch_size 1

echo ""
echo "========================================="
echo "Pipeline completed successfully!"
echo "========================================="
echo "Training: 10 images from babies_target"
echo "Generated: 100 synthetic images"
echo "FID computed against: /kaggle/working/children_under3"
echo "========================================="
