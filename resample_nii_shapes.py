import os
import nibabel as nib
import numpy as np
from scipy.ndimage import zoom

# ===================== CONFIG ======================

input_dir = 'input_dir'       # Folder with original .nii/.nii.gz files
output_dir = 'output_dir'     # Where resampled files will be saved
target_shape = (128, 128, 128)  # Desired image shape

# ===================================================

def resample_to_shape(data, target_shape):
    # Calculate the zoom factors for each dimension
    zoom_factors = [t / s for t, s in zip(target_shape, data.shape)]
    # Resample the image data with linear interpolation (order=1)
    return zoom(data, zoom_factors, order=1)

def process_nii(filepath, output_dir, target_shape):
    # Load the .nii or .nii.gz file
    img = nib.load(filepath)
    data = img.get_fdata()

    # Skip non-3D images
    if len(data.shape) != 3:
        print(f"Skipping {filepath} — not a 3D image.")
        return

    # Resample the data to the target shape
    resampled_data = resample_to_shape(data, target_shape)
    
    # Create a new NIfTI image with resampled data
    resampled_img = nib.Nifti1Image(resampled_data, img.affine, img.header)

    # Create the output file path and save the resampled image
    output_path = os.path.join(output_dir, os.path.basename(filepath))
    nib.save(resampled_img, output_path)
    print(f"Saved: {output_path}")

def batch_resample(input_dir, output_dir, target_shape):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Loop over all files in the input directory
    for fname in os.listdir(input_dir):
        # Process only .nii and .nii.gz files
        if fname.endswith('.nii') or fname.endswith('.nii.gz'):
            fpath = os.path.join(input_dir, fname)
            process_nii(fpath, output_dir, target_shape)

# ======================= RUN ========================
if __name__ == '__main__':
    batch_resample(input_dir, output_dir, target_shape)