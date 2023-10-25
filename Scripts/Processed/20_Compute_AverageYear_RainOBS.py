import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv

######################################################################################
# CODE DESCRIPTION
# 20_Compute_AverageYear_RainOBS.py computes the annual average rain for different accumulation 
# periods.
# Note: runtime code negligible.

# INPUT PARAMETERS DESCRIPTION
# Acc (number, in hours): rainfall accumulation to consider.
# DateS (date, in format YYYYMMDD): start date of the considered verification period.
# DateF (date, in format YYYYMMDD): final date of the considered verification period.
# AccPerS_list (list of integer, inUTC hours): list of the start times of the accumulation periods to consider.
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
AccPerS_list = [0,12]
RegionName_list = ["La Costa", "La Sierra"]
RegionCode_list = [1,2]
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
FileIN_Mask = "Data/Raw/Ecuador_Mask_ENS/Mask.grib"
DirIN = "Data/Raw/OBS/Rain"
DirOUT = "Data/Compute/20_AverageYear_RainOBS"
######################################################################################


# Reading the mask for the regions in the considered domain
mask = mv.read(Git_repo + "/" + FileIN_Mask)

# Computing the annual average rainfall for the considered accumulation period
for AccPerS in AccPerS_list:

      # Initializing the variable that will contain the annual rainfall average for all the considered regions in the domain
      tp_av_year = []

      # Computing the annual average rainfall for the considered region
      for RegionCode in RegionCode_list:
            
            tp_av_year_region = np.array([])

            # Computing the annual average rainfall for the considered year
            TheDateTime = DateTimeS + timedelta(hours=AccPerS)
            while TheDateTime <= DateTimeF:
                  
                  print("Post-processing observations ofr period starting on ", TheDateTime)
            
                  # Reading the correspondent global observations
                  FileIN = Git_repo + "/" + DirIN + "_" + f"{Acc:02d}" + "h/" + TheDateTime.strftime("%Y%m%d") + "/tp" + f"{Acc:02d}" + "_obs_" + TheDateTime.strftime("%Y%m%d") + TheDateTime.strftime("%H") + ".geo"
                  obs = mv.read(FileIN)
                  mask_at_obs = mv.nearest_gridpoint(mask, obs)
                  obs_region = mv.values(mv.filter(obs, mask_at_obs == RegionCode))
                  tp_av_year_region = np.concatenate((tp_av_year_region, obs_region))
                  
                  TheDateTime = TheDateTime + timedelta(days=1)

            # Computing the annual rainfall average 
            tp_av_year.append(np.nanmean(tp_av_year_region))

            # Saving the plot
            DirOUT_temp= Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h"
            FileNameOUT_temp = "AverageYear_RainOBS" + f"{Acc:02d}" + "h_AccPerS_" + f"{AccPerS:02d}" + "UTC"
            if not os.path.exists(DirOUT_temp):
                  os.makedirs(DirOUT_temp)
            np.save(DirOUT_temp + "/" + FileNameOUT_temp, tp_av_year)