import os
import nibabel as nib
import numpy as np
from scipy.ndimage import zoom

#config

input_dir = 'input_dir'        
output_dir = 'output_dir'      # Where processed files will be saved
target_shape = (128, 128, 128) # Desired output shape
target_spacing = 1.4           # Desired voxel spacing in mm (isotropic)



def resample_isotropic(data, affine, target_spacing):
    # Current voxel dimensions (mm)
    current_spacing = np.abs(affine.diagonal()[:3])

    # Calculate zoom factors
    zoom_factors = current_spacing / target_spacing

    # Resample the data
    resampled_data = zoom(data, zoom_factors, order=1)

    # Update affine matrix to reflect new spacing
    new_affine = affine.copy()
    for i in range(3):
        new_affine[i, i] = np.sign(affine[i, i]) * target_spacing

    return resampled_data, new_affine

def pad_or_crop(data, target_shape):
    current_shape = data.shape
    new_data = np.zeros(target_shape, dtype=data.dtype)

    # Calculate cropping or padding indices
    crop_start = [(curr - target) // 2 if curr > target else 0 for curr, target in zip(current_shape, target_shape)]
    crop_end = [crop_start[i] + target_shape[i] if current_shape[i] > target_shape[i] else current_shape[i] for i in range(3)]

    # Crop if needed
    cropped = data[
        crop_start[0]:crop_end[0],
        crop_start[1]:crop_end[1],
        crop_start[2]:crop_end[2]
    ]

    # Center the cropped data into new_data
    insert_start = [(target_shape[i] - cropped.shape[i]) // 2 for i in range(3)]
    insert_end = [insert_start[i] + cropped.shape[i] for i in range(3)]

    new_data[
        insert_start[0]:insert_end[0],
        insert_start[1]:insert_end[1],
        insert_start[2]:insert_end[2]
    ] = cropped

    return new_data

def process_nii(filepath, output_dir, target_shape, target_spacing):
    img = nib.load(filepath)
    data = img.get_fdata()
    affine = img.affine

    if len(data.shape) != 3:
        print(f"Skipping {filepath} — not a 3D image.")
        return

    # Step 1: Resample to isotropic voxels
    resampled_data, new_affine = resample_isotropic(data, affine, target_spacing)

    # Step 2: Pad or crop to target shape
    final_data = pad_or_crop(resampled_data, target_shape)

    # Step 3: Save new NIfTI
    resampled_img = nib.Nifti1Image(final_data, new_affine, img.header)
    output_path = os.path.join(output_dir, os.path.basename(filepath))
    nib.save(resampled_img, output_path)
    print(f"Saved: {output_path}")

def batch_process(input_dir, output_dir, target_shape, target_spacing):
    os.makedirs(output_dir, exist_ok=True)

    for fname in os.listdir(input_dir):
        if fname.endswith('.nii') or fname.endswith('.nii.gz'):
            fpath = os.path.join(input_dir, fname)
            process_nii(fpath, output_dir, target_shape, target_spacing)

# ======================= RUN ========================
if __name__ == '__main__':
    batch_process(input_dir, output_dir, target_shape, target_spacing)
