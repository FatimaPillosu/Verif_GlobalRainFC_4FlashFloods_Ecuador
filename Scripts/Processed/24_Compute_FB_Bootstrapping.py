import os
from datetime import datetime, timedelta
from  random import choices
import numpy as np

######################################################################################
# CODE DESCRIPTION
# 24_Compute_FB_Bootstrapping.py computes the Frequency Bias (FB), including the bootstrapped 
# values to estimate the statistical significance of the estimates.
# Note: the code can take up to 2 hours to run.

# INPUT PARAMETERS DESCRIPTION
# DateS (date, in format YYYYMMDD): start date of the considered verification period.
# DateF (date, in format YYYYMMDD): final date of the considered verification period.
# StepF_Start (integer, in hours): first final step of the accumulation periods to consider.
# StepF_Final (integer, in hours): last final step of the accumulation periods to consider.
# Disc_Step (integer, in hours): discretization for the final steps to consider.
# Acc (number, in hours): rainfall accumulation to consider.
# EFFCI_list (list of integers, from 1 to 10): list of EFFCI indexes to consider.
# MagnitudeInPerc_Rain_Event_FR_list (list of integers, from 0 to 100): list of magnitudes, in 
#     percentiles, of rainfall events that can potentially conduct to flash floods.
# RepetitionsBS (integer, from 0 to infinite): number of repetitions to consider in the bootstrapping.
# RegionName_list (list of strings): list of names for the domain's regions.
# SystemFC_list (list of strings): list of names of forecasting systems to consider.
# NumEM_list (list of integers): numer of ensemble members in the considered forecasting systems.
# Git_repo (string): repository's local path.
# DirIN (string): relative path containing the daily probabilistic contingency tables.
# DirOUT (string): relative path of the directory containing the FB values, including the bootstrapped ones.

# INPUT PARAMETERS
DateS = datetime(2020,1,1,0)
DateF = datetime(2020,12,31,0)
StepF_Start = 12
StepF_Final = 246
Disc_Step = 6
Acc = 12
EFFCI_list = [1,6,10]
MagnitudeInPerc_Rain_Event_FR_list = [85,99]
RepetitionsBS = 10000
RegionName_list = ["Costa","Sierra"]
SystemFC_list = ["ENS", "ecPoint"]
NumEM_list = [51,99]
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
DirIN = "Data/Compute/23_Counts_FC_OBS_Exceeding_VRT"
DirOUT_FB = "Data/Compute/24_FB_Bootstrapping"
######################################################################################


print(" ")
print("Computing FB, including " + str(RepetitionsBS) + " bootstrapped values")

# Sorting the dates to consider in the bootstrapping
NumDays = (DateF-DateS).days + 1
Dates_Orig = np.array([DateS + timedelta(days=i) for i in range(NumDays)])
Dates_BS = (np.array([choices(population=Dates_Orig, k=NumDays) for i in range(RepetitionsBS)])).flatten()
temp = {value: index for index, value in enumerate(Dates_Orig)}
ind_Dates_BS = (np.array([temp[elem] for elem in Dates_BS])).reshape(RepetitionsBS,NumDays)

# Creating the list containing the steps to considered in the computations
StepF_list = range(StepF_Start, (StepF_Final+1), Disc_Step)
NumStepF = len(StepF_list)

# Computing FB for a specific forecasting system
for indSystemFC in range(len(SystemFC_list)):
      
      # Selecting the forecasting system to consider and its number of ensemble members 
      SystemFC = SystemFC_list[indSystemFC]
      NumEM = NumEM_list[indSystemFC]

      # Computing FB for a specific EFFCI index
      for EFFCI in EFFCI_list:
            
            # Computing FB for a specific VRT
            for MagnitudeInPerc_Rain_Event_FR in MagnitudeInPerc_Rain_Event_FR_list:

                  # Computing FB for a specific region
                  for indRegion in range(len(RegionName_list)): 
                  
                        # Selecting the region to consider
                        RegionName = RegionName_list[indRegion]

                        print(" - For " + SystemFC + ", " + RegionName + ", EFFCI>=" + str(EFFCI) + ", VRT>=tp(" + str(MagnitudeInPerc_Rain_Event_FR) + "th percentile)")

                        # Initializing the variable that will contained the FB values
                        FB_BS = np.empty((NumStepF, RepetitionsBS + 2))

                        # Computing FB for a specific lead time
                        for indStepF in range(NumStepF):
                              
                              # Selecting the StepF to consider
                              StepF = StepF_list[indStepF]
                              FB_BS[indStepF,0] = StepF

                              print("     - Considering StepF=" + str(StepF) + " ...")

                              # Reading the counts of yes-events in the forecasts and observations for the original dates
                              count_yes_fc = np.empty(NumDays) * np.nan
                              count_yes_obs = np.empty(NumDays) * np.nan
                              for ind_Date in range(len(Dates_Orig)):
                                    TheDate = Dates_Orig[ind_Date]
                                    FileIN = Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h/EFFCI" +  f"{EFFCI:02d}" + "/VRT" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "/" + f"{StepF:03d}" + "/" + SystemFC + "/" + RegionName + "/Count_FC_OBS_" + f"{Acc:02d}" + "h_EFFCI" + f"{EFFCI:02d}" + "_VRT" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "_" + SystemFC + "_" + RegionName + "_" + TheDate.strftime("%Y%m%d") + "_" + TheDate.strftime("%H") + "_" + f"{StepF:03d}" + ".npy"
                                    if os.path.isfile(FileIN):
                                          count_yes_fc[ind_Date] = np.round(np.load(FileIN)[0]/NumEM).astype(int)
                                          count_yes_obs[ind_Date] = np.load(FileIN)[1]
                              FB_BS[indStepF,1] = np.nansum(count_yes_fc) / np.nansum(count_yes_obs)

                              # Extracting the bootstrapped values for the counts
                              for ind_BS in range(RepetitionsBS):
                                    count_yes_fc_BS = count_yes_fc[ind_Dates_BS[ind_BS,:]]
                                    count_yes_obs_BS = count_yes_obs[ind_Dates_BS[ind_BS,:]]
                                    FB_BS[indStepF,ind_BS+2] = np.nansum(count_yes_fc_BS) / np.nansum(count_yes_obs_BS)

                        # Saving the FB array
                        DirOUT_temp= Git_repo + "/" + DirOUT_FB + "/" + f"{Acc:02d}" + "h"
                        FileNameOUT_temp = "FB_" + f"{Acc:02d}" + "h_VRT" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "_" + SystemFC + "_EFFCI" + f"{EFFCI:02d}" + "_" + RegionName
                        if not os.path.exists(DirOUT_temp):
                              os.makedirs(DirOUT_temp)
                        np.save(DirOUT_temp + "/" + FileNameOUT_temp, FB_BS)