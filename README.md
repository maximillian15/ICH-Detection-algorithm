# CranioScan: A CNN-Transformer Model for Intracranial Hemorrhage Detection

CranioScan is a deep learning system designed to automatically detect six types of intracranial hemorrhage (ICH) from CT imaging.
It uses a hybrid architecture combining ResNet50 (CNN feature extractor) with a Transformer encoder, enabling both local and global feature understanding.

---

## Project Overview

Bleeding inside the skull is a crucial and potentially lethal neurological event known as an intracranial hemorrhage (ICH).

Intracranial hemorrhage (ICH) is a life-threatening neurological emergency.Diagnosis must be **immediate**, but CT interpretation requires expertise and time.

**CranioScan aims to:**
1. Improve detection speed  
2. Assist radiologists with AI-powered classification  
3. Explore modern hybrid deep learning architectures for medical imaging

---

## Dataset

This project uses a collection of non-contrast brain CT scans commonly provided in ICH classification dataset.
Each scan contains axial slices stored in DICOM format.
The scans vary in slice thickness, window settings, and pixel intensity ranges, so normalization and proper preprocessing are essential for consistent model performance.

---

## Data Preprocessing

To prepare the CT images for training, CranioScan applies a standardized preprocessing workflow:

### 1. DICOM Loading

All scans are read directly from DICOM files using pydicom.

Pixel intensities are converted to standard Hounsfield Units (HU) using Rescale Slope & Intercept metadata.
This ensures the images reflect true CT density values.

### 2. Image Resizing

Each slice is resized to 224 × 224 pixels to match the ResNet50 input size.

### 3. Normalization

Pixel values are scaled to a 0–1 range for stable gradient flow.

Batch normalization layers further ensure feature consistency.

### 4. Data Augmentation

To reduce overfitting and account for natural variation in CT scans, the following augmentations are applied:
1. Random rotations (±10°)
2. Zooming
3. Horizontal/vertical shifts
4. Brightness adjustments

---

## Installation

Clone the repo 

```bash
git clone https://github.com/maximillian15/ICH-Detection-algorithm
cd ICH-Detection-algorithm
```

Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies

```bash
pip install tensorflow pydicom scikit-learn numpy
```

The App expects a trained model called best_model.keras. 

Create the model/ folder if it doesn't exist and copy the file there:

```bash
mkdir -p model
```

Run the Flusk App:

```bash
Python App.py
```

