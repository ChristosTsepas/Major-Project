# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 13:49:09 2023

@author: User
"""
import nibabel as nib
import numpy as np
from dipy.align.reslice import reslice
from dipy.io.image import load_nifti, save_nifti
from dipy.segment.mask import median_otsu, crop
import nibabel as nib
import SimpleITK as sitk
import os


# Function to process and crop NIfTI files in a folder
def process_and_crop_T2(input_path, output_path):
    # Create the output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    for filename in os.listdir(input_path):
        if filename.endswith(".nii"):
            file_path = os.path.join(input_path, filename)
            data, affine, coord = load_nifti(file_path, return_coords=True)
            ###  for T2 change here
            mins = [1, 15, 0]
            maxs = [87, 71, 14]
            cropped_data = crop(data, mins, maxs)
            # Create the output file path in the output directory
            output_file_path = os.path.join(output_path, filename.replace("_resampled.nii", ".nii"))
            # Create a NIfTI image with the cropped data
            cropped_nii = nib.Nifti1Image(cropped_data, affine)
            # Save the cropped T2 image to the output file path
            nib.save(cropped_nii, output_file_path)

def check_correct_negative_values(input_path, output_path):        
        for filename in os.listdir(input_path):
            if filename.endswith('.nii'):
                t2_array, affine = load_nifti(os.path.join(input_path, filename))
                basename = filename.replace('.nii', '')
                if np.any(t2_array < 0):
                    print(f"There are negative values in the {basename} volume.")
                    t2_array[t2_array < 0] = 0
                else:
                    print(f"No negative values found in the {basename} volume.")
                     
                output_filename = f"{basename}.nii"
                nii_img = nib.Nifti1Image(t2_array, affine)
                # Save the NIfTI file
                nib.save(nii_img, os.path.join(output_path, output_filename))
                print(f"Modified volume saved to: {os.path.join(output_path, output_filename)}")

if __name__ == "__main__":
    # Set your input directory containing the .nii files
    input_directory = r"H:\Marc_Pastur_pipeline\T2 processing\Resampled and cropped"
    # Set your output directory for saving the cropped .nii files
    output_directory = r"H:\Marc_Pastur_pipeline\T2 processing\Correct for negative values"
    check_correct_negative_values(input_directory, output_directory)
    # Process and crop all .nii files in the input directory
    process_and_crop_T2(input_directory, output_directory)
















'''
##################################         Reslice diffusion dataset    #####################################################



t2 = r''


t2_data, t2_affine, t2_voxel_size = load_nifti(T2_path, return_voxsize=True)


print(t2_data.shape)
print(t2_voxel_size)
new_voxel_size = (1, 1, 1)
print(new_voxel_size)
# Dipy's function. trillinear interpolation used by default
t2_data2, t2_affine2 = reslice(t2_data, t2_affine, t2_voxel_size, new_voxel_size)
print(t2_data2.shape)


t2_data = sitk.ReadImage(T2_path)
# Set desired spacing for reslicing
new_spacing = (1.0, 1.0, 1.0)

# Reslice image
#resliced_t2_image = sitk.Resample(t2_data, new_spacing, sitk.Transform(), sitk.sitkLinear, t2_data.GetOrigin(), t2_data.GetSize(), t2_data.GetDirection())


new_size = [int(sz*spc/new_spc + 0.5) for sz, spc, new_spc in zip(t2_data.GetSize(), t2_data.GetSpacing(), new_spacing)]

# Reslice image
resampler = sitk.ResampleImageFilter()
resampler.SetSize(new_size)
resampler.SetOutputSpacing(new_spacing)
resampler.SetOutputOrigin(t2_data.GetOrigin())
resampler.SetOutputDirection(t2_data.GetDirection())
resampled_t2_image = resampler.Execute(t2_data)


output_path = r'H:\Data\t.nii'
sitk.WriteImage(resampled_t2_image, output_path)


#save_nifti('NH06_Denoised_FP_T2.nii', resampled_t2_image )



################################################## Crop T2 ##########################################################






crop


T2_path = r''


t2_data, t2_affine, t2_voxel_size = load_nifti(T2_path, return_voxsize=True)



##### create mask for T2    ################

maskdata, mask = median_otsu(t2_data, vol_idx=range(1, 25), median_radius=6,
                             numpass=4, autocrop=False, dilate=12)
print('maskdata.shape (%d, %d, %d)' % maskdata.shape)


mask_img = nib.Nifti1Image(mask.astype(np.float32), t2_affine)
t2_img = nib.Nifti1Image(maskdata.astype(np.float32), t2_affine)

nib.save(mask_img,'_t2_binary_mask.nii')
nib.save(t2_img,'full_t2_masked.nii')




#save_nifti('t2_1mmresliced.nii', t2_data, t2_affine2)


'''
