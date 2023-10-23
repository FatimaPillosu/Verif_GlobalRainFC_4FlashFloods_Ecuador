import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv
import matplotlib.pyplot as plt

#####################################################################################################################
# CODE DESCRIPTION
# 20_Plot_Count_NumRainOBS_AccPer.py plots the counts of rain observations in each considered accumulation period. 
# Note: runtime code negligible.

# INPUT PARAMETERS DESCRIPTION
# Acc (number, in hours): rainfall accumulation to consider.
# DateS (date, in format YYYYMMDD): start date of the considered verification period.
# DateF (date, in format YYYYMMDD): final date of the considered verification period.
# AccPerS_list (list of integer, inUTC hours): list of the start times of the accumulation periods to consider.
# CornersDomain_list (list of floats): coordinates [N/E/S/W] of the domain to plot.
# RegionName_list (list of strings): list of names for the domain's regions.
# RegionCode_list (list of integers): codes for the domain's regions to consider. 
# FileIN_Mask (string): relative path of the file containing the domain's mask.
# Git_repo (string): repository's local path.
# DirIN (string): relative path containing the raw rainfall observations.
# DirOUT (string): relative path of the plots containing the observations counts.

# INPUT PARAMETERS
Acc = 12
DateS = datetime(2020,1,1,0)
DateF = datetime(2020,12,31,0)
AccPerS_list = [0,12]
CornersDomain_list = [2,-81.5,-5.5,-74.5]
RegionName_list = ["La Costa", "La Sierra"]
RegionCode_list = [1,2]
FileIN_Mask = "Data/Raw/Ecuador_Mask_ENS/Mask.grib"
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
DirIN = "Data/Raw/OBS/Rain"
DirOUT = "Data/Plot/20_Count_NumRainOBS_AccPer"
#####################################################################################################################

# Setting some general parameters and variables
NumDays = (DateF-DateS).days + 1
Num_AccPerS = len(AccPerS_list)
Num_Regions = len(RegionName_list)
av_rain_region = np.empty((NumDays, Num_AccPerS, Num_Regions))

# Reading the Mask for the regions in the considered domain
mask = mv.read(Git_repo + "/" + FileIN_Mask)

# Computing the average rainfall within a period, per region
ind_Date = 0
TheDate = DateS
Num_Instances = 0
while TheDate <= DateF:
            
      for ind_AccPerS in range(Num_AccPerS):

            AccPerS = AccPerS_list[ind_AccPerS]
            TheDateTime = TheDate + timedelta(hours=AccPerS)
            print(TheDateTime)

            # Reading the observations
            FileIN = Git_repo + "/" + DirIN + "_" + f"{Acc:02d}" + "h/" + TheDateTime.strftime("%Y%m%d") + "/tp" + f"{Acc:02d}" + "_obs_" + TheDateTime.strftime("%Y%m%d") + TheDateTime.strftime("%H") + ".geo"
            obs = mv.read(FileIN)

            # Extracting the observations that are within the considered domain
            ind_obs_domain = mv.mask(obs, CornersDomain_list)
            obs_domain = mv.filter(obs, ind_obs_domain>=1)

            # Extracting the observations for the different regions in the considered domain
            obs_AllRegions = mv.nearest_gridpoint(mask, obs_domain)
            for ind_RegionCode in range(Num_Regions):
                  RegionCode = RegionCode_list[ind_RegionCode]
                  temp = mv.mean(mv.filter(obs_domain, obs_AllRegions==RegionCode))
                  if temp != None:
                        av_rain_region[ind_Date, ind_AccPerS, ind_RegionCode] = temp
                  else:
                        av_rain_region[ind_Date, ind_AccPerS, ind_RegionCode] = np.nan

      ind_Date = ind_Date + 1
      
      TheDate += timedelta(days=1)

# Defining average number of observations per day in each region
average = np.nanmean(av_rain_region, axis=0)
print(average)

