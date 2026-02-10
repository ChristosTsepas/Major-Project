# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 18:12:49 2023

@author: ctsepas
"""
import os
import nibabel as nib
import numpy as np
from dipy.io.image import load_nifti, save_nifti
import cv2
from scipy.io import savemat
from scipy.ndimage import affine_transform
from dipy.segment.mask import applymask
import matplotlib as plt
from shapely.geometry import Polygon, Point
import matplotlib.pyplot as plt

# Algorithm
# Manually segment masks for left and right T2
# Save them in a single folder with the {subject name}_left.nii and {subject_name}_right.nii
# Load each mask and calculate center coordinates
# Define mid sagittal plane

# Parametrize the center coordinates (hexgagon equation, create an hexagon from the central coordinates) 
# By knowing the centers can calculate the ROI
# Go and calculate M hexagons (for M slices subject/mask dependant ROI has the same slices as the mask)
# Transform mid sagittal plane and go 0.75*|cochlea - midpoint|  slices right/left
# AND rois are SEED ROI dpeendant
# AND ROIs are restricted in order to eliminate false tracts.
# Y0 and Y1, Z0 and Z1 of the rectangular is based on the minimum and maximum Yo, Zo of the SEED hexaonal ROI.
# Ymin = | min(Ycochleae) – 4| (4 voxels below the minimum y).
# Ymax = | max(Ycochleae + 2 | (2 voxels above the maximum y).
# Zmin = | min (Zcochleae) – 2 | (2 voxels below the minimum z).
# Zmax = | max(Zcochleae) + 1 | (1 voxel above the maximum z).

# Create two folders Left and Right 
# save ROI coordinates as .txts in subfolders with names _subject_name 
# General file structure
# ROI_generation
    # -> Tract_analysis
                #Left
                # Right
    # -> Segmentation 
                #Left
                #Right

# 1 for analyzing/splitting the tracts of interest. This folder contains:
        # Left and right subfolders
            # Subject name subfolders
                # .txt, .m files of SEED and AND ROIs, processed DKI files and Whole brain tract

# 2 for segmenting tracts of interest:
    # Big folder with Segmentation
        # Two folders with left and right
         # Subfolders with subjects
             # .txt and .m with AND rois, DKI data and the saved tracts of interest


# Matlab will create .mat ROI files and run script with EDTI functions

# Then segmented tracts will be saved to different left and right folders all together
# for calculating statistics and mean values.
# NOTE: My coordinates depend on slices (image coordinates).
# ExploreDTI uses as an input voxel coordinates (so multiplying by voxel resolution).

def hexagon_corners_from_center(x0, y0, distance, z_values):
    angles = np.linspace(0, 2*np.pi, 7)[:-1]  #angles in radians
    corners = []
    for z_value in z_values:
        for angle in angles:
            corner = (
                round(x0 + distance * np.cos(angle), 4),
                round(y0 + distance * np.sin(angle), 4),
                z_value
            )
            corners.append(corner)

    return np.array(corners)


def all_integer_points_inside_hexagon(center_coordinates, distance, z_value):
    x0, y0 = center_coordinates
    # Initialize a list to store all integer points inside the hexagon for a specific z slice
    all_points = []
    # Iterate over all potential integer coordinates inside the hexagon
    for x_int in range(int(x0 - distance), int(x0 + distance) + 1):
        for y_int in range(int(y0 - distance), int(y0 + distance) + 1):
            # Check if the current integer point is inside the hexagon
            if (
                Polygon(hexagon_corners_from_center(x0, y0, distance, [z_value])).contains(Point(x_int, y_int, z_value))
            ):
                all_points.append((x_int, y_int, z_value))
    
    return np.array(all_points)

# insert y0, z0, y1 
# top/bottom, right/left are defined based on visualization in ITKSnap
def rectangle_corners_from_center(x0, y0, z0, y1, z1):
           
            # Calculate coordinates of the four corners of the rectangular
            top_left = (round(x0, 4), y1 ,z1)
            top_right = (round(x0, 4),  y0,z1)
            bottom_right = (round(x0, 4), y0, z0)
            bottom_left = (round(x0, 4),  y1, z0)
            
            return top_left, top_right, bottom_right, bottom_left


# just define corners and distance
# for every point just iterate z = [z0, z0+8]
# y from y0 to y1 +1
# that's all :)                    
def all_integer_points_inside_rectangle(x0, y0, z0, y1, z1):
    # Initialize a list to store all integer points inside the rectangle
    all_points = []
    # Iterate over all potential integer coordinates inside the rectangle
    # and satisfy the condition ∣y−y0∣≤ ymax and ∣z−z0∣≤ zmax
    for y_int in range(int(y0), y1 + 1):
        for z_int in range(int(z0), z1 + 1):
            # Check if the current integer point is inside the rectangle
            if (
                abs(y_int - y0) <= y1+1  and
                abs(z_int - z0) <= z1+1
            ):
                all_points.append((x0, y_int, z_int))
            
    return np.array(all_points)
    
# a simple function to create a rectangular ROI and save all points inside
#top/bottom, right/left are defined based on visualization in ITKSnap in x plane
def rectangular_AND_ROI_segm(x0, ymin, ymax, zmin, zmax):
    
    top_left = (x0, ymax ,zmax)
    top_right = (x0,  ymin, zmax)
    bottom_right = (x0, ymin, zmin)
    bottom_left = (x0,  ymax, zmin)    
    
    return top_left, top_right, bottom_right, bottom_left


def points_inside_AND_ROI_segm(x0, ymin, ymax, zmin, zmax):
    
    all_points = []
    #y and z are defined based on the hexagonal ROI corner coordinates. They might be floats
    # It is mandatory to make them integers   
    for y in range(int(ymin), int(ymax) + 1):
        for z in range (int(zmin), int(zmax) + 1):
         if (
                abs(y - ymin) <= ymax  and
                abs(z - zmin) <= zmax
            ):
                all_points.append((x0, y, z))
             
    return np.array(all_points)
    
# helper function to calculate mean of masks
def calculate_roi_center(roi):    
    center = np.mean(np.argwhere(roi), axis=0)
    return center


# two big directories will be created.
# 1 for splitting the tracts (using SEED and AND)
# 1 for segmenting the already splitted tracts using 2 AND ROIs
# then the splitted tracts will be saved in the segmentation folder in subfolders for each patient
# the tracts will be segmented and stored in a single folder named after each subject 
# Then statistics will be applied
def process_masks_to_ROI(masks_path, left_path, right_path, left_segm_path, right_segm_path):
    
    for filename in os.listdir(masks_path):
        if filename.endswith('_left.nii'):
            left = filename
            right = filename.replace("_left.nii", "_right.nii")
            subject_id = filename.replace("_left.nii", "")
            left_roi_file = os.path.join(masks_path, left)
            right_roi_file = os.path.join(masks_path, right)
           
            # error handling if one of the masks is missing
            if not os.path.exists(left_roi_file) or not os.path.exists(right_roi_file):
                print(f"Error: Left or Right mask file not found for subject {subject_id}")
                continue
            # specify arrays for left and right ROI
            # determine mid point coordinates
            # specify left and right directories for tract analysis and segmentation
            
            left_roi, left_array = load_nifti(left_roi_file)
            left_roi_center = calculate_roi_center(left_roi) 
            right_roi, right_array = load_nifti(right_roi_file)
            right_roi_center = calculate_roi_center(right_roi)
    
            midpoint = (left_roi_center + right_roi_center) / 2
                    
            # move the point that defines the mid sagittal plane 12 voxels to left and right
            modified_array_left = midpoint[0]- 0.75*(abs(midpoint[0]-left_roi_center[0]))
            left_mid_point = np.array([modified_array_left, midpoint[1], midpoint[2]])
            modified_array_right = midpoint[0]+0.75*(abs(midpoint[0]-right_roi_center[0]))
            right_mid_point = np.array([modified_array_right, midpoint[1], midpoint[2]])
            
            # For Left
            left_patient_folder = os.path.join(left_path, subject_id)
            os.makedirs(left_patient_folder, exist_ok=True)
            
            # For Right
            right_patient_folder = os.path.join(right_path, subject_id)
            os.makedirs(right_patient_folder, exist_ok=True)
            
            # For Left segmentation
            left_segm_folder = os.path.join(left_segm_path, subject_id)
            os.makedirs(left_segm_folder, exist_ok=True)
            
            # For Right segmentation
            right_segm_folder = os.path.join(right_segm_path, subject_id)
            os.makedirs(right_segm_folder, exist_ok=True)
           
###########################################    Determine Hexagonal ROIs    #########################################################
        
            # initialize center coordinates
            x0, y0 = left_roi_center[0]+1, left_roi_center[1]+1
            distance = 3  
            # define minimum and maximum range of slices based on the specific mask of each subject.
            # Then the approach is robust and the hexagonal ROI is going to be subject dependent
            # return minimum/maximum z that has non zero elements
            # numpy starts from 0 so +1 to match the real voxel coordinates
            zmin_left = np.min(np.argwhere(left_roi), axis=0)[2]+1         
            zmax_left = np.max(np.argwhere(left_roi), axis=0)[2]+1      
            z_values = range(zmin_left, zmax_left+1)
            hexagon_corners_array_left =  np.array(hexagon_corners_from_center(x0, y0, distance, z_values))  
            all_points_inside_array_left = np.empty((0, 3), dtype=int)
            
            # SPECIFY THE Z values depending on the z of the masks
            # so roi is going to be exactly on top of the cochlea in exploreDTI
            # Try to iterate through each z values specified by the min and max of the z coordinate of each mask
            # so z_values = (min(left[;,;,1])), max(left[;,;,1])
            # Then change enumeration and store them as SEED_1, SEED_2, SEED_3
            # iterate through each value but name the hROI_SEED_ 1, 2, 3, 4, 5...
            # That's easier when handling ROIs
            counter1 = 1
            for z_value in z_values: 
                
                # else: distance = smaller and create spherical ROI
                # Get the coordinates of points on the corners of the hexagon
                hexagon_corners_left = hexagon_corners_from_center(x0, y0, distance, [z_value])
                hexagon_corners_array_left = np.array(hexagon_corners_left)
            
                # Save hexagon corners to a text file
                hexagon_filename = os.path.join(left_patient_folder, f'hROI_SEED_{counter1}.txt')
                np.savetxt(hexagon_filename, hexagon_corners_array_left, fmt='%.4f')
            
                # Get the coordinates of all integer points inside the hexagon for the current z slice
                all_points_inside_left = all_integer_points_inside_hexagon((x0, y0), distance, z_value)
                all_points_inside_array_left = np.concatenate((all_points_inside_array_left, all_points_inside_left), axis=0)
            
                # Save points inside hexagon to a text file
                points_inside_hexagon_filename = os.path.join(left_patient_folder, f'ROI_SEED_{counter1}.txt')
                np.savetxt(points_inside_hexagon_filename, all_points_inside_left.astype(int), fmt='%d')    
                counter1 += 1
           
            # initialize center coordinates
            x0, y0 = right_roi_center[0]+1, right_roi_center[1]+1
            distance = 3  
            # numpy starts from 0 so +1 to match the real voxel coordinates
            zmin_right = np.min(np.argwhere(right_roi), axis=0)[2]+1
            zmax_right = np.max(np.argwhere(right_roi), axis=0)[2]+1
            z_values = range(zmin_right, zmax_right+1)  # +1 we need zmax as well
            hexagon_corners_array_right = np.array(hexagon_corners_from_center(x0, y0, distance, z_values))
            all_points_inside_array_right = np.empty((0, 3), dtype=int)
        
            counter2 = 1
            # Iterate through slices between 5, 12. Template space the ROI is (6, 10). but include more slices including the transformed ones
            for z_value in z_values:
                # Get the coordinates of points on the corners of the hexagon
                hexagon_corners_right = hexagon_corners_from_center(x0, y0, distance, [z_value])
                hexagon_corners_array_right = np.array(hexagon_corners_right)
                
                # Save hexagon corners to a text file
                hexagon_filename_right = os.path.join(right_patient_folder, f'hROI_SEED_{counter2}.txt')
                np.savetxt(hexagon_filename_right, hexagon_corners_array_right, fmt='%.4f')  #maintain 4 digits float number for corner coordinates
                # Get the coordinates of all integer points inside the hexagon for the current z slice
                all_points_inside_right = all_integer_points_inside_hexagon((x0, y0), distance, z_value)
                all_points_inside_array_right = np.concatenate((all_points_inside_array_right, all_points_inside_right), axis=0)
                # Save points inside hexagon to a text file
                right_points_inside_hexagon_filename = os.path.join(right_patient_folder, f'ROI_SEED_{counter2}.txt')
                np.savetxt(right_points_inside_hexagon_filename, all_points_inside_right.astype(int), fmt='%d') #save the points as an integer -> voxel coordinates
    
                counter2 += 1
    
#######################################       Determine rectangular ROIs        ####################################################
            # Define y0 and y1. how wide the AND ROI?
            # define z0. the max z is defined inside the helper funciton 
            y1_AND = int(np.max(hexagon_corners_array_left[:,1])+3) #2 voxels above the cochlea ROI (+1 because we are numpy!!)
            y0_AND = int(np.min(hexagon_corners_array_left[:,1])-5) # 4 voxels below the cochlea ROI (+1 because numpy!!)
            z0_AND = int(np.min(hexagon_corners_array_left[:,2])-3) #2 slices below the cochlea
            z1_AND = int(np.min(hexagon_corners_array_left[:,2])+2) # 1 slice above the cochlea
            
            # Get the coordinates of points on the corners of the rectangle
            rectangle_corners_left = rectangle_corners_from_center(left_mid_point[0], y0_AND, z0_AND, y1_AND, z1_AND)
            # Get the coordinates of all integer points inside the rectangle
            all_points_inside_left_mid = all_integer_points_inside_rectangle(left_mid_point[0], y0_AND, z0_AND, y1_AND, z1_AND)
            # Convert lists to NumPy arrays
            rectangle_corners_array_left = np.array(rectangle_corners_left)   
            all_points_inside_array_left_mid = np.array(all_points_inside_left_mid)
            # Save rectangle corners to a text file to splitter directory
            rectangle_filename = os.path.join(left_patient_folder, r'hROI_AND_1.txt')
            np.savetxt(rectangle_filename, rectangle_corners_array_left, fmt='%.4f')
            # Save points inside rectangle to a text file
            points_inside_rectangle_filename = os.path.join(left_patient_folder, r'ROI_AND_1.txt')
            np.savetxt(points_inside_rectangle_filename, all_points_inside_array_left_mid.astype(int), fmt='%d') 
            
            # Save rectangular AND ROI to segmentation directory
            np.savetxt(os.path.join(left_segm_folder, r'hROI_AND_1.txt'), rectangle_corners_array_left, fmt='%.4f' )
            np.savetxt(os.path.join(left_segm_folder, r'ROI_AND_1.txt'), all_points_inside_array_left_mid.astype(int), fmt='%d')    
            
            y1_AND = int(np.max(hexagon_corners_array_right[:,1])+3) #2 voxels above the cochlea ROI (+1 because we are numpy!!)
            y0_AND = int(np.min(hexagon_corners_array_right[:,1])-5) # 4 voxels below the cochlea ROI (+1 because numpy!!)
            z0_AND = int(np.min(hexagon_corners_array_right[:,2])-3) #2 slices below the cochlea
            z1_AND = int(np.min(hexagon_corners_array_right[:,2])+2) # 1 slice above the cochlea
            
            # Get the coordinates of points on the corners of the rectangle
            rectangle_corners_right = rectangle_corners_from_center(right_mid_point[0], y0_AND, z0_AND, y1_AND,z1_AND)
            # Get the coordinates of all integer points inside the rectangle
            all_points_inside_right_mid = all_integer_points_inside_rectangle(right_mid_point[0], y0_AND, z0_AND, y1_AND, z1_AND)
            # Convert lists to NumPy arrays
            rectangle_corners_array_right = np.array(rectangle_corners_right) 
            all_points_inside_array_right_mid = np.array(all_points_inside_right_mid)
            # Save rectangle corners to a .txt file
            right_rectangle_filename = os.path.join(right_patient_folder, r'hROI_AND_1.txt')
            np.savetxt(right_rectangle_filename, rectangle_corners_array_right, fmt='%.4f')
            
            # Save points inside rectangle to a text file
            right_points_inside_rectangle_filename = os.path.join(right_patient_folder, r'ROI_AND_1.txt')
            np.savetxt(right_points_inside_rectangle_filename, all_points_inside_array_right_mid.astype(int), fmt='%d')

            # Save txt to segmentation folder as well
            np.savetxt(os.path.join(right_segm_folder, r'hROI_AND_1.txt'), rectangle_corners_array_right, fmt='%.4f' ) 
            np.savetxt(os.path.join(right_segm_folder, r'ROI_AND_1.txt'), all_points_inside_array_right_mid.astype(int), fmt='%d')

            
    ##############################  create AND roi for segmentation  for left and right cochlea    ###################
            
            x0_left = left_roi_center[0] + 1 # define the AND segmentation ROI based on the center of the cochlea 
            ymin = int(np.min(hexagon_corners_array_left[:,1])+1)  #find the down boundary of hexagonal roi (but as an integer)
            ymax = int(np.max(hexagon_corners_array_left[:, 1])+1)  
        
            segm_ROI_array_left = np.array(rectangular_AND_ROI_segm(x0_left, ymin, ymax, zmin_left, zmax_left))  
            points_inside_AND_left = np.array(points_inside_AND_ROI_segm(x0_left, ymin, ymax, zmin_left, zmax_left))         
             
            # Save segmetation ROI
            np.savetxt(os.path.join(left_segm_folder, r'hROI_AND_2.txt'), segm_ROI_array_left, fmt='%.4f' )      
            np.savetxt(os.path.join(left_segm_folder, r'ROI_AND_2.txt'), points_inside_AND_left.astype(int), fmt='%d')   
              
            x0_right = right_roi_center[0] + 1
            ymin = int(np.min(hexagon_corners_array_right[:,1])+1)  #find the down boundary of hexagonal roi (but as an integer)
            ymax = int(np.max(hexagon_corners_array_right[:,1])+1) 
            segm_ROI_array_right = np.array(rectangular_AND_ROI_segm(x0_right, ymin, ymax, zmin_right, zmax_right))
            points_inside_AND_right = np.array(points_inside_AND_ROI_segm(x0_right, ymin, ymax, zmin_right, zmax_right))
                
            # Save segmetation ROI
            np.savetxt(os.path.join(right_segm_folder, r'hROI_AND_2.txt'), segm_ROI_array_right, fmt='%.4f' )    
            np.savetxt(os.path.join(right_segm_folder, r'ROI_AND_2.txt'), points_inside_AND_right.astype(int), fmt='%d')
            print(f"Processing for subject {subject_id} done!")
     
        
if __name__ == "__main__":        
        # Run script
        # Specify the path of the manual segmented masks
        # Specify the path to store left and right SEED and AND coordinates
        # Specify the path to store left and right AND coordinates for segmentation 
        masks_path = r"H:\Marc_Pastur_pipeline\DTI_MODEL\Masks"
        left_path = r"H:\Marc_Pastur_pipeline\DTI_MODEL\ROI_generation\Tract_analysis\Left"
        right_path= r"H:\Marc_Pastur_pipeline\DTI_MODEL\ROI_generation\Tract_analysis\Right"
        left_segm_path = r"H:\Marc_Pastur_pipeline\DTI_MODEL\ROI_generation\Segmentation\Left"
        right_segm_path = r"H:\Marc_Pastur_pipeline\DTI_MODEL\ROI_generation\Segmentation\Right"  
        process_masks_to_ROI(masks_path, left_path, right_path, left_segm_path, right_segm_path)
