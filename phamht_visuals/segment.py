'''import nibabel as nib
import numpy as np
from sklearn.cluster import KMeans
from scipy import ndimage

def segment_t1(t1_path, mask_path=None, n_clusters=3):
    # Load T1 image and optional mask
    t1_img = nib.load(t1_path)
    t1_data = t1_img.get_fdata()
    
    # If no mask is provided, create a simple intensity-based mask
    if mask_path:
        mask = nib.load(mask_path).get_fdata() > 0
    else:
        mask = t1_data > np.percentile(t1_data, 10)  # Simple threshold
    
    # Prepare data for clustering (normalize intensities)
    masked_data = t1_data[mask].reshape(-1, 1)
    normalized_data = (masked_data - np.mean(masked_data)) / np.std(masked_data)
    
    # K-means clustering (GM=1, WM=2, CSF=0)
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(normalized_data)
    labels = kmeans.labels_
    
    # Assign clusters to tissues (reorder based on intensity)
    cluster_means = [np.mean(masked_data[labels == i]) for i in range(n_clusters)]
    sorted_clusters = np.argsort(cluster_means)  # CSF (darkest) -> GM -> WM (brightest)
    
    # Create segmentation map
    seg_data = np.zeros_like(t1_data)
    seg_data[mask] = sorted_clusters[labels]  # 0=CSF, 1=GM, 2=WM
    
    # Save results
    seg_img = nib.Nifti1Image(seg_data, t1_img.affine)
    nib.save(seg_img, "segmentation.nii.gz")
    print("Segmentation saved to segmentation.nii.gz")

# Example usage
segment_t1("C:/Code_class/CS_548_D3D_Segmentator_grigols_chaputf_phamht-1/sample_data/shared_data/shared_data/data_mprage/sub-02/anat/sub-02_T1w_defaced.nii.gz", mask_path="C:/Code_class/CS_548_D3D_Segmentator_grigols_chaputf_phamht-1/sample_data/shared_data/shared_data/data_mprage/derivatives/sub-02/masks/sub-02_brain_mask.nii.gz")'''
'''import nibabel as nib
import matplotlib.pyplot as plt

seg = nib.load("segmentation.nii.gz").get_fdata()
plt.imshow(seg[:, :, seg.shape[2]//2], cmap="jet")  # Mid-slice
plt.colorbar(label="0=CSF, 1=GM, 2=WM")
plt.savefig("segmentation_check.png")'''

import os
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np

# 1. Define correct paths (adjust these to match your actual paths)
base_dir = "c:/Code_class/CS_548_D3D_Segmentator_grigols_chaputf_phamht-1/sample_data/shared_data/shared_data/data_mprage"
input_files = {
    "t1": os.path.join(base_dir, "sub-02/anat/sub-02_T1w_defaced.nii.gz"),
    "truth": os.path.join(base_dir, "derivatives/sub-02/ground_truth/sub-02_gm_v06.nii.gz"),
    "seg": "segmentation.nii.gz"  # Output from previous step
}

# 2. Verify all files exist
missing_files = [name for name, path in input_files.items() if not os.path.exists(path)]
if missing_files:
    print("ERROR: Missing files:")
    for name in missing_files:
        print(f"- {name}: {input_files[name]}")
    print("\nCurrent directory contents:", os.listdir('.'))
    exit()

# 3. Load verified files
t1 = nib.load(input_files["t1"]).get_fdata()
truth = nib.load(input_files["truth"]).get_fdata()
seg = nib.load(input_files["seg"]).get_fdata()

# 4. Visualization (same as before)
slice_idx = truth.shape[2] // 2
plt.figure(figsize=(15, 5))

plt.subplot(131)
plt.imshow(t1[:,:,slice_idx], cmap='gray')
plt.title("Original T1")

plt.subplot(132)
plt.imshow(seg[:,:,slice_idx] == 2, cmap='Blues')
plt.title("Your Segmentation (GM)")

plt.subplot(133)
plt.imshow(truth[:,:,slice_idx], cmap='Reds')
plt.title("Ground Truth")

plt.tight_layout()
plt.savefig("segmentation_vs_truth.png")
print("Successfully created comparison plot")