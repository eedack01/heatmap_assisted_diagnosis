import torch
import torchvision.transforms as tf
from tqdm import tqdm
import glob
from PIL import Image

def compute_stats(file_paths, verbose=True):
    """Compute mean and std of a grayscale image dataset.
    
    Args:
        file_paths: List of image paths
        verbose: Whether to show progress bar
    
    Returns:
        (mean, std) as float32 torch tensors
    """
    # Initialize with double precision for numerical stability
    sum_ = torch.tensor(0.0, dtype=torch.float64)
    sum_sq = torch.tensor(0.0, dtype=torch.float64)
    num_pixels = 0
    to_tensor = tf.ToTensor()
    
    # Use tqdm only if verbose
    iterable = tqdm(file_paths, desc="Calculating mean/std") if verbose else file_paths
    
    for img_path in iterable:
        try:
            with Image.open(img_path) as img:
                img = img.convert('L')  # Convert to grayscale
                tensor = to_tensor(img).to(torch.float64)  # [1,H,W], range [0,1]
                
                num_pixels += tensor.numel()
                sum_ += tensor.sum()
                sum_sq += (tensor ** 2).sum()
        except Exception as e:
            print(f"\nSkipping {img_path} due to error: {str(e)}")
            continue
    
    # Convert results to float32 for typical usage
    mean = sum_ / num_pixels
    std = ((sum_sq / num_pixels) - mean.pow(2)).sqrt()

    if verbose:
        print(f"\nProcessed {len(file_paths)} images ({num_pixels} pixels)")
        print(f"Mean: {mean.item():.6f}")
        print(f"Std: {std.item():.6f}")
    
    return mean, std
# ## NIH STATS
# print('')
vin_images = glob.glob("/storage/homefs/ed22q093/heatmap_assisted_diagnosis/data/train/*")
vin_stats = compute_stats(vin_images)