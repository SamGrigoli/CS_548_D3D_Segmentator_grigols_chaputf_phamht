# Segmentator – CS 548 Final Project

[![DOI](https://zenodo.org/badge/59303623.svg)](https://zenodo.org/badge/latestdoi/59303623)

<img src="visuals/logo.png" width=420 align="right" />

This is a **forked version** of the original Segmentator repository, created as part of a **CS 548 class project** at **SUNY Polytechnic Institute**.

---

## Project Team
- Rosaline Pham
- Sam Grigoli 
- Forest Chaput
---

## About This Fork
This fork modifies the original Segmentator package to support additional datasets (including 1.5T and 3T MRIs) and provides updated scripts for preprocessing and easier dataset handling.

**Key Modifications:**
- Added convert.py to resample and standardize different MRI datasets for compatibility with Segmentator.
- Added requirements_update.txt to help with environment setup and package installation for modern Python versions.
- Added pham_visuals/segment.py to generate .png visualizations from NIfTI files (T1, segmentation, and ground truth comparisons).
- Added pham_visuals/extract_data.py as a workaround script to manually calculate Dice and AVHD values; note that AVHD results may not be perfectly precise compared to the original FSL-based calculations.
- Provided clearer instructions for running Segmentator with custom datasets.
- Updated installation and troubleshooting guidelines for better compatibility with updated Python environments.
- Included new dataset sources and detailed processing steps for handling diverse MRI scans.
---

## Dataset Information

### Datasets Used:
- **7T MRI:** Original dataset from Segmentator project: [https://doi.org/10.5281/zenodo.1117858](https://doi.org/10.5281/zenodo.1117858)
- **3T MRI:** Custom clinical scans converted from DICOM format can be found at(only SUNYIT have access): [https://drive.google.com/file/d/134v9LlZ_-6xa1o0kUPd3DjN95rFsheB4/view?usp=sharing](https://drive.google.com/file/d/134v9LlZ_-6xa1o0kUPd3DjN95rFsheB4/view?usp=sharing) 
- **1.5T MRI:** Public Kaggle dataset: [Brain Cancer MRI Dataset](https://www.kaggle.com/datasets/unidatapro/brain-cancer-dataset)

### How to Acquire 1.5T Dataset:
1. Visit the Kaggle page: [Brain Cancer MRI Dataset](https://www.kaggle.com/datasets/unidatapro/brain-cancer-dataset)
2. Download and extract the dataset to a desired directory on your system.

### How to Acquire 3T Dataset:
1. Access the database through provided DOI [https://doi.org/10.48550/arXiv.2302.09200] (https://doi.org/10.48550/arXiv.2302.09200)
2. Download the dataset containing MRI scans in DICOM (.dcm) format.
3. Convert the DICOM files to NIfTI (.nii.gz) format using dcm2niix: 
```
Command
dcm2niix -z y -o output_folder_path input_dicom_folder
```
4. Use the generated .nii.gz files for segmentation and evaluation experiments.

----
## Installation & Setup

This project is compatible with **Python 3.6**.

### Core Dependencies
| Package                                        | Tested Version |
|------------------------------------------------|----------------|
| [matplotlib](http://matplotlib.org/)           | 3.1.1          |
| [NumPy](http://www.numpy.org/)                 | 1.17.2         |
| [NiBabel](http://nipy.org/nibabel/)            | 2.5.1          |
| [SciPy](http://scipy.org/)                     | 1.3.1          |
| [Compoda](https://github.com/ofgulban/compoda) | 0.3.5          |

---

### Quick Start Instructions

**1. Download the Repository:**
- Clone or download [this forked version](https://github.com/YOURUSERNAME/segmentator) and unzip it.
- Run miniconda as administrator

- Create python environment (miniconda) using the following command:
```
conda create -n Segementator python=3.6
```
- Activate python environment using the following command:
```
conda activate Segmentator
```

**2. Install Requirements:**
```bash
cd /path/to/segmentator
pip install -r requirements.txt
```
If you encounter dependency issues, use the updated file:
```bash
pip install -r requirements_update.txt
```

**3. Install the Package:**
```bash
python setup.py install
```

---

### How to Run `convert.py` (Preprocessing)

**Convert and standardize your MRI data:**
```bash
cd /path/to/segmentator
python convert.py
```
This will resample and save NIfTI files into `sample_data/images/nifti_output/`.

---

### How to Run Segmentator Tool

**Navigate to your output directory:**
```bash
cd sample_data/images/nifti_output
```

**Run Segmentator on a selected `.nii.gz` file:**
```bash
segmentator "your_selected_file.nii.gz"
```

Or check help options:
```bash
segmentator --help
```

---

## Citation
- Paper: [PLoS ONE Publication](https://doi.org/10.1371/journal.pone.0198335)
- Software: [Zenodo DOI](https://zenodo.org/badge/latestdoi/59303623)
- Dataset for resampling: [citation: Hugo J. Kuijf; Edwin Bennink; Koen L. Vincken; Nick Weaver; Geert Jan Biessels; Max A. Viergever,"MR Brain Segmentation Challenge 2018 Data", 2024 DataverseNL, https://doi.org/10.34894/E0U32Q, V1] 
(citation: Hugo J. Kuijf; Edwin Bennink; Koen L. Vincken; Nick Weaver; Geert Jan Biessels; Max A. Viergever,"MR Brain Segmentation Challenge 2018 Data", 2024 DataverseNL, https://doi.org/10.34894/E0U32Q, V1)
---

## Resampler instructions

- review current configs found at top of resample_stretch.py and isotropic_resample.py
- run script as standalone:

```
resample_stretch.py
```
OR

```
isotropic_resample.py
```

## Support
Please use [GitHub Issues](https://github.com/ofgulban/segmentator/issues) for questions or bug reports.

---

## License
This project is licensed under [BSD-3-Clause License](https://opensource.org/licenses/BSD-3-Clause).

---

## References
This application is based on:

* Kniss, J., Kindlmann, G., & Hansen, C. D. (2005). Multidimensional transfer functions for volume rendering. *Visualization Handbook*, 189–209. [doi](http://doi.org/10.1016/B978-012387582-2/50011-3)

---

## Acknowledgements
- Original development by [Omer Faruk Gulban](https://github.com/ofgulban) and [Marian Schneider](https://github.com/MSchnei).
- This fork is modified for educational use under SUNY Polytechnic's CS 548 course.
