import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv

###################################################################################
# CODE DESCRIPTION
# 22_Compute_AverageYear_RainFC_gridbox.py computes the annual average rain for different  
# accumulation periods and different lead times, per grid-box.
# Note: It can take up to 24 hours to run is series.

# INPUT PARAMETERS DESCRIPTION
# Acc (number, in hours): rainfall accumulation to consider.
# BaseDateTimeS (date, in format YYYYMMDDHH): start base date and time of the period to consider.
# BaseDateTimeF (date, in format YYYYMMDDHH): final base date and time of the period to consider.
# StepF_S (integer, in hours): lead time indicating the end of the first accumulation period to consider.
# StepF_F (integer, in hours): lead time indicating the end of the last accumulation period to consider.
# Disc_StepF (integer, in hours): discretization between accumulation periods.
# SystemFC_list (list of strings): list of forecasting systems to consider.
# Git_repo (string): repository's local path.
# FileIN_Mask (string): relative path of the file containing the domain's mask.
# DirIN (string): relative path containing the raw rainfall forecasts.
# DirOUT (string): relative path for the plots containing annual average of rainfall from forecasts.

# INPUT PARAMETERS
Acc = 12
BaseDateTimeS = datetime(2020,1,1,0)
BaseDateTimeF = datetime(2020,12,31,0)
StepF_S = 60
StepF_F = 72
Disc_StepF = 12
SystemFC_list = ["ENS", "ecPoint"]
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
FileIN_Mask = "Data/Raw/Ecuador_Mask_ENS/Mask.grib"
DirIN = "Data/Raw/FC"
DirOUT = "Data/Compute/22_AverageYear_RainFC_gridbox"
###################################################################################

# Creating the variable that stores the lead times to consider
StepF_list = np.arange(StepF_S,StepF_F+1, Disc_StepF)
Num_StepF = StepF_list.shape[0]

# Computing the annual rainfall average for a specific forecasting system
for SystemFC in SystemFC_list:

      # Initializing the variables that will contain the annual rainfall averages
      tp_av_year = None
      
      # Computing the annual rainfall average for a specific lead time
      for ind_StepF in range(Num_StepF):
            
            StepF = StepF_list[ind_StepF]
            StepS = StepF - Acc

            # Computing the annual rainfall average for all dates
            tp_av_year_temp = None
            BaseDateTime = BaseDateTimeS
            while BaseDateTime <= BaseDateTimeF:
                  
                  print("Computing the annual average for " + SystemFC + ", for StepF=" + str(StepF) + ", for the run on " + BaseDateTime.strftime("%Y%m%d") + " at " + BaseDateTime.strftime("%H") + " UTC")
                              
                  # Reading the forecasts
                  if SystemFC == "ENS":
                        FileIN1 =  Git_repo + "/" + DirIN + "/" + SystemFC + "/" + BaseDateTime.strftime("%Y%m%d%H")  + "/tp_" + BaseDateTime.strftime("%Y%m%d") + "_" + BaseDateTime.strftime("%H") + "_" + f"{StepS:03d}" + ".grib"
                        FileIN2 =  Git_repo + "/" + DirIN + "/" + SystemFC + "/" + BaseDateTime.strftime("%Y%m%d%H")  + "/tp_" + BaseDateTime.strftime("%Y%m%d") + "_" + BaseDateTime.strftime("%H") + "_" + f"{StepF:03d}" + ".grib"
                        if os.path.isfile(FileIN1) and os.path.isfile(FileIN2):
                              tp = (mv.read(FileIN2) - mv.read(FileIN1)) * 1000
                  if SystemFC == "ecPoint":
                        FileIN =  Git_repo + "/" + DirIN + "/" + SystemFC + "/" + BaseDateTime.strftime("%Y%m%d%H")  + "/Pt_BC_PERC_" + f"{Acc:03d}"+ "_" + BaseDateTime.strftime("%Y%m%d") + "_" + BaseDateTime.strftime("%H") + "_" + f"{StepF:03d}" + ".grib"
                        if os.path.isfile(FileIN):
                              tp = mv.read(FileIN)

                  # Extracting the forecasts for a specific region
                  if len(tp) != 0:
                        NumEM = int(mv.count(tp))
                        tp_av_year_temp = mv.merge(tp_av_year_temp, (mv.sum(tp))/NumEM)

                  BaseDateTime += timedelta(days=1)

            # Computing the annual rainfall average
            NumRealizations = int(mv.count(tp_av_year_temp))
            tp_av_year = (mv.sum(tp_av_year_temp))/NumRealizations
            
            # Saving the plot
            DirOUT_temp= Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h" 
            FileNameOUT_temp = "AverageYear_RainFC_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + f"{StepF:03d}" + ".grib"
            if not os.path.exists(DirOUT_temp):
                  os.makedirs(DirOUT_temp)
            mv.write(DirOUT_temp + "/" + FileNameOUT_temp, tp_av_year)