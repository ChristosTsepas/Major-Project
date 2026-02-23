# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 14:15:48 2023

@author: ctsepas
"""


import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from time import time
import dipy.io as io
import os
from dipy.core.gradients import gradient_table
from dipy.denoise.localpca import localpca
from dipy.denoise.pca_noise_estimate import pca_noise_estimate
from dipy.io.image import load_nifti
from dipy.denoise.localpca import mppca


######################################## Automated denoising script ######################################
# insert input and output directory. 
# Even if it's the same, the data will be saved as {filename}_denoised.nii
# For further changes (renaming, copy paste etc) go to File_processing.py script
def denoising(input_directory, output_directory):
    for filename in os.listdir(input_directory):
        if filename.endswith('.nii'):
            base_filename = filename.replace(".nii", "")
            image_data, image_affine = load_nifti(os.path.join(input_directory, filename))
            t = time()
            denoised_image, sigma = mppca(image_data, patch_radius=3, return_sigma=True)
            print("Time taken for local PCA ",  -t + time())
            save_denoised = nib.Nifti1Image(denoised_image,
                                     image_affine)
            # saved as {base_filename}_denoised just to be sure.
            # File prefix can be changed using file processing script
            nib.save(save_denoised, os.path.join(output_directory, f"{base_filename}.nii"))
 
if __name__ == "__main__":
    input_directory = r"H:\Testing\batch"
    output_directory = r"H:\Testing\batch\denoising"
    denoising(input_directory, output_directory)

