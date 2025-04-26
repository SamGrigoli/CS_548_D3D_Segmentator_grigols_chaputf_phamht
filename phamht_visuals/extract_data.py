import os
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# ========================================================
# 1. SAFE PATH HANDLING (Windows/Linux/Mac compatible)
# ========================================================
base_dir = r"c:\Code_class\CS_548_D3D_Segmentator_grigols_chaputf_phamht-1\sample_data\adni_phamht_CS548_converted"
input_file = r"sub1_phamht\adni_phamht_CS548_(3.22)_ADNI3_Study_Huma_20180330093014_3.nii.gz"  # Your filename

# Construct full path safely
input_path = os.path.normpath(os.path.join(base_dir, input_file))

# ========================================================
# 2. VERIFY FILE EXISTS
# ========================================================
if not os.path.exists(input_path):
    print(f"ERROR: File not found at:\n{input_path}")
    print("\nDirectory contents:")
    print(*os.listdir(base_dir), sep='\n')
    exit()

# ========================================================
# 3. LOAD AND PROCESS DATA
# ========================================================
try:
    img = nib.load(input_path)
    data = img.get_fdata()
    
    # Simple segmentation (modify as needed)
    mask = data > np.percentile(data[data > 0], 10)
    kmeans = KMeans(n_clusters=3).fit(data[mask].reshape(-1, 1))
    seg = np.zeros_like(data)
    seg[mask] = kmeans.labels_ + 1  # 1=CSF, 2=GM, 3=WM

    # ========================================================
    # 4. VISUALIZATION
    # ========================================================
    slice_idx = data.shape[2] // 2
    plt.figure(figsize=(12, 6))
    
    plt.subplot(121)
    plt.imshow(data[:, :, slice_idx], cmap='gray')
    plt.title("Original Scan")
    
    plt.subplot(122)
    plt.imshow(seg[:, :, slice_idx], cmap='jet')
    plt.title("Segmentation")
    plt.colorbar(label="1=CSF, 2=GM, 3=WM")
    
    plt.savefig("segmentation_result.png", dpi=300)
    print(f"Success! Results saved to:\n{os.path.abspath('segmentation_result.png')}")
    
except Exception as e:
    print(f"Processing failed: {str(e)}")
    
