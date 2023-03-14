import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#####################################################################################
# CODE DESCRIPTION
# 10_Plot_AROC_CI.py plots AROC and confidence intervals (CI).

# INPUT PARAMETERS DESCRIPTION
# Acc (number, in hours): rainfall accumulation to consider.
# EFFCI_list (list of integers, from 1 to 10): list of EFFCI indexes to consider.
# MagnitudeInPerc_Rain_Event_FR_list (list of integers, from 0 to 100): list of magnitudes, in 
#     percentiles, of rainfall events that can potentially conduct to flash floods.
# CL (integer from 0 to 100, in percent): confidence level for the definition of the confidence intervals.
# Perc_VRE (integer, from 0 to 100): percentile that defines the verifying rainfall event to consider.
# RegionName_list (list of strings): list of names for the domain's regions.
# Lines_Region_list (list of strings): types of lines used to plot ROC curves for different regions. 
# SystemFC_list (list of strings): list of names of forecasting systems to consider.
# NumEM_list (list of integers): numer of ensemble members in the considered forecasting systems.
# Colour_SystemFC_list (list of strings): colours used to plot ROC curves for different forecasting systems.
# Git_repo (string): repository's local path.
# DirIN (string): relative path containing the daily probabilistic contingency tables.
# DirOUT (string): relative path of the directory containing the daily probabilistic contingency tables.

# INPUT PARAMETERS
Acc = 12
EFFCI_list = [6]
MagnitudeInPerc_Rain_Event_FR_list = [99]
CL = 95
RegionName_list = ["Costa", "Sierra"]
Lines_Region_list = ["o-", "o-"]
SystemFC_list = ["ENS", "ecPoint"]
Colour_SystemFC_list = ["magenta", "cyan"]
Git_repo="/ec/vol/ecpoint/mofp/PhD/Papers2Write/FlashFloods_Ecuador"
DirIN = "Data/Compute/08_AROC_Bootstrapping"
DirOUT = "Data/Plot/10_AROC"
#####################################################################################


# Plotting ROC curves for a specific EFFCI index
for EFFCI in EFFCI_list:
       
       # Plotting ROC curves for a specific VRE
      for MagnitudeInPerc_Rain_Event_FR in MagnitudeInPerc_Rain_Event_FR_list:

            print("Plotting AROC curves for EFFCI>=" + str(EFFCI) + ", VRE>=tp(" + str(MagnitudeInPerc_Rain_Event_FR) + "th percentile) ...") 

            # Setting the figure
            fig, ax = plt.subplots(figsize=(12, 10))

            # Plotting AROC for a specific region
            for indRegion in range(len(RegionName_list)): 

                  # Selecting the region to plot, and its correspondent line type in the plot
                  RegionName = RegionName_list[indRegion]
                  Lines_Region = Lines_Region_list[indRegion]
                  
                  # Plotting AROC for a specific forecasting system
                  for indSystemFC in range(len(SystemFC_list)):
                        
                        # Selecting the forecasting system to plot, and its correspondent colour in the plot
                        SystemFC = SystemFC_list[indSystemFC]
                        Colour_SystemFC = Colour_SystemFC_list[indSystemFC]

                        # Reading the steps computed, and the original and bootstrapped AROC values
                        DirIN_temp= Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h"
                        FileNameIN_temp = "AROC_" + f"{Acc:02d}" + "h_VRE" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "_" + SystemFC + "_EFFCI" + f"{EFFCI:02d}" + "_" + RegionName + ".npy"
                        StepF = np.load(DirIN_temp + "/" + FileNameIN_temp)[:,0].astype(int)
                        aroc_real = np.load(DirIN_temp + "/" + FileNameIN_temp)[:,1]
                        aroc_BS = np.load(DirIN_temp + "/" + FileNameIN_temp)[:,2:]

                        # Computing the confidence intervals from the bootstrapped AROC values
                        alpha = 100 - CL # significance level (in %)
                        CI_lower = np.percentile(aroc_BS, alpha/2, axis=1)
                        CI_upper = np.percentile(aroc_BS, 100 - (alpha/2), axis=1)

                        # Plotting the ROC curves
                        ax.plot(StepF, aroc_real, Lines_Region, color=Colour_SystemFC, label=SystemFC + " - " + RegionName, linewidth=2)
                        ax.fill_between(StepF, CI_lower, CI_upper, color=Colour_SystemFC, alpha=0.2, edgecolor="none")
                  
                  # Setting the plot metadata
                  ax.plot([StepF[0], StepF[-1]], [0.5, 0.5], "-", color="grey", linewidth=2)
                  DiscStep = ((StepF[-1] - StepF[0]) / (len(StepF)-1))
                  ax.set_title("Area Under the ROC curve\n" + r"EFFCI>=" + str(EFFCI) + " - VRE>=tp(" + str(MagnitudeInPerc_Rain_Event_FR) + "th percentile), Region=" +  RegionName, fontsize=20, pad=20)
                  ax.set_xlabel("Step ad the end of the " + str(Acc) + "-hourly accumulation period [hours]", fontsize=18, labelpad=10)
                  ax.set_ylabel("AROC [-]", fontsize=18, labelpad=10)
                  ax.set_xlim([StepF[0]-1, StepF[-1]+1])
                  ax.set_ylim([0.4,1])
                  ax.set_xticks(np.arange(StepF[0], (StepF[-1]+1), DiscStep))
                  ax.set_yticks(np.arange(0.4,1.1, 0.1))
                  ax.xaxis.set_tick_params(labelsize=16, rotation=90)
                  ax.yaxis.set_tick_params(labelsize=16)
                  ax.legend(loc="lower right", fontsize=16)
                  ax.grid()
                  plt.show()
                  exit()