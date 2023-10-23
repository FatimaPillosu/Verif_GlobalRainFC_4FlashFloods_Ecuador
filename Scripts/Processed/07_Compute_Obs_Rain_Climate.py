import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv

############################################################################
# CODE DESCRIPTION
# 07_Compute_Obs_Rain_Climate.py computes the observational rainfall climatology for
# each region in the domain of interest. 
# Code runtime: it can take up to 10 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Acc (number, in hours): rainfall accumulation to consider.
# DateS (date, in format YYYYMMDD): start day of the period to consider.
# DateF (date, in format YYYYMMDD): final day of the period to consider.
# AccPerS_list (list of integers): list of the start times of the accumulation periods to consider.
# RegionName_list (list of strings): list of names for the domain's regions.
# RegionCode_list (list of integers): codes for the domain's regions to consider. 
# Git_repo (string): repository's local path.
# FileIN_Mask (string): relative path of the file containing the domain's mask.
# DirIN (string): relative path containing the rainfall observations.
# DirOUT (string): relative path where the observational rainfall climatologies will be stored.

# INPUT PARAMETERS
Acc = 12
DateS = datetime(2010,1,1,0)
DateF = datetime(2019,12,31,0)
AccPerS_list = [0,12]
RegionName_list = ["Costa", "Sierra"]
RegionCode_list = [1,2]
Perc_list = np.concatenate((np.arange(100), np.array([99.5,99.8,99.9])))
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
FileIN_Mask = "Data/Raw/Ecuador_Mask_ENS/Mask.grib"
DirIN = "Data/Raw/OBS/Rain"
DirOUT = "Data/Compute/07_Obs_Rain_Climate"
############################################################################

# Reading the Mask for the regions in the considered domain
mask = mv.read(Git_repo + "/" + FileIN_Mask)

# Computing the observational rainfall climatology
for in_Region in range(len(RegionName_list)):

      # Select the region to consider for the computation of the observational rainfall climatology
      RegionName = RegionName_list[in_Region]
      RegionCode = RegionCode_list[in_Region]

      # Initializing the variable that will contain the rainfall realizations
      obs_rain_region = np.array([])

      # Computing the observational rainfall climatology for the period of interest
      TheDate = DateS
      while TheDate <= DateF:
            
            for AccPerS in AccPerS_list:
                  
                  print("Considering accumulation period starting on " + TheDate.strftime("%Y%m%d") + " at " + f"{AccPerS:02d}" + " for region " + RegionName + "(" + str(RegionCode) + ")")

                  # Reading the rainfall observations
                  FileIN = Git_repo + "/" + DirIN + "_" + f"{Acc:0d}" + "h/" + TheDate.strftime("%Y%m%d") + "/tp" + f"{Acc:02d}" + "_obs_" + TheDate.strftime("%Y%m%d") + f"{AccPerS:02d}" + ".geo"
                  obs_rain_global = mv.read(FileIN)

                  # Extracting the observations for the region to consider
                  mask_obs_global = mv.values(mv.nearest_gridpoint (mask,obs_rain_global))
                  obs_rain_region_temp = mv.filter(mv.values(obs_rain_global), mask_obs_global == RegionCode)
                  if obs_rain_region_temp is not None:
                        obs_rain_region = np.concatenate((obs_rain_region, obs_rain_region_temp))

            TheDate += timedelta(days=1)
      
       # Computing the observational rainfall climatology
      obs_rain_climate_region = np.percentile(obs_rain_region, Perc_list)
      
      # Saving the plot
      DirOUT_temp= Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h"
      FileNameOUT_temp = "Obs_Rain_Climate_" + f"{Acc:02d}" + "h_" + DateS.strftime("%Y%m%d") + "_" + DateF.strftime("%Y%m%d") + "_" + RegionName
      if not os.path.exists(DirOUT_temp):
            os.makedirs(DirOUT_temp)
      np.save(DirOUT_temp + "/" + FileNameOUT_temp, obs_rain_climate_region)
      np.save(DirOUT_temp + "/Percs_computed_" + DateS.strftime("%Y%m%d") + "_" + DateF.strftime("%Y%m%d"), Perc_list)