import os
from datetime import datetime, timedelta
from  random import choices
import numpy as np
import metview as mv

#############################################################################################
# CODE DESCRIPTION
# 15_Compute_Obs_Rain_Climate.py computes the observational rainfall climatology for
# each region in the domain of interest. 
# Code runtime: it can take up to 45 minutes to run in serial if the observations need to be read for the first time.

# INPUT PARAMETERS DESCRIPTION
# Acc (number, in hours): rainfall accumulation to consider.
# DateS (date, in format YYYYMMDD): start day of the period to consider.
# DateF (date, in format YYYYMMDD): final day of the period to consider.
# AccPerF_list (list of integers): list of the final times of the accumulation periods to consider.
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
AccPerF_list = [12,0]
RegionName_list = ["Costa", "Sierra"]
RegionCode_list = [1,2]
RepetitionsBS = 10000
Perc_list = np.concatenate((np.arange(1,100), np.array([99.5,99.8,99.9]))) # up to ~ 1 event in 3 years
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
FileIN_Mask = "Data/Raw/Ecuador_Mask_ENS/Mask.grib"
DirIN = "Data/Raw/OBS/Rain"
DirOUT = "Data/Compute/15_Obs_Rain_Climate"
#############################################################################################


# Creating the output directory
DirOUT_temp= Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h"
if not os.path.exists(DirOUT_temp):
      os.makedirs(DirOUT_temp)

# Reading the mask for the regions in the considered domain
mask = mv.read(Git_repo + "/" + FileIN_Mask)

# Computing the observational rainfall climatology
for in_Region in range(len(RegionName_list)):

      # Select the region to consider for the computation of the observational rainfall climatology
      RegionName = RegionName_list[in_Region]
      RegionCode = RegionCode_list[in_Region]

      print("Computing the rainfall calimatology from rainfall observations for " + RegionName)

      # Initializing the variable that will contain the original/bootstrapped percentiles
      obs_clim = np.empty([len(Perc_list),RepetitionsBS+1]) * np.nan

      # Reading the rainfall realizations from the observations
      FileNameOUT_RainOBS_vals = "Obs_Rain_Vals_" + f"{Acc:02d}" + "h_" + DateS.strftime("%Y%m%d") + "_" + DateF.strftime("%Y%m%d") + "_" + RegionName
      FileNameOUT_RainOBS_lats = "Obs_Rain_Lats_" + f"{Acc:02d}" + "h_" + DateS.strftime("%Y%m%d") + "_" + DateF.strftime("%Y%m%d") + "_" + RegionName
      FileNameOUT_RainOBS_lons = "Obs_Rain_Lons_" + f"{Acc:02d}" + "h_" + DateS.strftime("%Y%m%d") + "_" + DateF.strftime("%Y%m%d") + "_" + RegionName
      if not os.path.exists(DirOUT_temp + "/" + FileNameOUT_RainOBS_vals + ".npy") and not os.path.exists(DirOUT_temp + "/" + FileNameOUT_RainOBS_lats + ".npy") and not os.path.exists(DirOUT_temp + "/" + FileNameOUT_RainOBS_lons + ".npy"): # if the files exist already, the while loop is not necessary and it is skipped
            
            # Initializing the variable that will contain the rainfall realizations
            vals_obs = np.array([])
            lats_obs = np.array([])
            lons_obs = np.array([])

            TheDate = DateS
            while TheDate <= DateF:
                  
                  for AccPerF in AccPerF_list:
                        
                        print(" - Reading observations for accumulation period ending on " + TheDate.strftime("%Y%m%d") + " at " + f"{AccPerF:02d}")

                        # Reading the rainfall observations
                        FileIN = Git_repo + "/" + DirIN + "_" + f"{Acc:0d}" + "h/" + TheDate.strftime("%Y%m%d") + "/tp" + f"{Acc:02d}" + "_obs_" + TheDate.strftime("%Y%m%d") + f"{AccPerF:02d}" + ".geo"
                        vals_obs_global = mv.read(FileIN)

                        # Extracting the observations for the region to consider
                        mask_obs = mv.nearest_gridpoint (mask,vals_obs_global)
                        vals_obs_region = mv.values(mv.filter(vals_obs_global, mask_obs == RegionCode))
                        lats_obs_region = mv.latitudes(mv.filter(vals_obs_global, mask_obs == RegionCode))
                        lons_obs_region = mv.longitudes(mv.filter(vals_obs_global, mask_obs == RegionCode))

                        if vals_obs_region is not None:
                              vals_obs = np.concatenate((vals_obs, vals_obs_region))
                              lats_obs = np.concatenate((lats_obs, lats_obs_region))
                              lons_obs = np.concatenate((lons_obs, lons_obs_region))

                  TheDate += timedelta(days=1)
      
            # Saving the rainfall observation realizations
            np.save(DirOUT_temp + "/" + FileNameOUT_RainOBS_vals, vals_obs)
            np.save(DirOUT_temp + "/" + FileNameOUT_RainOBS_lats, lats_obs)
            np.save(DirOUT_temp + "/" + FileNameOUT_RainOBS_lons, lons_obs)

      else:
            
            print(" - Reading the file containing all " + str(Acc) + "-hourly observations ending at " + str(AccPerF_list[0]) + " and " + str(AccPerF_list[-1])  +" UTC between " + DateS.strftime("%Y%m%d") + " and " + DateF.strftime("%Y%m%d"))
            vals_obs = np.load(DirOUT_temp + "/" + FileName_RainOBS + ".npy")

      # Computing the percentiles for the original observations
      print("Computing the original percentiles")
      obs_clim[:,0] = np.percentile(vals_obs, Perc_list)

      # Computing the percentiles for the bootstrapped observations
      print("Computing the bootstrapped percentiles")
      for ind_BS in range(1,RepetitionsBS+1):
            vals_obs_BS = np.array(choices(population=vals_obs, k=vals_obs.shape[0])) # list of bootstrapped obs
            obs_clim[:,ind_BS] = np.percentile(vals_obs_BS, Perc_list)

      # Saving the plot
      FileNameOUT_ClimOBS = "Obs_Rain_Climate_" + f"{Acc:02d}" + "h_" + DateS.strftime("%Y%m%d") + "_" + DateF.strftime("%Y%m%d") + "_" + RegionName
      FileNameOUT_Percs = "Percs_computed_" + f"{Acc:02d}" + "h_" + DateS.strftime("%Y%m%d") + "_" + DateF.strftime("%Y%m%d")
      np.save(DirOUT_temp + "/" + FileNameOUT_ClimOBS, obs_clim)
      np.save(DirOUT_temp + "/" + FileNameOUT_Percs, Perc_list)