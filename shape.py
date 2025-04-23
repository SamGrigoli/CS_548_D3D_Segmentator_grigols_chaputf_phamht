import nibabel as nib

nii = nib.load("series_1_1_2_276_0_7230010_3_1_3_4087122745_11320_170676948.nii.gz")
print("Shape:", nii.shape)
print("Voxel dimensions (pixdim):", nii.header.get_zooms())
