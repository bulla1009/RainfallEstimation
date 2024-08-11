# Real Time Rainfall Estimation using Z values

### Overview

This repository contains the code to find out a relationship between Z (reflectivity of microwaves) from the radar and R (rainfall rate) using the Marshall Palmer Relation specific to the Kalpakkam Region.

Marshall Palmer Equation : 
![equation](http://www.sciweavers.org/tex2img.php?eq=Z%20%3D%20aR%5E%7Bb%7D&bc=Transparent&fc=White&im=jpg&fs=12&ff=arev&edit=0)
where a and b are the site specific coefficients to be found 

This project was divided into three parts : 
1. Correction : The raw data is stored in NetCDF format. The reflectivity values started from different azimuth angles. To maintain uniformity in data, this code takes a directory containing all the netcdf files for a particular date and changes their reflectivity values such that each date starts from zero azimuth angle. 
2. Extraction : This code takes in latitude,longitude of the rain gauge and gives the reflectivity values corresponding to this location. Each netcdf file gives a single value. These values are collected in a csv file for each date.
3. Modelling : This code finds the coefficients for Marshall Palmer Equation using Linear Regression corresponding to the csv files created by extraction of the netcdf file. 

### Visualisation 
![Contour Plot of Reflectivity for 4th December 10:10 IST](https://github.com/bulla1009/RainfallEstimation/blob/main/plot.png)
