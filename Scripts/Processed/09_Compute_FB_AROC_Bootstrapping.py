import os
from datetime import datetime, timedelta
from  random import choices
import numpy as np
import pandas as pd

####################################################################################################
# CODE DESCRIPTION
# 09_Compute_FB_AROC_Bootstrapping.py computes frequency bias (FB) and area under the ROC curves (AROC), 
# including the bootstrapped values to estimate the statistical significance of FB and AROC.

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
StepF_Final = 246
Disc_Step = 6
Acc = 12
EFFCI_list = [1,6,10]
MagnitudeInPerc_Rain_Event_FR_list = [85,99]
RepetitionsBS = 10000
RegionName_list = ["Costa", "Sierra"]
SystemFC_list = ["ENS", "ecPoint"]
NumEM_list = [51,99]
Git_repo="/ec/vol/ecpoint/mofp/PhD/Papers2Write/FlashFloods_Ecuador"
DirIN = "Data/Compute/07_Daily_Prob_Contingency_Tables"
DirOUT_FB = "Data/Compute/09_FB_Bootstrapping"
DirOUT_AROC = "Data/Compute/09_AROC_Bootstrapping"
####################################################################################################

# COSTUME FUNCTIONS

###############################
# Computation of the frequency bias #
###############################
def FreqBias(ct):
      FB = ( ct[:,0] + ct[:,1] ) / (ct[:,0] + ct[:,2])
      return FB

#######################################################################
# Computation of the area under the ROC curve, using the trapezoidal approximation  #
#######################################################################
def AROC_trapezoidal(ct):
      
      # Computing hit rates (hr) and false alarm rates (far). The arrays are reversed for a more intuitive reading of the elements.
      hr = np.flipud( ct[:,0] / (ct[:,0] + ct[:,2]) )# hit rates (reverse the order of the elements 
      far = np.flipud( ct[:,1] / (ct[:,1] + ct[:,3]) ) # false alarms (reverse the order of the elements for a more intuitive reading of the meaining of the element)
      
      # Adding the points (0,0) and (1,1) to the arrays to ensure the ROC curve is complete.
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

np.set_printoptions(suppress=True, formatter={'float_kind':'{:0.2f}'.format}) 

print(" ")
print("Computing FB and AROC, including " + str(RepetitionsBS) + " bootstrapped values")

# Creating the list containing the dates considered in the computations
original_dates_list = []
for x in range(((DateF+timedelta(days=1))-DateS).days):
      original_dates_list.append(DateS+timedelta(days=x))

# Creating the list containing the steps to considered in the computations
StepF_list = range(StepF_Start, (StepF_Final+1), Disc_Step)

# Initializing the variables containing the sizes of the FB and AROC variables
m = len(StepF_list)
n = len(range(RepetitionsBS + 1))

# Computing FB and AROC for a specific forecasting system
for indSystemFC in range(len(SystemFC_list)):
      
      # Selecting the forecasting system to consider and its number of ensemble members 
      SystemFC = SystemFC_list[indSystemFC]
      NumEM = NumEM_list[indSystemFC]

      # Computing FB and AROC for a specific region
      for indRegion in range(len(RegionName_list)): 

            # Selecting the region to consider
            RegionName = RegionName_list[indRegion]

            # Computing FB and AROC for a specific EFFCI index
            for EFFCI in EFFCI_list:
                  
                  # Computing FB and AROC for a specific VRE
                  for MagnitudeInPerc_Rain_Event_FR in MagnitudeInPerc_Rain_Event_FR_list:

                        print(" - For " + SystemFC + ", " + RegionName + ", EFFCI>=" + str(EFFCI) + ", VRE>=tp(" + str(MagnitudeInPerc_Rain_Event_FR) + "th percentile)")

                        # Initializing the variables containing the FB and AROC values, and the bootstrapped ones
                        FB_array = np.empty([m,n+2,NumEM+1])
                        AROC_array = np.empty([m,n+1])

                        # Computing FB and AROC for a specific lead time
                        for indStepF in range(len(StepF_list)):
                              
                              # Selecting the StepF to consider
                              StepF = StepF_list[indStepF]
                              print("     - Considering StepF=" + str(StepF) + " ...")

                              # Storing information about the step computed
                              FB_array[indStepF, 0,:] = StepF
                              AROC_array[indStepF, 0] = StepF

                              # Creating the list of dates to considered from the boostrapping technique
                              for indBS in range(RepetitionsBS+1):
                                    
                                    # Establishing whether to consider the original dates or the bootstrapped ones
                                    if indBS == 0:
                                          datesBS_list = original_dates_list
                                    if indBS > 0:
                                          datesBS_list = choices(population=original_dates_list, k=len(original_dates_list)) # it picks random values from the list with replacement
                                    
                                    # Reading the daily probabilistic contingency tables for the defined list of dates, and adding them together
                                    ct_tot = np.zeros((NumEM+1,4), dtype=int)
                                    for TheDate in datesBS_list:
                                          DirIN_temp = Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h/VRE" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "/" + SystemFC + "/EFFCI" + f"{EFFCI:02d}" + "/" + TheDate.strftime("%Y%m%d%H")
                                          FileNameIN_temp = "CT_" + f"{Acc:02d}" + "h_VRE" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "_" + SystemFC + "_EFFCI" + f"{EFFCI:02d}" + "_" + TheDate.strftime("%Y%m%d") + "_" + TheDate.strftime("%H") + "_" + f"{StepF:03d}" + "_" + RegionName + ".csv"
                                          if os.path.isfile(DirIN_temp + "/" + FileNameIN_temp):
                                                ct_daily = pd.read_csv(DirIN_temp + "/" + FileNameIN_temp).to_numpy()[:,1:]
                                                ct_tot = ct_tot + ct_daily

                                    # Computing and saving FB
                                    FB = FreqBias(ct_tot)
                                    FB_array[indStepF, indBS+2,:] = FB

                                    # Computing and saving AROC
                                    AROC = AROC_trapezoidal(ct_tot)
                                    AROC_array[indStepF, indBS+1] = AROC
                        
                        # Storing information about the probability thresholds considered
                        ProbThr = pd.read_csv(DirIN_temp + "/" + FileNameIN_temp).to_numpy()[:,0]
                        FB_array[indStepF, 1,:] = ProbThr
                        
                        # Saving the FB array
                        DirOUT_temp= Git_repo + "/" + DirOUT_FB + "/" + f"{Acc:02d}" + "h"
                        FileNameOUT_temp = "FB_" + f"{Acc:02d}" + "h_VRE" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "_" + SystemFC + "_EFFCI" + f"{EFFCI:02d}" + "_" + RegionName + ".csv"
                        if not os.path.exists(DirOUT_temp):
                              os.makedirs(DirOUT_temp)
                        np.save(DirOUT_temp + "/" + FileNameOUT_temp, FB_array)

                        # Saving the AROC array
                        DirOUT_temp= Git_repo + "/" + DirOUT_AROC + "/" + f"{Acc:02d}" + "h"
                        FileNameOUT_temp = "AROC_" + f"{Acc:02d}" + "h_VRE" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "_" + SystemFC + "_EFFCI" + f"{EFFCI:02d}" + "_" + RegionName + ".csv"
                        if not os.path.exists(DirOUT_temp):
                              os.makedirs(DirOUT_temp)
                        np.save(DirOUT_temp + "/" + FileNameOUT_temp, AROC_array)