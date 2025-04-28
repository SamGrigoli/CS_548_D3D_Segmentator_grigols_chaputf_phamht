'''
Rosaline Pham
Description: This is an interactive simple Python for visualizing and segmenting NIfTI brain scans.
It supports both multi-file comparisons (T1 + segmentation + ground truth) and single-file segmentation using KMeans clustering.
Output images are saved automatically with unique filenames, and errors are handled for user inputs.
'''
# All imports go here
import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from sklearn.cluster import MiniBatchKMeans

# unique filename
def get_unique_filename(base_name, output_dir=None):
    if output_dir:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        path = os.path.join(output_dir, base_name)
    else:
        path = base_name

    count = 1
    name, ext = os.path.splitext(path)
    new_name = f"{name}_{count}{ext}"
    while os.path.exists(new_name):
        count += 1
        new_name = f"{name}_{count}{ext}"
    return new_name

while True:
    # menu
    print("\n--- What do you want to do? ---")
    print("1. Compare a T1 + Auto-Segmentation + Ground Truth (Case 1)")
    print("2. Segment a single NIfTI file (Case 2)")
    print("Type 'exit' to quit.")

    choice = input("Enter 1, 2, or 'exit': ").strip()

    if choice.lower() == 'exit':
        print("Exiting program. Goodbye!")
        break

    if choice not in ['1', '2']:
        print("Invalid choice. Please enter 1, 2, or 'exit'.")
        continue

    # prompt save results path
    save_dir = input("\nEnter full path to the directory where you want to save output files (or press Enter to save in current folder): ").strip()
    if not save_dir:
        save_dir = None
    elif not os.path.exists(save_dir):
        print(f"The directory '{save_dir}' does not exist. Creating it...")
        os.makedirs(save_dir)

    # common segmentation function
    def segment_brain(img_data):
        mask = img_data > np.percentile(img_data[img_data > 0], 10)
        masked_data = img_data[mask].reshape(-1, 1)
        normalized_data = (masked_data - np.mean(masked_data)) / np.std(masked_data)

        kmeans = MiniBatchKMeans(n_clusters=3, random_state=0, batch_size=5000).fit(normalized_data)
        labels = kmeans.labels_

        cluster_means = [np.mean(masked_data[labels == i]) for i in range(3)]
        sort_idx = np.argsort(cluster_means)

        new_labels = np.zeros_like(labels)
        for new_label, old_label in enumerate(sort_idx):
            new_labels[labels == old_label] = new_label

        seg_data = np.zeros_like(img_data)
        seg_data[mask] = new_labels
        return seg_data

    # case 1: generate segmentation from original t1 and compare to ground_truth
    if choice == '1':
        print("\nYou selected Case 1: Provide T1 file and Ground Truth. Segmentation will be generated automatically.")

        t1_path = input("Enter full path to the T1 original file (.nii.gz): ").strip()
        truth_path = input("Enter full path to the Ground Truth file (.nii.gz): ").strip()

        input_files = {"T1": t1_path, "Ground Truth": truth_path}
        missing_files = [name for name, path in input_files.items() if not os.path.exists(path)]

        if missing_files:
            print("ERROR: Missing files:")
            for name in missing_files:
                print(f"- {name}: {input_files[name]}")
            continue

        try:
            t1_img = nib.load(t1_path)
            t1_data = t1_img.get_fdata()
            truth = nib.load(truth_path).get_fdata()

            seg_data = segment_brain(t1_data)

            slice_idx = truth.shape[2] // 2
            plt.figure(figsize=(15, 5))

            plt.subplot(131)
            plt.imshow(t1_data[:, :, slice_idx], cmap='gray')
            plt.title("Original T1")

            plt.subplot(132)
            plt.imshow(seg_data[:, :, slice_idx] == 1, cmap='Blues')
            plt.title("Generated Segmentation (GM Only)")

            plt.subplot(133)
            plt.imshow(truth[:, :, slice_idx], cmap='Reds')
            plt.title("Ground Truth")

            plt.tight_layout()
            save_filename = get_unique_filename("segmentation_vs_truth.png", output_dir=save_dir)
            plt.savefig(save_filename, dpi=300)
            plt.close()
            print(f"Successfully created comparison plot at '{os.path.abspath(save_filename)}'.")

        except Exception as e:
            print(f"Processing failed: {str(e)}")
            continue

    # case 2: segment a single scan
    elif choice == '2':
        print("\nYou selected Case 2: Provide a single file to segment.")

        file_path = input("Enter full path to the single NIfTI file (.nii.gz): ").strip()

        if not os.path.exists(file_path):
            print(f"ERROR: The provided file does not exist:\n{file_path}")
            continue

        try:
            img = nib.load(file_path)
            data = img.get_fdata()

            seg_data = segment_brain(data)

            slice_idx = data.shape[2] // 2
            plt.figure(figsize=(12, 6))

            plt.subplot(121)
            plt.imshow(data[:, :, slice_idx], cmap='gray')
            plt.title("Original Scan")

            plt.subplot(122)
            plt.imshow(seg_data[:, :, slice_idx] == 1, cmap='Blues')
            plt.title("Segmentation (GM Only)")

            plt.tight_layout()
            save_filename = get_unique_filename("segmentation_result.png", output_dir=save_dir)
            plt.savefig(save_filename, dpi=300)
            plt.close()
            print(f"Success! Results saved to:\n{os.path.abspath(save_filename)}")

        except Exception as e:
            print(f"Processing failed: {str(e)}")
            continue
