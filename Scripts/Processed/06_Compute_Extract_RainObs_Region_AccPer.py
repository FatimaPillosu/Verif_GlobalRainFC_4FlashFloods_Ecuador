import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv
import matplotlib.pyplot as plt

############################################################################################
# CODE DESCRIPTION
# 06_Compute_Extract_RainObs_Region_AccPer.py extracts the rainfall observations per region and accumulation 
# period.
# Code runtime: the code takes up to 30 minutes to run in series.

# INPUT PARAMETERS DESCRIPTION
# Acc (number, in hours): rainfall accumulation to consider.
# DateS (date, in format YYYYMMDD): start day of the period to consider.
# DateF (date, in format YYYYMMDD): final day of the period to consider.
# AccPerF_list (list of integer, inUTC hours): list of the final times of the accumulation periods to consider.
# RegionCode_list (list of integers): codes for the domain's regions to consider. 
# RegionName_list (list of strings): names for the domain's regions to consider.
# RegionColour_list (list of strings): rgb-codes for the domain's regions to consider.
# Git_repo (string): repository's local path.
# FileIN_Mask (string): relative path of the file containing the domain's mask.
# DirIN (string): relative path containing the raw rainfall observations.
# DirOUT (string): relative path containing the extracted rainfall observations per region and accumulation period.

# INPUT PARAMETERS
Acc = 12
DateS = datetime(2010,1,1,0)
DateF = datetime(2020,12,31,0)
AccPerF_list = [12,0]
RegionCode_list = [1,2,3]
RegionName_list = ["Costa", "Sierra", "Oriente"]
RegionColour_list = ["#ffea00", "#c19a6b", "#A9FE00"]
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
FileIN_Mask = "Data/Raw/Ecuador_Mask_ENS/Mask.grib"
DirIN = "Data/Raw/OBS/Rain"
DirOUT = "Data/Compute/06_Extract_RainObs_Region_AccPer"
############################################################################################

# Reading the domain's mask
FileIN_Mask = Git_repo + "/" + FileIN_Mask
mask = mv.read(FileIN_Mask)

# Reading the rainfall observations for each day
TheDate = DateS
while TheDate <= DateF:

      # Reading the rainfall observations for each accumulation period
      for AccPerF in AccPerF_list:

            print("Processing rainfall observations in the " + f"{Acc:02d}" + "-hourly accumulation period ending on  " + TheDate.strftime("%Y%m%d") + " at "+ f"{AccPerF:02d}" + " UTC")

            # Reading the observations
            FileIN = Git_repo + "/" + DirIN + "_" + f"{Acc:02d}" + "h/" + TheDate.strftime("%Y%m%d") + "/tp" +  f"{Acc:02d}" + "_obs_" + TheDate.strftime("%Y%m%d") + f"{AccPerF:02d}" + ".geo"
            obs_global = mv.read(FileIN)

            # Extracting the rainfall observations for a specific region
            for in_Region in range(len(RegionName_list)):

                  # Select the region to consider
                  RegionName = RegionName_list[in_Region]
                  RegionCode = RegionCode_list[in_Region]

                  # Extracting the observations for the region to consider
                  mask_obs = mv.nearest_gridpoint (mask, obs_global)
                  vals_obs_region = mv.values(mv.filter(obs_global, mask_obs == RegionCode))
                  lats_obs_region = mv.latitudes(mv.filter(obs_global, mask_obs == RegionCode))
                  lons_obs_region = mv.longitudes(mv.filter(obs_global, mask_obs == RegionCode))
                  obs_region = np.vstack((lats_obs_region, lons_obs_region, vals_obs_region))

                  # Save the extracted rainfall observations
                  DirOUT_temp = Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h/" + TheDate.strftime("%Y%m%d")
                  if not os.path.exists(DirOUT_temp):
                        os.makedirs(DirOUT_temp)
                  FileNameOUT = "tp" +  f"{Acc:02d}" + "_obs_" + TheDate.strftime("%Y%m%d") + f"{AccPerF:02d}" + "_" +  RegionName + ".npy"
                  np.save(DirOUT_temp + "/" + FileNameOUT, obs_region)
            
      TheDate = TheDate + timedelta(days=1)