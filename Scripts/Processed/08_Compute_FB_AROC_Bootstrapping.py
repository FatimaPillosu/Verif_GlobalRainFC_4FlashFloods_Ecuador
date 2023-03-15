import os
from datetime import datetime, timedelta
from  random import choices
import numpy as np
import pandas as pd


####################################################################################################
# CODE DESCRIPTION
# 08_Compute_FB_AROC_Bootstrapping.py computes frequency bias (FB) and area under the ROC curves (AROC), 
# including the bootstrapped values to estimate the statistical significance of FB and AROC.
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
# DirOUT_FB (string): relative path of the directory containing the FB values, including the bootstrapped ones.
# DirOUT_AROC (string): relative path of the directory containing the AROC values, including the bootstrapped ones.

# INPUT PARAMETERS
DateS = datetime(2020,1,1,0)
DateF = datetime(2020,12,31,0)
StepF_Start = 12
StepF_Final = 18
Disc_Step = 6
Acc = 12
EFFCI_list = [1]
MagnitudeInPerc_Rain_Event_FR_list = [85]
RepetitionsBS = 10000
RegionName_list = ["Costa","Sierra"]
SystemFC_list = ["ENS", "ecPoint"]
NumEM_list = [51,99]
Git_repo="/ec/vol/ecpoint/mofp/PhD/Papers2Write/FlashFloods_Ecuador"
DirIN = "Data/Compute/07_Daily_Prob_Contingency_Tables"
DirOUT_FB = "Data/Compute/08_FB_Bootstrapping"
DirOUT_AROC = "Data/Compute/08_AROC_Bootstrapping"
####################################################################################################


# COSTUME FUNCTIONS

# Computation of the frequency bias
def FreqBias(ct):
      FB = ( ct[:,0] + ct[:,1] ) / (ct[:,0] + ct[:,2])
      return FB

# Computation of the area under the ROC curve, using the trapezoidal approximation
def AROC_trapezoidal(ct):
      
      # Computing hit rates (hr) and false alarm rates (far).
      hr = ct[:,0] / (ct[:,0] + ct[:,2]) # hit rates
      far = ct[:,1] / (ct[:,1] + ct[:,3]) # false alarms
      
      # Adding the points (0,0) and (1,1) to the arrays to ensure the ROC curve is closed.
      hr = np.insert(hr, 0, 0) 
      hr = np.insert(hr, -1, 1)
      far = np.insert(far, 0, 0) 
      far = np.insert(far, -1, 1) 
      
      # Computing the AROC with the trapezoidal approximation, and approximating its value to the second decimal digit.
      aroc = 0
      for i in range(len(hr)-1):
            j = i+1
            a = hr[i]
            b = hr[i+1]
            h = far[i+1] - far[i]
            aroc = aroc + ( ( (a+b)*h ) / 2 )
      aroc = round(aroc,2)

      return aroc
####################################################################################################


print(" ")
print("Computing FB and AROC, including " + str(RepetitionsBS) + " bootstrapped values")

# Computing the totals number of days contained in the considered verification period
NumTotDays = (DateF-DateS).days + 1

# Creating the list containing the steps to considered in the computations
StepF_list = range(StepF_Start, (StepF_Final+1), Disc_Step)

# Computing the variables containing the sizes of the FB and AROC variables
m = len(StepF_list)
n = len(range(RepetitionsBS + 1))

