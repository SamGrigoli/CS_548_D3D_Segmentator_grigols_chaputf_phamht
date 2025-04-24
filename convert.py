import os
import pydicom
import numpy as np
import nibabel as nib
from glob import glob
from nilearn.image import resample_img

script_dir = os.path.dirname(os.path.abspath(__file__))

# Make directory and output for nii.gz files relative
root_dicom_dir = os.path.join(script_dir, "sample_data", "Images", "ST000001")
output_dir = os.path.join(script_dir, "sample_data", "nifti_output")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

CUSTOM_DIMENSIONS = [
    (32, 128, 128)   # Lower resolution but balanced
    
]

def convert_dicom_with_custom_dimensions(dicom_files, output_path, custom_dims_list):
    if not dicom_files:
        print("No DICOM files found")
        return []
        
    # Sort files to ensure correct slice order
    dicom_files.sort()
    
    # Read all slices
    slices = []
    for file in dicom_files:
        try:
            ds = pydicom.dcmread(file)
            slices.append(ds)
        except Exception as e:
            print(f"Error reading {file}: {e}")
            continue
        
    if not slices:
        print("No valid DICOM files found")
        return []
        
    # Extract pixel arrays and stack them
    img_array = np.stack([s.pixel_array for s in slices], axis=0)
    
    # Get original shape
    original_shape = img_array.shape
    print(f"Original image shape: {original_shape}")
    
    # Create initial NIfTI with identity affine
    affine = np.eye(4)
    nifti_img = nib.Nifti1Image(img_array, affine)
    
    # First save the original canonical version
    canonical_img = nib.as_closest_canonical(nifti_img)
    canonical_path = output_path.replace('.nii.gz', '_original_canonical.nii.gz')
    nib.save(canonical_img, canonical_path)
    print(f"Saved original canonical version: {canonical_path}")
    
    # Create all the custom dimension versions
    output_files = [canonical_path]
    
    for i, dims in enumerate(custom_dims_list):
        try:
            # Create a properly scaled affine matrix for the resampled image
            scale_x = original_shape[0] / dims[0] if dims[0] > 0 else 1
            scale_y = original_shape[1] / dims[1] if dims[1] > 0 else 1
            scale_z = original_shape[2] / dims[2] if dims[2] > 0 else 1
            
            target_affine = np.diag([scale_x, scale_y, scale_z, 1])
            
            # Resample to the new dimensions
            custom_img = resample_img(
                nifti_img,
                target_affine=target_affine,
                target_shape=dims,
                interpolation='linear'
            )
            
            # Create a descriptive filename
            custom_path = output_path.replace('.nii.gz', f'_dim_{dims[0]}x{dims[1]}x{dims[2]}.nii.gz')
            nib.save(custom_img, custom_path)
            print(f"Saved version {i+1} with dimensions {dims}: {custom_path}")
            output_files.append(custom_path)
        except Exception as e:
            print(f"Error creating version with dimensions {dims}: {e}")
    
    return output_files

# Recursively find all DICOM series
def find_dicom_series(root_dir):
    # Dictionary to store series: each key is a SeriesInstanceUID, value is list of DICOM files
    series_dict = {}
        
    # Walk through all directories
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Find all DICOM files in this directory
        dicom_files = [os.path.join(dirpath, f) for f in filenames if f.endswith('.dcm')]
                
        # Group files by series
        for file in dicom_files:
            try:
                ds = pydicom.dcmread(file, stop_before_pixels=True)
                # Use SeriesInstanceUID as unique identifier for the series
                series_id = ds.SeriesInstanceUID if hasattr(ds, 'SeriesInstanceUID') else os.path.basename(dirpath)
                                
                if series_id not in series_dict:
                    series_dict[series_id] = []
                                
                series_dict[series_id].append(file)
            except Exception as e:
                print(f"Error reading header of {file}: {e}")
        
    return series_dict
 
# Find all DICOM series
print("Scanning for DICOM series...")
series_dict = find_dicom_series(root_dicom_dir)
print(f"Found {len(series_dict)} DICOM series")

# Convert each series to multiple NIfTI formats with custom dimensions
for i, (series_id, dicom_files) in enumerate(series_dict.items()):
    # Create a safe filename using part of the series ID
    safe_name = str(series_id).replace('.', '_').replace('/', '_').replace('\\', '_')[:50]
    output_file = os.path.join(output_dir, f"series_{i+1}_{safe_name}.nii.gz")
        
    print(f"\nConverting series {i+1}/{len(series_dict)} with {len(dicom_files)} files...")
    try:
        converted_paths = convert_dicom_with_custom_dimensions(dicom_files, output_file, CUSTOM_DIMENSIONS)
        print(f"Successfully created {len(converted_paths)} versions")
    except Exception as e:
        print(f"Error converting series: {e}")

print("\nConversion complete!")
