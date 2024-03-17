#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from osgeo import gdal 
import os

## filespaths
#contain all h5 files
import_folder = "/Users/me/Desktop/Summer 2021 Lab Files/RasterFiles/also h5/"

#script will put all tif files in this folder; include a / at the end
outputFolder = "/Users/me/Desktop/Summer 2021 Lab Files/RasterFiles/tif/"



os.chdir(import_folder)
rasterFiles = os.listdir(os.getcwd())
#rasterFiles.remove('.DS_Store') #uncomment if using mac

#print(rasterFiles)

for file in rasterFiles:
  #Get File Name Prefix
  rasterFilePre = file[:-3]
  #print(rasterFilePre)

  fileExtension = "_BBOX.tif"

  ## Open HDF file
  #reads the first file.The rasterFiles[ ] index can be modified to select one specific file, 
  #or iterate through all files within the input folder
  hdflayer = gdal.Open(file, gdal.GA_ReadOnly)

  # Open raster layer
  subhdflayer = hdflayer.GetSubDatasets()[0][0]
  rlayer = gdal.Open(subhdflayer, gdal.GA_ReadOnly)

  #Subset the Long Name
  outputName = subhdflayer[92:]

  outputNameNoSpace = outputName.strip().replace(" ","_").replace("/","_")
  outputNameFinal = outputNameNoSpace + rasterFilePre + fileExtension
  #print(outputNameFinal)

  outputRaster = outputFolder + outputNameFinal
  #print (outputRaster)

  #collect bounding box coordinates
  HorizontalTileNumber = int(rlayer.GetMetadata_Dict()["HorizontalTileNumber"])
  VerticalTileNumber = int(rlayer.GetMetadata_Dict()["VerticalTileNumber"])
      
  WestBoundCoord = (10*HorizontalTileNumber) - 180
  NorthBoundCoord = 90-(10*VerticalTileNumber)
  EastBoundCoord = WestBoundCoord + 10
  SouthBoundCoord = NorthBoundCoord - 10

  EPSG = "-a_srs EPSG:4326" #WGS84

  translateOptionText = EPSG+" -a_ullr " + str(WestBoundCoord) + " " + str(NorthBoundCoord) + " " + str(EastBoundCoord) + " " + str(SouthBoundCoord)

  translateoptions = gdal.TranslateOptions(gdal.ParseCommandLine(translateOptionText))
  gdal.Translate(outputRaster,rlayer, options=translateoptions)


print ('done converting files')