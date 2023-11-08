import os
import numpy as np
import matplotlib.pyplot as plt

#####################################################################################
# CODE DESCRIPTION
# 25_Plot_FB_CI.py plots Frequency Bias (FB) and confidence intervals (CI).
# Note: runtime negligible.

# INPUT PARAMETERS DESCRIPTION
# Acc (number, in hours): rainfall accumulation to consider.
# StepF_2_Plot_list (list of integers, in hours): list of final steps of the accumulation periods to consider.
# EFFCI_list (list of integers, from 1 to 10): list of EFFCI indexes to consider.
# MagnitudeInPerc_Rain_Event_FR_list (list of integers, from 0 to 100): list of magnitudes, in 
#     percentiles, of rainfall events that can potentially conduct to flash floods.
# CL (integer from 0 to 100, in percent): confidence level for the definition of the confidence intervals.
# Perc_VRT (integer, from 0 to 100): percentile that defines the verifying rainfall event to consider.
# RegionName_list (list of strings): list of names for the domain's regions.
# SystemFC_list (list of strings): list of names of forecasting systems to consider.
# Colour_SystemFC_list (list of strings): colours used to plot the FB for different forecasting systems.
# Git_repo (string): repository's local path.
# DirIN (string): relative path containing the real and boostrapped FB values.
# DirOUT (string): relative path of the directory containing the plots of the real and boostrapped FB values.

# INPUT PARAMETERS
Acc = 12
EFFCI_list = [1,6,10]
MagnitudeInPerc_Rain_Event_FR_list = [85,99]
CL = 95
RegionName_list = ["Costa","Sierra"]
SystemFC_list = ["ENS", "ecPoint"]
Colour_SystemFC_list = ["#ec4d37", "#00539CFF"]
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
DirIN = "Data/Compute/24_FB_Bootstrapping"
DirOUT = "Data/Plot/25_FB_CI"
#####################################################################################


# Plotting FB for a specific EFFCI index
for EFFCI in EFFCI_list:
       
      # Plotting FB for a specific VRT
      for MagnitudeInPerc_Rain_Event_FR in MagnitudeInPerc_Rain_Event_FR_list:

            print("Plotting FB values for EFFCI>=" + str(EFFCI) + ", VRT>=tp(" + str(MagnitudeInPerc_Rain_Event_FR) + "th percentile) ...") 

            # Plotting FB for a specific region
            for RegionName in RegionName_list: 
                  
                  # Setting the figure
                  fig, ax = plt.subplots(figsize=(14, 10))

                  # Plotting FB for a specific forecasting system
                  for indSystemFC in range(len(SystemFC_list)):
                        
                        # Selecting the forecasting system to plot, and its correspondent colour in the plot
                        SystemFC = SystemFC_list[indSystemFC]
                        Colour_SystemFC = Colour_SystemFC_list[indSystemFC]

                        # Reading the steps computed, and the original and bootstrapped FB values
                        DirIN_temp= Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h"
                        FileNameIN_temp = "FB_" + f"{Acc:02d}" + "h_VRT" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "_" + SystemFC + "_EFFCI" + f"{EFFCI:02d}" + "_" + RegionName + ".npy"
                        StepF = np.load(DirIN_temp + "/" + FileNameIN_temp)[:,0].astype(int)
                        fb_real = np.load(DirIN_temp + "/" + FileNameIN_temp)[:,1]
                        fb_BS = np.load(DirIN_temp + "/" + FileNameIN_temp)[:,2:]
                        
                        # Computing the confidence intervals from the bootstrapped FB values
                        alpha = 100 - CL # significance level (in %)
                        CI_lower = np.nanpercentile(fb_BS, alpha/2, axis=1)
                        CI_upper = np.nanpercentile(fb_BS, 100 - (alpha/2), axis=1)
                        
                        # Plotting the FB values
                        ax.plot(StepF, fb_real, "o-", color=Colour_SystemFC, label=SystemFC, linewidth=3)
                        ax.fill_between(StepF, CI_lower, CI_upper, color=Colour_SystemFC, alpha=0.2, edgecolor="none")
                  
                  # Setting the plot metadata
                  DiscStep = ((StepF[-1] - StepF[0]) / (len(StepF)-1))
                  ax.set_title("Frequency Bias\n" + "EFFCI>=" + str(EFFCI) + ", VRT>=tp(" + str(MagnitudeInPerc_Rain_Event_FR) + "th percentile), Region=" +  RegionName + ", CL=" + str(CL) + "%", fontsize=20, pad=40, color="#333333", weight="bold")
                  ax.set_xlabel("Step ad the end of the " + str(Acc) + "-hourly accumulation period [hours]", fontsize=20, labelpad=10, color="#333333")
                  ax.set_ylabel("Frequency Bias [-]", fontsize=20, labelpad=10, color="#333333")
                  ax.set_xlim([StepF[0]-1, StepF[-1]+1])
                  ax.set_xticks(np.arange(StepF[0], (StepF[-1]+1), DiscStep))
                  ax.xaxis.set_tick_params(labelsize=20, rotation=90, color="#333333")
                  ax.yaxis.set_tick_params(labelsize=16, color="#333333")
                  ax.legend(loc="upper center",  bbox_to_anchor=(0.5, 1.08), ncol=2, fontsize=20, frameon=False)
                  ax.grid()
                  
                  # Saving the plot
                  DirOUT_temp= Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h"
                  FileNameOUT_temp = "FB_" + f"{Acc:02d}" + "h_VRT" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "_EFFCI" + f"{EFFCI:02d}" + "_" + RegionName  + ".jpeg"
                  if not os.path.exists(DirOUT_temp):
                        os.makedirs(DirOUT_temp)
                  plt.savefig(DirOUT_temp + "/" + FileNameOUT_temp)