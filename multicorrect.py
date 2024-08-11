#corects every file in the 1 hour window such that azimuthal angle starts from true north along with all other observations
import os
import math
import netCDF4 as nc
import numpy as np
directory = r'G:\PS1\nov\09'
parameter_list = ['Reflectivity_Horizontal','Reflectivity_Vertical','RxPower_Horizontal','RxPower_Vertical','KDP','PHIDP','RHO','SW_Horizontal','SW_Vertical','Uncorrected_Reflectivity_Horizontal',
                 'Uncorrected_Reflectivity_Vertical','Velocity_Horizontal','Velocity_Vertical','ZDR']
files = os.listdir(directory)
for i in range(len(files)) :
    file_path = os.path.join(directory, files[i])
    ncfile = nc.Dataset(file_path, 'a')
    angles = ncfile.variables['Azimuth_Info'][0] # converting 2D to 1D
    starting_angle = int(angles[0])
    starting_index = 360 - starting_angle
    angles = np.roll(angles,-starting_index) #for debugging 
    ncfile.variables['Azimuth_Info'][0] = angles #assigns to the original
    for parameter in parameter_list:
        if parameter in ncfile.variables:
            mat = ncfile.variables[parameter][0] #convert to 2D 
            for j in range(mat.shape[1]):
                col = mat[:,j]
                col = np.roll(col, -starting_index)
                mat[:,j] = col  # Assign modified col back to mat
            ncfile.variables[parameter][0] = mat  # Assign modified mat back to nc
        else:
            print("defect in file no.",i,"parameter",parameter)
    ncfile.close()

    
