import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv

######################################################################################
# CODE DESCRIPTION
# 11_Compute_AverageYear_RainOBS.py computes the annual average rain for different accumulation 
# periods, and extracts the location of the rainfall observations used in the computations.
# Note: the code takes up to 5 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Acc (number, in hours): rainfall accumulation to consider.
# DateTimeS (date, in format YYYYMMDD): start date of the considered verification period.
# DateTimeF (date, in format YYYYMMDD): final date of the considered verification period.
# AccPerF_list (list of integer, inUTC hours): list of the final times of the accumulation periods to consider.
# RegionName_list (list of strings): list of names for the domain's regions.
# RegionCode_list (list of integers): codes for the domain's regions to consider. 
# Git_repo (string): repository's local path.
# FileIN_Mask (string): relative path of the file containing the domain's mask.
# DirIN (string): relative path containing the raw rainfall observations.
# DirOUT (string): relative path of the plots containing the annual average rain.

# INPUT PARAMETERS
Acc = 12
DateTimeS = datetime(2020,1,1,0)
DateTimeF = datetime(2020,12,31,0)
AccPerF_list = [12,0]
RegionName_list = ["Costa", "Sierra"]
RegionCode_list = [1,2]
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
FileIN_Mask = "Data/Raw/Ecuador_Mask_ENS/Mask.grib"
DirIN = "Data/Raw/OBS/Rain"
DirOUT = "Data/Compute/11_AverageYear_RainOBS"
######################################################################################

# Creating the output directory
DirOUT_temp= Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h"
if not os.path.exists(DirOUT_temp):
      os.makedirs(DirOUT_temp)

# Reading the mask for the regions in the considered domain
mask = mv.read(Git_repo + "/" + FileIN_Mask)

# Computing the annual rainfall average for a specific region
for ind_Region in range(len(RegionName_list)):
      
      RegionName = RegionName_list[ind_Region]
      RegionCode = RegionCode_list[ind_Region]

      # Initializing the variables that will contain the annual rainfall averages
      tp_av_year = np.empty((len(AccPerF_list),2)) * np.nan

      # Computing the annual average rainfall for a specifc accumulation period
      for ind_AccPerF in range(len(AccPerF_list)):
            
            AccPerF = AccPerF_list[ind_AccPerF]

            # Initializing the variable that will contain the rainfall observations for the region
            vals_obs_region = np.array([])
            lats_obs_region = np.array([])
            lons_obs_region = np.array([])

            # Computing the annual average rainfall for the considered year
            TheDateTime = DateTimeS + timedelta(hours=AccPerF)
            while TheDateTime <= DateTimeF:
                  
                  print("Post-processing observations for period ending on ", TheDateTime, " for ", RegionName)
            
                  # Reading global rainfall observations
                  FileIN = Git_repo + "/" + DirIN + "_" + f"{Acc:02d}" + "h/" + TheDateTime.strftime("%Y%m%d") + "/tp" + f"{Acc:02d}" + "_obs_" + TheDateTime.strftime("%Y%m%d") + TheDateTime.strftime("%H") + ".geo"
                  obs = mv.read(FileIN)

                  # Selecting the observations for the region and the considered accumulation period
                  mask_at_obs = mv.nearest_gridpoint(mask, obs)
                  vals_obs_region = np.concatenate((vals_obs_region, mv.values(mv.filter(obs, mask_at_obs == RegionCode))))
                  lats_obs_region = np.concatenate((lats_obs_region, mv.latitudes(mv.filter(obs, mask_at_obs == RegionCode))))
                  lons_obs_region = np.concatenate((lons_obs_region, mv.longitudes(mv.filter(obs, mask_at_obs == RegionCode))))
                  
                  TheDateTime = TheDateTime + timedelta(days=1)

            # Computing the annual rainfall average 
            tp_av_year[ind_AccPerF,0] = AccPerF
            tp_av_year[ind_AccPerF,1] = np.mean(vals_obs_region)

            # Saving the observations timeseries
            FileNameOUT_vals_obs = "vals_obs_" + f"{Acc:02d}" + "h_" + RegionName + "_" + f"{AccPerF:02d}" + "UTC"
            FileNameOUT_lats_obs = "lats_obs_" + f"{Acc:02d}" + "h_" + RegionName + "_" + f"{AccPerF:02d}" + "UTC"
            FileNameOUT_lons_obs = "lons_obs_" + f"{Acc:02d}" + "h_" + RegionName + "_" + f"{AccPerF:02d}" + "UTC"
            np.save(DirOUT_temp + "/" + FileNameOUT_vals_obs, vals_obs_region)
            np.save(DirOUT_temp + "/" + FileNameOUT_lats_obs, lats_obs_region)
            np.save(DirOUT_temp + "/" + FileNameOUT_lons_obs, lons_obs_region)

      # Saving the plot
      FileNameOUT_av_obs = "AverageYear_RainOBS_" + f"{Acc:02d}" + "h_" + RegionName
      np.save(DirOUT_temp + "/" + FileNameOUT_av_obs, tp_av_year)