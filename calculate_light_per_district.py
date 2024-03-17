#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 23:24:04 2021

@author: me

using the method to merge all files for one day then find stats
"""
import rasterio

from rasterio.merge import merge

from rasterio.plot import show

import os

from rasterstats import zonal_stats


##List input raster files for the given day; already tif file format

#folder containing all the tif files, this should be the same as the output folder from the file convertion script
import_folder = '/Users/me/Desktop/Summer 2021 Lab Files/RasterFiles/tif' 

#district line shape file
district_fp = '/Users/me/Desktop/Summer 2021 Lab Files/gis/AssemblyDistrictsPostDissolved.shp'

#folder where you want to place the merged day raster files; include a / at the end
merge_folder = "/Users/me/Desktop/Summer 2021 Lab Files/RasterFiles/merged/" 

#folder where you want to place the resulting csv files; include a / at the end
csv_folder = '/Users/me/Desktop/Summer 2021 Lab Files/' 




def count_dark(x): 
 count = 0
 one_dim = x.compressed()
 for item in one_dim:
     if item == 0:
         count +=1
 return count



os.chdir(import_folder)
rasterFiles = os.listdir(os.getcwd())
#print(rasterFiles)
print('Input folder number of files:', len(rasterFiles))
master_stats = []

#Data is Available for 2012-01-19 to yesterday

for year in range(2012, 2022):
    days_in_yr = 365
    start_day = 0
    
    #account for leap years, and the data range
    if year == 2012 or year == 2016 or year == 2020:
        days_in_yr = 366
    if year == 2021:
        days_in_yr = 232 #up to 8/20 of this year
    if year == 2012:
        start_day = 19
        
    for day in range (start_day,days_in_yr+1):
        
        date = "A" + str(year) + str(day).zfill(3) #AYYYYDDD format
        day_files = [file for file in rasterFiles if date in file]
        #print(day_files)
        print('Number of files for', date, '(AYYYYDDD format) :', len(day_files))
        if len(day_files) != 16 :
            print ('*error* missing files for' , date, '; currently # of files;', len(day_files),)


        ##merge the files into one
        merged_fp = merge_folder + date + '_merged.tif'
    
        src_files_to_mosaic = []
    
        for fp in day_files:
            src = rasterio.open(fp)
            src_files_to_mosaic.append(src)


        # Merge function returns a single mosaic array and the transformation info
        mosaic, out_trans = merge(src_files_to_mosaic)
        
        show(mosaic, cmap='terrain')
        
        # Copy the metadata
        out_meta = src.meta.copy()
        
        # Update the metadata
        out_meta.update({"driver": "GTiff",
                          "height": mosaic.shape[1],
                          "width": mosaic.shape[2],
                          "transform": out_trans,
                          "crs": "+proj=utm +zone=35 +ellps=GRS80 +units=m +no_defs "
                          }
                         )
        
        # Write the mosaic raster to disk
        with rasterio.open(merged_fp, "w", **out_meta) as dest:
            dest.write(mosaic)
            
        
        #getting the calculated statistics
        num_districts = 4125
        
        
        stats = zonal_stats(district_fp, merged_fp, stats= ['count', 'sum', 'mean'], add_stats={'count_dark': count_dark}, geojson_out = True)
              
        #get only the needed info; taking out the geometry and coordinate info
        #num_disctricts = len(stats)
        for s in stats: 
          master_stats.append( {'Date': date, 'ID': s['id'], 'Count':s['properties']['count'], 'Sum':s['properties']['sum'], 'Day_Average':s['properties']['mean'], 'Count_Dark':s['properties']['count_dark']} )
        
        
        #additional calc stats based on those already calculated
        for k in range (0, num_districts):
          master_stats[k]['percent_dark'] = (master_stats[k]['Count_Dark']/master_stats[k]['Count'])*100.0
          
  
        #write/convert the statistics to csv file
        import csv
        toCSV = master_stats
        keys = toCSV[0].keys()
        csv_fp = csv_folder + date + '_stats.csv'
        with open(csv_fp, 'w', encoding='utf8', newline='')  as output_file: #auto closes file once finish block
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(toCSV)



