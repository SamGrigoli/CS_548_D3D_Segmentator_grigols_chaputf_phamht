# Segmentation and Evaluation Tools
Author: Rosaline Pham

This folder contains two main Python scripts for basic brain MRI segmentation and evaluation:

** segment.py
A simple interactive tool for visualizing, segmenting, and comparing NIfTI (.nii or .nii.gz) brain MRI files. Additionally, segment.py provides visual comparisons by automatically saving images that display the original MRI scan, the auto-segmentation, and (if provided) the ground truth.

*** Notes ***
Segmentations are performed using simple unsupervised KMeans clustering based on voxel intensity (3 classes: CSF, GM, WM).

run this following command to use: python path\to\segment.py

** extract_data.py
A Python-based tool designed to quantitatively evaluate segmentation results against ground truth labels using metrics like Dice Coefficient and Average Surface Distance (AVHD).

run this following command to use: python path\to\extract_data.py

***Note***
In the original paper, the authors used MATLAB and FSL for segmentation and evaluation. This Python implementation serves as a convenient workaround but may produce mismatched or less precise results compared to the original methods.

Core Dependencies
Python 3.8+ 

Package	Tested Version
matplotlib	3.1.1
NumPy	1.22.0
NiBabel	2.5.1
SciPy	1.3.1
Compoda	0.3.5
SimpleITK	- (latest)
scikit-learn	- (latest)
````````
pip install SimpleITK numpy nibabel matplotlib scikit-learn
``````````````````````
*** folder structure***
/your_project/
│
├── segment.py
├── extract_data.py
├── examples/
│   ├── t1_example.png
│   ├── segmentation_example.png
│   ├── groundtruth_example.png
│   ├── t1_single_example.png
│   ├── segmentation_single_example.png
│
└── README.md