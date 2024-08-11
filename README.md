# Real Time Rainfall Estimation using Z values

### Overview

This repository contains the code to find out a relationship between Z (reflectivity of microwaves) from the radar and R (rainfall rate) using the Marshall Palmer Relation specific to the Kalpakkam Region. This project was divided into three parts : 

1. Correction : The raw data is stored in NetCDF format. The reflectivity values started from different azimuth angles. To maintain uniformity in data, this code takes a directory containing all the netcdf files for a particular date and changes their reflectivity values such that each date starts from zero azimuth angle. 
2. Extraction : This code takes in latitude,longitude of the rain gauge and gives the reflectivity values corresponding to this location. Each netcdf file gives a single value. These values were put in a csv file for each date
3. Modelling : Plotted the values of Z and R and found a relation adhering to the Marshall Palmer Equation. 

Visualisation 

Contour Plot of Reflectivity for 4th December 10:10 IST
![image](https://github.com/bulla1009/RainfallEstimation/blob/main/plot.png)
