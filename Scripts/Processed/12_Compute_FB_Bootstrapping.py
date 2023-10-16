import os
from datetime import datetime, timedelta
from  random import choices
import numpy as np
import pandas as pd


####################################################################################################
# CODE DESCRIPTION
# 10_Compute_FB_Bootstrapping.py computes the Frequency Bias (FB), including the bootstrapped values to estimate the 
# statistical significance of the estimates.
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
RepetitionsBS = 0
RegionName_list = ["Costa","Sierra"]
SystemFC_list = ["ENS", "ecPoint"]
NumEM_list = [51,99]
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
DirIN = "Data/Compute/08_Counts_FC_OBS_Exceeding_VRE"
DirOUT_FB = "Data/Compute/10_FB_Bootstrapping"
####################################################################################################


print(" ")
print("Computing FB, including " + str(RepetitionsBS) + " bootstrapped values")

# Computing the totals number of days contained in the considered verification period
NumTotDays = (DateF-DateS).days + 1

# Creating the list containing the steps to considered in the computations
StepF_list = range(StepF_Start, (StepF_Final+1), Disc_Step)

# Computing the variables containing the sizes of the FC variables
m = len(StepF_list)
n = len(range(RepetitionsBS + 1))

# Computing FB for a specific forecasting system
for indSystemFC in range(len(SystemFC_list)):
      
      # Selecting the forecasting system to consider and its number of ensemble members 
      SystemFC = SystemFC_list[indSystemFC]
      NumEM = NumEM_list[indSystemFC]

      # Computing FB for a specific EFFCI index
      for EFFCI in EFFCI_list:
            
            # Computing FB for a specific VRE
            for MagnitudeInPerc_Rain_Event_FR in MagnitudeInPerc_Rain_Event_FR_list:

                  # Computing FB for a specific region
                  for indRegion in range(len(RegionName_list)): 
                  
                        # Selecting the region to consider
                        RegionName = RegionName_list[indRegion]

                        print(" - For " + SystemFC + ", " + RegionName + ", EFFCI>=" + str(EFFCI) + ", VRE>=tp(" + str(MagnitudeInPerc_Rain_Event_FR) + "th percentile)")

                        # Initializing the variables containing the FB values, and the bootstrapped ones
                        FB_array = np.zeros([m,n+1])
            
                        # Computing FB for a specific lead time
                        for indStepF in range(len(StepF_list)):
                              
                              # Selecting the StepF to consider
                              StepF = StepF_list[indStepF]
                              print("     - Considering StepF=" + str(StepF) + " ...")

                              # Storing information about the step computed
                              FB_array[indStepF, 0] = StepF

                              # Generating the list of days to use during the bootstrapping 
                              TheDate = DateS
                              TheDates_original = []
                              while TheDate <= DateF:
                                    TheDates_original.append(TheDate)
                                    TheDate += timedelta(days=1)
                              TheDates_original = np.array(TheDates_original)
                              
                              # Computing FB for the original and the bootstrapped dates
                              for ind_repBS in range(RepetitionsBS+1):
                                   
                                   # Selecting the list of dates to consider
                                    if ind_repBS == 0: # selecting the original dates
                                          TheDates_BS = TheDates_original
                                    else: # selecting the bootstrapped dates
                                          TheDates_BS = np.array(choices(population=TheDates_original, k=NumTotDays)) # list of bootstrapped dates

                                    # Computing the FB for the selected dates
                                    tot_count_fc_exceed_vre = 0
                                    tot_count_obs_exceed_vre = 0
                                    for TheDate_BS in TheDates_BS:
                                          FileIN = Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h/EFFCI" +  f"{EFFCI:02d}" + "/VRE" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "/" + f"{StepF:03d}" + "/" + SystemFC + "/" + RegionName + "/Count_FC_OBS_" + f"{Acc:02d}" + "h_EFFCI" + f"{EFFCI:02d}" + "_VRE" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "_" + SystemFC + "_" + RegionName + "_" + TheDate_BS.strftime("%Y%m%d") + "_" + TheDate_BS.strftime("%H") + "_" + f"{StepF:03d}" + ".csv.npy"
                                          tot_count_fc_exceed_vre = tot_count_fc_exceed_vre + np.load(FileIN)[0]
                                          tot_count_obs_exceed_vre = tot_count_obs_exceed_vre  + np.load(FileIN)[1]
                                          
                                    # Computing FB
                                    if tot_count_obs_exceed_vre != 0:
                                          tempFB = tot_count_fc_exceed_vre / (NumEM * tot_count_obs_exceed_vre)
                                    else:
                                          tempFB = tot_count_fc_exceed_vre / NumEM # the proportion of ensemble members that incorrectly predicted the event is computed to avoid diving by zero
                                    FB_array[indStepF, ind_repBS+1] = tempFB
                                    
                                    print("     tot_count_fc_exceed_vre=", str(tot_count_fc_exceed_vre), "; tot_count_obs_exceed_vre=", str(tot_count_obs_exceed_vre))
                        
                        
                        print(FB_array)
                        exit()
                        # Saving the FB array
                        DirOUT_temp= Git_repo + "/" + DirOUT_FB + "/" + f"{Acc:02d}" + "h"
                        FileNameOUT_temp = "FB_" + f"{Acc:02d}" + "h_VRE" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "_" + SystemFC + "_EFFCI" + f"{EFFCI:02d}" + "_" + RegionName
                        if not os.path.exists(DirOUT_temp):
                              os.makedirs(DirOUT_temp)
                        np.save(DirOUT_temp + "/" + FileNameOUT_temp, FB_array)