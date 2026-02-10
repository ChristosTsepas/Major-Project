# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 11:36:35 2024

@author: ctsepas
"""
import os
from Cochlea_ROI import process_masks_to_ROI
from Automated_normalization import process_directory
from Denoising import denoising
from Automated_masking import mask_all_nii_files
from T2_processing import process_and_crop_T2, check_correct_negative_values
 
# Script to call all necessary functions for processing and analysis of dMRI data

if __name__ == "__main__":
    
    step = input("Please type which processing step you want to do. Options are: \n 1) Denoising \n 2) Normalization \n 3) Masking \n 4) Crop or correct for negatives values \n 5) Other step \n Type 'Generate ROIs' if you want to creat Cochlea Rois for further analysis. \n ")
    if (step == "Denoising"):
        input_path = input("Please type the input path Denoising: ")
        output_path = input("Please type the output path Denoising: ")   
        denoising(input_path, output_path)
        
    elif (step == "Masking"):
        input_path = input("Please type the input path for Masking: ")
        output_path = input("Please type the output path Masking: ")
        mask_all_nii_files(input_path, output_path)
        
    elif (step == "Normalization"):
        
        input_path = input("Please type the input path for Normalization: ")
        output_path = input("Please type the output path for Normalization: ")
        
        if not os.path.exists(output_path):
            os.makedirs(output_path)
    
        process_directory(input_path, output_path)  #will change
      
    elif (step == "Crop or correct for negative values"):
        t2_step = input("Please type if you want to 'crop' or 'correct for negative values': ")  
        if (t2_step == "crop"):
            input_path = input("Please type the input path for processing volumes: ")
            output_path = input("Please type the output path for processing volumes: ")  
            process_and_crop_T2(input_path, output_path) #change code to handle min max user inputed
            
        elif(t2_step == "correct for negative values"):
            input_path = input("Please type the input path for processing volumes: ")
            output_path = input("Please type the output path for processing volumes: ")
            check_correct_negative_values(input_path, output_path)
            
        else:
            print("Wrong input.")
        
    elif (step == "Generate ROIs"):
        masks_path = input("Please specify the input path for cochleae masks: ")
        left_path = input(" Please specify output path for left ROIs: ")
        right_path = input(" Please specify the outut path for right ROIs: ")
        left_segm_path = input(" Please specify the output path for left ROIs to be used for segmentation: ")
        right_segm_path = input("Please specify the output path for right ROIs to be used for segmentation: ")
        process_masks_to_ROI(masks_path, left_path, right_path, left_segm_path, right_segm_path)   
        
    elif (step == "Other step"): 
        print("For signal drift, eddy current/motion correction and EPI distortion correction open Matlab and ExploreDTI.")
    else :
        print("Wrong input. Please type a preprocessing step that you want to do.")

        

