import os
import pydicom
import numpy as np
import nibabel as nib
from glob import glob

# Path to the root directory containing multiple DICOM folders
root_dicom_dir = r"C:\Users\samgr\OneDrive\Desktop\MRI\CS_548_D3D_Segmentator_grigols_chaputf_phamht\sample_data\Images\ST000001"
output_dir = r"C:\Users\samgr\OneDrive\Desktop\MRI\CS_548_D3D_Segmentator_grigols_chaputf_phamht\sample_data\nifti_output"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

def convert_dicom_to_nifti(dicom_files, output_path):
    if not dicom_files:
        print("No DICOM files found")
        return
    
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
        return
    
    # Extract pixel arrays and stack them
    img_array = np.stack([s.pixel_array for s in slices], axis=0)
    
    # IMPORTANT CHANGE: Force a balanced aspect ratio with identity matrix
    # This ignores the original spacing but creates visually balanced images
    affine = np.eye(4)
    
    # Create NIfTI object with forced aspect ratio
    nifti_img = nib.Nifti1Image(img_array, affine)
    
    # Save as compressed NIfTI (.nii.gz)
    nib.save(nifti_img, output_path)
    print(f"Converted {len(dicom_files)} DICOM files to {output_path}")

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

# Convert each series to a NIfTI file
for i, (series_id, dicom_files) in enumerate(series_dict.items()):
    # Create a safe filename using part of the series ID
    safe_name = str(series_id).replace('.', '_').replace('/', '_').replace('\\', '_')[:50]
    output_file = os.path.join(output_dir, f"series_{i+1}_{safe_name}.nii.gz")
    
    print(f"Converting series {i+1}/{len(series_dict)} with {len(dicom_files)} files...")
    convert_dicom_to_nifti(dicom_files, output_file)

print("Conversion complete!")