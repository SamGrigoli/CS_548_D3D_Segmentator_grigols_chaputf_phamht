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
