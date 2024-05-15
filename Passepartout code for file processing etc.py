# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 20:18:51 2023

@author: ctsepas
"""

import os
import shutil
import glob
import pandas as pd




# Quick and dirty way for file processing
# Copy-paste files, rename files etc
# Store info from files in Excel



#iterate all the files in a specific directory and rename them

def rename_files(input_directory):
    for filename in os.listdir(input_directory):
        if filename.endswith(".nii"):
            # Generate the new filename by removing "_resampled" from the original filename
            new_filename = filename.replace("_T2_resampled.nii", "_T2.nii")
            
            # Create the full paths for the old and new filenames
            old_filepath = os.path.join(input_directory, filename)
            new_filepath = os.path.join(input_directory, new_filename)
            
            # Rename the file and print out the changes
            os.rename(old_filepath, new_filepath)
            print(f"Renamed: {filename} -> {new_filename}")






def copy_nii_files(copy_folder, paste_folder):
    # Create the destination folder if it doesn't exist
    if not os.path.exists(copy_folder):
        os.makedirs(paste_folder)

    # Use glob to find all .nii files in the source folder.
    # Modify *_T2.nii to handle different types of .nii files
    nii_files = glob.glob(os.path.join(copy_folder, '*_T2.nii'))

    # Copy each .nii file to the destination folder
    for nii_file in nii_files:
        shutil.copy(nii_file, paste_folder)




    
# store file information in excel, assuming that all files are in a single directory

def store_info_in_Excel(input_directory, output_excel_path):
    
    # Use glob to get a list of .nii files in the directory
    nii_files = glob.glob(os.path.join(input_directory, '*.nii'))

    # Create a DataFrame to store basenames
    df = pd.DataFrame(columns=['Basename'])



    # Iterate through each .nii file, read the basename, and store it in the DataFrame
    for nii_file in nii_files:
        
        
        # Basename without extention
        basename = os.path.splitext(os.path.basename(nii_file))[0]
        
        df = df.append({'Basename': basename}, ignore_index=True)
    # Store df into an Excel file
    df.to_excel(output_excel_path, index=False)

    

# Raw data are into different Dicom folder. Iteration through different folders is needed
# Read first .nii of each folder and extract code name


# this function can produce folders from excel names (need it for manual roi specification)





def create_folders_from_excel(excel_file, column_name, start_row, num_rows, folder_path):
    # Load the specific range from the Excel file into a DataFrame
    df = pd.read_excel(excel_file, usecols=column_name, skiprows=start_row-1, nrows=num_rows, header=None)

    # Iterate through the DataFrame and create folders directly under the base directory
    for cell_value in df.values.flatten():
        if isinstance(cell_value, str):
            folder_name = cell_value.strip()
            folder = os.path.join(folder_path, folder_name)
            if not os.path.exists(folder):
                os.makedirs(folder)
                print(f"Created folder: {folder}")
            else:
                print(f"Folder already exists: {folder}")

    print("Folder creation process completed.")
    
    
    
    


def store_nii_basenames(subfolders_directory, output_excel_path):
    
    
    # Create a list to store basenames
    basenames = []

    # Iterate through all subdirectories in the root directory
    for subdirectory in os.listdir(subfolders_directory):
        subdirectory_path = os.path.join(subfolders_directory, subdirectory)

        # Check if the current item is a directory
        if os.path.isdir(subdirectory_path):
            
            # Use glob to get a list of .nii files in the folder
            nii_files = glob.glob(os.path.join(subdirectory_path, '*.nii'))

            # Check if there are any .nii files in the folder
            if nii_files:
                # Read the basename of the first .nii file
                first_nii_file = nii_files[0]
                filename = os.path.splitext(os.path.basename(first_nii_file))[0]

                # Append the filename to the list
                basenames.append(filename)

    # Create a DataFrame with the basenames
    df = pd.DataFrame({'Basename': basenames})

    # Write the DataFrame to an Excel file
    df.to_excel(output_excel_path, index=False)





# this function reads DTI and tract files of the same subject and copy pastes them to the respected subject folder
# where ROIs are placed

def copy_paste_mat_files(input_path, paste_path, paste_segm_path):
    
    for filename in os.listdir(input_path):
        
        if filename.endswith("_MD_C_native.mat"):
            DTI = filename
            tract = filename.replace(".mat", "_Tracts_DTI.mat")
            basename = filename.replace("_MD_C_native.mat","")
            
            # Check if the subject's paste_path folder exists
            if not os.path.exists(os.path.join(paste_path, basename)):
                print(f"Error: Folder associated with subject {basename} does not exist!")
                continue  # Skip this subject if folder doesn't exist
            
            # Check if the subject's paste_segm_path folder exists
            if not os.path.exists(os.path.join(paste_segm_path, basename)):
                print(f"Error: Folder associated with subject {basename} for segmentation does not exist!")
                continue  # Skip this subject if folder doesn't exist
            
            # Copy and paste files
            shutil.copy(os.path.join(input_path, DTI), os.path.join(paste_path, basename))
            shutil.copy(os.path.join(input_path, DTI), os.path.join(paste_segm_path, basename))
            shutil.copy(os.path.join(input_path, tract), os.path.join(paste_path, basename))
            
            print(f"Files for subject {basename} copied and pasted!")




    
if __name__ == "__main__":
    
    
    folder_path = r"H:\Manual ROI generation\Tract_analysis\Right"
    excel_file = r"H:\Data(comments etc).xlsx"
    
    
    
    
    
    create_folders_from_excel(excel_file, "A", 50, 34, folder_path)
    
    
    
    # Specify input directory containing the files
    input_directory = r"H:\Testing\batch\rigid_reg_EDTI"
    copy_folder= r'H:\Rest of data\MD_EPI'
    paste_folder= r'H:\Data\ROI_analysis\Moving'
    
    
    file_directory = r''
    Excel_path = r'H:\Data\Basenames4.xlsx'
    
    
    subfolders_directory = r'H:\Rest of data\DICOM_DTIADS15a'
    
    input_directory = r"H:\Marc_Pastur_pipeline\T2 processing"
    # Call the function to rename the files
    rename_files(input_directory)
    # call function to copy files
    copy_nii_files(copy_folder, paste_folder)
    
    
    # call function to store info in Excel
    store_info_in_Excel(file_directory, Excel_path)   
    store_nii_basenames(subfolders_directory, Excel_path)
    
    
    # call function to copy paste DTI and tract files
    copy_path = r"H:\Marc_Pastur_pipeline\DTI_MODEL\Tractography"
    paste_path = r"H:\Marc_Pastur_pipeline\DTI_MODEL\ROI_generation\Tract_analysis\Right" # right
    paste_segm_path = r"H:\Marc_Pastur_pipeline\DTI_MODEL\ROI_generation\Segmentation\Right" # right
    copy_paste_mat_files(copy_path, paste_path, paste_segm_path)
        
        
        
        
        
        
        
        
        
        
    
    
    