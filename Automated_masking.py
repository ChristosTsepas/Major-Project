# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 12:05:33 2023

@author: ctsepas
"""

import os
import nibabel as nib
from dipy.segment.mask import median_otsu
from dipy.io.image import load_nifti
import numpy as np





#function for masking a single volume. From Dipy

def mask_nii(input_path, output_path):
    # Load the NIfTI image
    denoised_data, denoised_affine, denoised_voxel =  load_nifti(input_path, return_voxsize=True)

    # Apply median_otsu masking
    masked_data, mask = median_otsu(denoised_data, vol_idx=range(1, 20), median_radius=4,
                                 numpass=4, autocrop=False, dilate=10)

     # Create NIfTI images with the masked data and the mask
    masked_img = nib.Nifti1Image(masked_data, denoised_affine)
    mask_img = nib.Nifti1Image(mask.astype(np.float32), denoised_affine)

    # Save the masked image and the mask to separate files on the specified path
    nib.save(masked_img, output_path.replace('.nii', '.nii'))
    nib.save(mask_img, output_path.replace('.nii', '_mask.nii'))
    #iterate through files and get all datasets




def mask_all_nii_files(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all .nii files in the input folder
    nii_files = [f for f in os.listdir(input_folder) if f.endswith('.nii')]

    # Mask each .nii file and save it to the output folder
    for nii_file in nii_files:
        input_path = os.path.join(input_folder, nii_file)
        output_path = os.path.join(output_folder, nii_file)
        mask_nii(input_path, output_path)






if __name__ == "__main__":
    # Set your input and output folder paths
    input_folder = r"H:\Rest of data\Denoising_DTI_DTIADS"
    output_folder = r"H:\Rest of data\Masked_DTIADS"

    # Mask all .nii files in the input folder and save to the output folder
    mask_all_nii_files(input_folder, output_folder)