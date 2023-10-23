import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv

###################################################################################
# CODE DESCRIPTION
# 19_Compute_AverageYear_RainFC.py computes the annual average rain for different accumulation 
# periods and different lead times.
# Note: It can take up to 24 hours to run is series.

# INPUT PARAMETERS DESCRIPTION
# Acc (number, in hours): rainfall accumulation to consider.
# DateS (date, in format YYYYMMDD): start day of the period to consider.
# DateF (date, in format YYYYMMDD): final day of the period to consider.
# AccPerS_list (list of integers): list of the start times of the accumulation periods to consider.
# BaseTime (integer, in UTC hours): base time to consider for the forecasts.
# StepF_S (integer, in hours): lead time indicating the end of the first accumulation period to consider.
# StepF_F (integer, in hours): lead time indicating the end of the last accumulation period to consider.
# Disc_StepF (integer, in hours): discretization between accumulation periods
# RegionName_list (list of strings): list of names for the domain's regions.
# RegionCode_list (list of integers): codes for the domain's regions to consider. 
# FileIN_Mask (string): relative path of the file containing the domain's mask.
# Git_repo (string): repository's local path.
# DirIN (string): relative path containing the raw rainfall forecasts.
# DirOUT (string): relative path for the plots containing annual average of rainfall from forecasts.

# INPUT PARAMETERS
Acc = 12
DateS = datetime(2020,1,1,0)
DateF = datetime(2020,12,31,0)
AccPerS_list = [0,12]
LT_S = 1
LT_F = 10
Disc_StepF = 12
SystemFC_list = ["ENS", "ecPoint"]
RegionName_list = ["La Costa", "La Sierra"]
RegionCode_list = [1,2]
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
FileIN_Mask = "Data/Raw/Ecuador_Mask_ENS/Mask.grib"
DirIN = "Data/Raw/FC"
DirOUT = "Data/Compute/19_AverageYear_RainFC"
###################################################################################

# Reading the Mask for the regions in the considered domain
mask = mv.values(mv.read(Git_repo + "/" + FileIN_Mask))

# Computing the average rainfall within a period, per region
for LT_day in np.arange(LT_S,LT_F+1):

      for AccPerS in AccPerS_list:

            for SystemFC in SystemFC_list:

                  print("Computing the annual average for " + SystemFC + ", for LT = " + str(LT_day) + " day, and for accumulation period starting at " + str(AccPerS) + " UTC")
                        
                  ind_Date = 0
                  TheDate = DateS
                  while TheDate <= DateF:
                        
                        print("Post-Processing date: " , TheDate)
                        
                        # Defining the forecasts to consider
                        VT_S = TheDate + timedelta(hours = (AccPerS))
                        VT_F = TheDate + timedelta(hours = (AccPerS + Acc))
                        BaseDateTime = VT_F - timedelta(hours= (AccPerS + Acc) + ((int(LT_day) -1)*24))
                        Step2 = int((VT_F - BaseDateTime).total_seconds() / 3600)
                        Step1 = int(Step2 - Acc)
                        
                        # Creating the annual rainfall averages
                        NumDays = (DateF-DateS).days + 1
                        NumRegions = len(RegionName_list)
                        tp_av_year = np.empty((NumDays, NumRegions)) * np.nan
                  
                        # Reading the forecasts
                        if SystemFC == "ENS":
                              FileIN1 =  Git_repo + "/" + DirIN + "/" + SystemFC + "/" + BaseDateTime.strftime("%Y%m%d%H")  + "/tp_" + BaseDateTime.strftime("%Y%m%d") + "_" + BaseDateTime.strftime("%H") + "_" + f"{Step1:03d}" + ".grib"
                              FileIN2 =  Git_repo + "/" + DirIN + "/" + SystemFC + "/" + BaseDateTime.strftime("%Y%m%d%H")  + "/tp_" + BaseDateTime.strftime("%Y%m%d") + "_" + BaseDateTime.strftime("%H") + "_" + f"{Step2:03d}" + ".grib"
                              if os.path.isfile(FileIN1) and os.path.isfile(FileIN2):
                                    tp = mv.values((mv.read(FileIN2) - mv.read(FileIN1)) * 1000)
                        if SystemFC == "ecPoint":
                              FileIN =  Git_repo + "/" + DirIN + "/" + SystemFC + "/" + BaseDateTime.strftime("%Y%m%d%H")  + "/Pt_BC_PERC_" + f"{Acc:03d}"+ "_" + BaseDateTime.strftime("%Y%m%d") + "_" + BaseDateTime.strftime("%H") + "_" + f"{Step2:03d}" + ".grib"
                              if os.path.isfile(FileIN):
                                    tp = mv.values(mv.read(FileIN))

                        if len(tp) != 0:
                        
                              for ind_Region in range(NumRegions):
                                    RegionName = RegionName_list[ind_Region]
                                    RegionCode = RegionCode_list[ind_Region]
                                    ind_mask_region = np.where(mask == RegionCode)[0]
                                    tp_av_year[ind_Date, ind_Region] = np.mean(tp[:,ind_mask_region])
                  
                        ind_Date = ind_Date + 1

                        TheDate += timedelta(days=1)

                  # Creating the annual rainfall average
                  tp_av_year = np.nanmean(tp_av_year, axis=0)
                  
                  # Saving the plot
                  DirOUT_temp= Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h"
                  FileNameOUT_temp = "AverageYear_RainFC" + f"{Acc:02d}" + "h_AccPerS_" + f"{AccPerS:02d}" + "UTC_LT" + f"{LT_day:02d}" + "day_" + SystemFC
                  if not os.path.exists(DirOUT_temp):
                        os.makedirs(DirOUT_temp)
                  np.save(DirOUT_temp + "/" + FileNameOUT_temp, tp_av_year)