# Computing FB and AROC for a specific forecasting system
for indSystemFC in range(len(SystemFC_list)):
      
      # Selecting the forecasting system to consider and its number of ensemble members 
      SystemFC = SystemFC_list[indSystemFC]
      NumEM = NumEM_list[indSystemFC]

      # Computing FB and AROC for a specific EFFCI index
      for EFFCI in EFFCI_list:
            
            # Computing FB and AROC for a specific VRE
            for MagnitudeInPerc_Rain_Event_FR in MagnitudeInPerc_Rain_Event_FR_list:

                  # Computing FB and AROC for a specific region
                  for indRegion in range(len(RegionName_list)): 
                  
                        # Selecting the region to consider
                        RegionName = RegionName_list[indRegion]

                        print(" - For " + SystemFC + ", " + RegionName + ", EFFCI>=" + str(EFFCI) + ", VRE>=tp(" + str(MagnitudeInPerc_Rain_Event_FR) + "th percentile)")

                        # Initializing the variables containing the FB and AROC values, and the bootstrapped ones
                        FB_array = np.zeros([m,n+2,NumEM+1])
                        AROC_array = np.zeros([m,n+1])
            
                        # Computing FB and AROC for a specific lead time
                        for indStepF in range(len(StepF_list)):
                              
                              # Selecting the StepF to consider
                              StepF = StepF_list[indStepF]
                              print("     - Considering StepF=" + str(StepF) + " ...")

                              # Storing information about the step computed
                              FB_array[indStepF, 0,:] = StepF
                              AROC_array[indStepF, 0] = StepF

                              # Reading the daily probabilistic contingency tables for the original list of dates
                              original_datesSTR_array = [] # list of dates for which a contingency table was created (not all steps have one if the forecasts did not exist)
                              ct_AllDays_original = np.full((NumEM+1,4), np.nan) # initialize the 3d-array containing the daily contingency tables for those days in which one was computed. The variable is initialized with a 2d-array filled of NaNs, and contains the same dimensions of the daily probabilistic contingency tables 
                              TheDate = DateS
                              while TheDate <= DateF:
                                    DirIN_temp= Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h/EFFCI" + f"{EFFCI:02d}" + "/VRE" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "/" + f"{StepF:03d}" + "/" + SystemFC + "/" + RegionName
                                    FileNameIN_temp = "CT_" + f"{Acc:02d}" + "h_EFFCI" + f"{EFFCI:02d}" + "_VRE" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "_" + SystemFC + "_" + RegionName + "_" + TheDate.strftime("%Y%m%d") + "_" + TheDate.strftime("%H") + "_" + f"{StepF:03d}" + ".csv"
                                    if os.path.isfile(DirIN_temp + "/" + FileNameIN_temp): # if the files exists, add the correspondent daily probabilistic contingency table to the 3d-array
                                          original_datesSTR_array.append(TheDate.strftime("%Y%m%d"))
                                          ProbThr = pd.read_csv(DirIN_temp + "/" + FileNameIN_temp).to_numpy()[:,0]
                                          ct_daily = pd.read_csv(DirIN_temp + "/" + FileNameIN_temp).to_numpy()[:,1:]
                                          ct_AllDays_original = np.concatenate((ct_AllDays_original, ct_daily), axis=0)
                                    else: # if the file does not exist, add a 2d-array filled with NaNs to the 3d-array
                                          ct_AllDays_original = np.concatenate((ct_AllDays_original, np.full((NumEM+1,4), np.nan)), axis=0)
                                    TheDate += timedelta(days=1)
                              ct_AllDays_original = ct_AllDays_original.reshape((NumTotDays+1,(NumEM+1),4)) # reshape the long 2d-array into a 3d-array 
                              NumDays = len(original_datesSTR_array)
                              ind_nan2del = np.any(~np.isnan(ct_AllDays_original), axis=(1,2))
                              ct_AllDays_original = ct_AllDays_original[ind_nan2del] # eliminate the 2d-arrays containing only NaNs
                              
                              # Computing FB and AROC for the original and the bootstrapped probabilistic contingency tables
                              for ind_repBS in range(RepetitionsBS+1):
                                    
                                    # Selecting the original or the bootstrapped contingency tables
                                    if ind_repBS == 0: # original
                                          ct = ct_AllDays_original
                                    else: # bootstrapped
                                          datesBS_array = np.array(choices(population=original_datesSTR_array, k=NumDays)) # list of bootstrapped dates
                                          indBS = np.searchsorted(original_datesSTR_array, datesBS_array) # indexes of the bootstrapped dates
                                          ct = ct_AllDays_original[indBS,:,:] # indexing the bootstrapped daily probabilistic contingency tables
                                    
                                    # Adding the correspondent elements of the daily probabilistic contingency tables over the condisered verification period
                                    ct_tot = np.sum(ct, axis=0) #2d-array, of the same dimensions of the daily probabilistic contingency tables
                                    
                                    # Computing FB
                                    FB = FreqBias(ct_tot)
                                    FB_array[indStepF, ind_repBS+2,:] = FB

                                    # Computing AROC
                                    AROC = AROC_trapezoidal(ct_tot)
                                    AROC_array[indStepF, ind_repBS+1] = AROC
                        
                              # Storing information about the probability thresholds considered for FB
                              FB_array[indStepF, 1,:] = ProbThr
                              
                        # Saving the FB array
                        DirOUT_temp= Git_repo + "/" + DirOUT_FB + "/" + f"{Acc:02d}" + "h"
                        FileNameOUT_temp = "FB_" + f"{Acc:02d}" + "h_VRE" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "_" + SystemFC + "_EFFCI" + f"{EFFCI:02d}" + "_" + RegionName
                        if not os.path.exists(DirOUT_temp):
                              os.makedirs(DirOUT_temp)
                        np.save(DirOUT_temp + "/" + FileNameOUT_temp, FB_array)

                        # Saving the AROC array
                        DirOUT_temp= Git_repo + "/" + DirOUT_AROC + "/" + f"{Acc:02d}" + "h"
                        FileNameOUT_temp = "AROC_" + f"{Acc:02d}" + "h_VRE" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "_" + SystemFC + "_EFFCI" + f"{EFFCI:02d}" + "_" + RegionName
                        if not os.path.exists(DirOUT_temp):
                              os.makedirs(DirOUT_temp)
                        np.save(DirOUT_temp + "/" + FileNameOUT_temp, AROC_array)