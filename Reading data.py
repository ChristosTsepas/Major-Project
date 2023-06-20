# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 13:07:02 2023

@author: User
"""
import os 

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animate
import numpy as np
import dipy.io as io
from mpl_toolkits.mplot3d import Axes3D
import dipy.core.geometry as geo



        
#I don't like this because the user has to change every time the file directory

fbvals = r'D:\Utrecht University\Major Project\Data\DICOM_NH02\DICOM_NH02_WIP_DKI_gehoor_AP_SENSE_20170101164340_501.bval'
fbvecs = r'D:\Utrecht University\Major Project\Data\DICOM_NH02\DICOM_NH02_WIP_DKI_gehoor_AP_SENSE_20170101164340_501.bvec'
        
bval, bvec = io.read_bvals_bvecs(fbvals, fbvecs)

print(bval)
print(bvec)


#calculating and writing b matrices in a .txt file
b_matrices = []

for bval, bvec in zip(bval, bvec):
    b_matrix = bval * np.outer(bvec, bvec)
    b_matrices.append(b_matrix) 



with open('b_matrices.txt', 'w') as f:
    for i, b_matrix in enumerate(b_matrices):
        f.write(f"b-matrix {i+1}:\n")
        np.savetxt(f, b_matrix, delimiter='\t', fmt='%f')
        f.write('\n')



# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot each matrix
for b_matrix in b_matrices:
    # Extract the coordinates from the matrix
    x = b_matrix[:, 0]
    y = b_matrix[:, 1]
    z = b_matrix[:, 2]
    
    # Plot the points
    ax.scatter(x, y, z)

# Set labels for each axis
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Show the plot
plt.show()





    
 