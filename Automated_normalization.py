# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 20:22:54 2023

@author: User
"""

## automated normalization process

import os
import numpy as np
import nibabel as nib
from dipy.io.image import load_nifti
from dipy.segment.mask import applymask
import matplotlib.pyplot as plt
from dipy.segment.mask import median_otsu

# Function to load and normalize images
def load_and_normalize_images(ap_image_path, pa_image_path):
    # Load AP image
    ap_image_data, ap_affine, _ = load_nifti(ap_image_path, return_voxsize=True)
    # Load PA image
    pa_image_data, pa_affine, _ = load_nifti(pa_image_path, return_voxsize=True)
    # Apply masks to images
    #ap_masked_data = applymask(ap_image_data, ap_mask_data)
    #pa_masked_data = applymask(pa_image_data, pa_mask_data)  # Use the same mask for PA
    scaling_factors = []
    # Calculate scaling factors
    scaling_factors = [np.mean(ap_image_data[..., i]) / np.mean(pa_image_data[..., i]) for i in range(ap_image_data.shape[-1])]
    # Calculate mean scaling factor
    mean_scaling_factor = np.mean(scaling_factors)
    print("Mean scaling factor for subject {patient_id}: ", mean_scaling_factor)
    # Apply normalization to PA image
    pa_normalized_data = pa_image_data * mean_scaling_factor
     # Plot scaling factors
    plt.plot(scaling_factors, marker="o", markeredgecolor="red", markerfacecolor="red")
    plt.title("Scaling Factors")
    plt.xlabel("Volume Number")
    plt.ylabel("Scaling Factor")
    plt.show()
    
    return ap_image_data, ap_affine, pa_normalized_data, pa_affine, scaling_factors
    
# Function to iterate through files in a directory
def process_directory(input_dir, output_dir):
    # Iterate through all files in the input directory
    files = os.listdir(input_dir)
    # Process each patient
    for filename in files:
        # Extract patient ID from the filename
        patient_id, direction = os.path.splitext(filename)[0].rsplit('_', 1)
        # Create paths for AP and PA images
        if direction == 'AP' and f'{patient_id}_PA.nii' in files:
            ap_path = os.path.join(input_dir, filename)
            pa_path = os.path.join(input_dir, f'{patient_id}_PA.nii')
            # Print filenames for debugging
            print(f"Processing: {ap_path}, {pa_path}")
            # Load and normalize images
            ap_image_data, ap_affine, pa_normalized_data, pa_affine, scaling_factors = load_and_normalize_images(ap_path, pa_path)
            # Save normalized PA image
            save_normalized_images(ap_image_data, ap_affine, pa_normalized_data, pa_affine, patient_id, output_dir)

# Function to save normalized images
def save_normalized_images(ap_image_data, ap_affine, pa_normalized_data, pa_affine, patient_id, output_dir):
    # Save AP image
    ap_img = nib.Nifti1Image(ap_image_data, ap_affine)
    ap_output_path = os.path.join(output_dir, f"{patient_id}_AP.nii")
    nib.save(ap_img, ap_output_path)

    # Save normalized PA image
    pa_img = nib.Nifti1Image(pa_normalized_data, pa_affine)  # Assuming the affine is the same for both
    pa_output_path = os.path.join(output_dir, f"{patient_id}_PA.nii")
    nib.save(pa_img, pa_output_path)



if __name__ == "__main__":
    # Input and output directories
    input_directory = r"H:\Rest of data\Signal_drift_DTI_DTIADS\data"
    output_directory = r"H:\Rest of data\Normalized_DTI_DTIADS"
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    process_directory(input_directory, output_directory)
