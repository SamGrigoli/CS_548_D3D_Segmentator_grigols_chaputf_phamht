import SimpleITK as sitk
import numpy as np
import os


def compute_dice(pred, gt):
    intersection = np.logical_and(pred, gt).sum()
    dice = (2. * intersection) / (pred.sum() + gt.sum())
    return dice


def compute_surface_distance(pred, gt):
    pred_surface = sitk.LabelContour(pred)
    gt_surface = sitk.LabelContour(gt)

    hausdorff_filter = sitk.HausdorffDistanceImageFilter()
    hausdorff_filter.Execute(pred_surface, gt_surface)

    avg_surface_distance = hausdorff_filter.GetAverageHausdorffDistance()
    return avg_surface_distance


def main():
    print("Segmentation Evaluation Tool")
    print("------------------------------")

    gt_path = input("Enter path to Ground Truth NIfTI file (.nii or .nii.gz): ").strip()
    pred_path = input("Enter path to Predicted Segmentation NIfTI file (.nii or .nii.gz): ").strip()

    if not os.path.exists(gt_path):
        print(f"Error: Ground truth file not found at {gt_path}")
        return

    if not os.path.exists(pred_path):
        print(f"Error: Predicted segmentation file not found at {pred_path}")
        return

    gt_img = sitk.ReadImage(gt_path)
    pred_img = sitk.ReadImage(pred_path)

    gt_arr = sitk.GetArrayFromImage(gt_img) > 0
    pred_arr = sitk.GetArrayFromImage(pred_img) > 0

    dice_score = compute_dice(pred_arr, gt_arr)

    # Make sure inputs to surface distance computation are binary images
    gt_bin = sitk.Cast(gt_img > 0, sitk.sitkUInt8)
    pred_bin = sitk.Cast(pred_img > 0, sitk.sitkUInt8)

    avg_surface_dist = compute_surface_distance(pred_bin, gt_bin)

    print("\nEvaluation Results:")
    print(f"DICE Coefficient: {dice_score:.4f}")
    print(f"Average Surface Distance (AVHD): {avg_surface_dist:.4f} mm")


if __name__ == '__main__':
    main()
