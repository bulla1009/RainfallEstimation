import os
import netCDF4 as nc
import math
import pandas as pd
import numpy.ma as ma
import re
from datetime import datetime, time

def utc_to_ist(utc_time):
    hours_utc = int(utc_time[:2])
    minutes_utc = int(utc_time[2:4])
    seconds_utc = int(utc_time[4:6])
    hours_ist = hours_utc + 5
    minutes_ist = minutes_utc + 30
    if minutes_ist >= 60:
        minutes_ist -= 60
        hours_ist += 1
    if hours_ist >= 24:
        hours_ist -= 24
    ist_time = int(f"{hours_ist:02}{minutes_ist:02}{seconds_utc:02}")
    return ist_time
    
def round_time(time_str):
    time = int(time_str)
    rounded_time = str(time -time%1000)
    return rounded_time
    
def haversine_distance(lat1, lon1, lat2, lon2, radius=6378.137):
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c
    return distance

def initial_bearing(lat1, lon1, lat2, lon2):
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    dlon = lon2_rad - lon1_rad
    x = math.sin(dlon) * math.cos(lat2_rad)
    y = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon)
    bearing = math.atan2(x, y)
    bearing = math.degrees(bearing)
    bearing = (bearing + 360) % 360  
    return bearing

def lat_lon_to_radius_azimuthal(lat, lon, elev_angle, igcar_lat, igcar_lon, radius=6378.137):
    horizontal_distance = haversine_distance(igcar_lat, igcar_lon, lat, lon, radius)
    elev_angle_rad = math.radians(elev_angle)
    radial_distance = horizontal_distance / math.cos(elev_angle_rad)
    azimuth = initial_bearing(igcar_lat, igcar_lon, lat, lon)
    radial_distance = round(radial_distance, 6)
    azimuth = round(azimuth, 6)
    return radial_distance, azimuth

igcar_lat = 12.8352
igcar_lon = 80.1826
# old rain gauge location (2023)
#target_lat = 12.583966
#target_lon = 80.173783
# new rain gauge location (2024)
target_lat = 12.563796
target_lon = 80.127402
directory = r'G:\PS1\8 Jan'
files = os.listdir(directory)
data = []
time = []
ele = []
pattern_ele = r"ELE-([\d\.]+)"
pattern_time = r'\d{4}-\d{2}-\d{2}-\d{6}'
for i in range(len(files)):
    file_path = os.path.join(directory, files[i])
    ncfile = nc.Dataset(file_path, 'r')
    if 'Reflectivity_Horizontal' in ncfile.variables:
        elev_angle = float(format(ncfile.variables['Elevation_Info'][0][0],".2f"))
        r, phi = lat_lon_to_radius_azimuthal(target_lat, target_lon, elev_angle, igcar_lat, igcar_lon) 
        index1 = int(phi)
        index2 = int(r / 0.15)
        data.append(ncfile.variables['Reflectivity_Horizontal'][0][index1][index2]) #reflectivity value at that point
    else:
        data.append(0) #to maintain continuity
    match = re.search(pattern_ele, files[i])
    ele.append(match.group(1))
    match = re.search(pattern_time,files[i])
    time.append(match.group())
        
#replace the -- values by 0
for i in range(len(data)):
    if ma.is_masked(data[i]):
        data[i] = 0
df = pd.DataFrame()
df['Z'] = data
df['time'] = time
df['elevation'] = ele
#df = df.sort_values(by = "time")
df = df.reset_index(drop = True)
df.to_csv('all_values_8_jan.csv')
