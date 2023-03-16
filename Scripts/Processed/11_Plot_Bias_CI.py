import os
import numpy as np
import matplotlib.pyplot as plt

#####################################################################################
# CODE DESCRIPTION
# 11_Plot_FB_CI.py plots Frequency Bias (FB) and confidence intervals (CI).
# Note: the code can take up 20 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Acc (number, in hours): rainfall accumulation to consider.
# StepF_2_Plot_list (list of integers, in hours): list of final steps of the accumulation periods to consider.
# EFFCI_list (list of integers, from 1 to 10): list of EFFCI indexes to consider.
# MagnitudeInPerc_Rain_Event_FR_list (list of integers, from 0 to 100): list of magnitudes, in 
#     percentiles, of rainfall events that can potentially conduct to flash floods.
# CL (integer from 0 to 100, in percent): confidence level for the definition of the confidence intervals.
# Perc_VRE (integer, from 0 to 100): percentile that defines the verifying rainfall event to consider.
# RegionName_list (list of strings): list of names for the domain's regions.
# SystemFC_list (list of strings): list of names of forecasting systems to consider.
# Colour_SystemFC_list (list of strings): colours used to plot the FB for different forecasting systems.
# Git_repo (string): repository's local path.
# DirIN (string): relative path containing the real and boostrapped FB values.
# DirOUT (string): relative path of the directory containing the plots of the real and boostrapped FB values.

# INPUT PARAMETERS
Acc = 12
StepF_2_Plot_list = np.arange(12,246+1,6)
EFFCI_list = [1,6,10]
MagnitudeInPerc_Rain_Event_FR_list = [85,99]
CL = 95
RegionName_list = ["Costa","Sierra"]
SystemFC_list = ["ENS", "ecPoint"]
Colour_SystemFC_list = ["magenta", "cyan"]
Git_repo="/ec/vol/ecpoint/mofp/PhD/Papers2Write/FlashFloods_Ecuador"
DirIN = "Data/Compute/08_FB_Bootstrapping"
DirOUT = "Data/Plot/11_FB"
#####################################################################################


# Plotting FB for a specific EFFCI index
for EFFCI in EFFCI_list:
       
      # Plotting FB for a specific VRE
      for MagnitudeInPerc_Rain_Event_FR in MagnitudeInPerc_Rain_Event_FR_list:

            # Plotting FB for a specific region
            for RegionName in RegionName_list: 
                  
                  print(" ")

                  # Plotting FB for a specific StepF
                  for StepF_2_Plot in StepF_2_Plot_list:
                        
                        print("Plotting FB for EFFCI>=" + str(EFFCI) + ", VRE>=tp(" + str(MagnitudeInPerc_Rain_Event_FR) + "th percentile), for StepF=" + str(StepF_2_Plot) + ", for Region=" +  RegionName + "...") 

                        # Setting the figure
                        fig, ax = plt.subplots(figsize=(12, 10))

                        # Plotting FB for a specific forecasting system
                        for indSystemFC in range(len(SystemFC_list)):
                              
                              # Selecting the forecasting system to plot, and its correspondent colour in the plot
                              SystemFC = SystemFC_list[indSystemFC]
                              Colour_SystemFC = Colour_SystemFC_list[indSystemFC]

                              # Reading the steps and the percentiles computed, and the original and bootstrapped FB values
                              DirIN_temp= Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h"
                              FileNameIN_temp = "FB_" + f"{Acc:02d}" + "h_VRE" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "_" + SystemFC + "_EFFCI" + f"{EFFCI:02d}" + "_" + RegionName + ".npy"
                              StepF = np.load(DirIN_temp + "/" + FileNameIN_temp)[:,0].astype(int)[:,0]
                              percentiles = np.load(DirIN_temp + "/" + FileNameIN_temp)[:,1].astype(int)[0]
                              fb_real = np.load(DirIN_temp + "/" + FileNameIN_temp)[:,2]
                              fb_BS = np.load(DirIN_temp + "/" + FileNameIN_temp)[:,3:]
                        
                              # Finding the index of the StepF to plot
                              indStepF = np.where(StepF == StepF_2_Plot)[0]
                              percentiles = 100 - ( percentiles / percentiles[0] * 100 ) 
                              fb_real = fb_real[indStepF,:][0]
                              fb_BS = fb_BS[indStepF,:,:][0]

                              # Computing the confidence intervals from the bootstrapped FB values
                              alpha = 100 - CL # significance level (in %)
                              CI_lower = np.nanpercentile(fb_BS, alpha/2, axis=0)
                              CI_upper = np.nanpercentile(fb_BS, 100 - (alpha/2), axis=0)

                              # Plotting the FB values
                              ax.plot(percentiles, fb_real, "o-", color=Colour_SystemFC, label=SystemFC, linewidth=2)
                              ax.fill_between(percentiles, CI_lower, CI_upper, color=Colour_SystemFC, alpha=0.2, edgecolor="none")
                        
                        # Setting the plot metadata
                        ax.set_title("Frequency Bias\n" + r"EFFCI>=" + str(EFFCI) + " - VRE>=tp(" + str(MagnitudeInPerc_Rain_Event_FR) + "th percentile), Region=" +  RegionName + ", CL=" + str(CL) + "%", fontsize=20, pad=20)
                        ax.set_xlabel("Percentiles [-]", fontsize=18, labelpad=10)
                        ax.set_ylabel("Frequency Bias [-]", fontsize=18, labelpad=10)
                        ax.set_xlim([-1,101])
                        ax.set_ylim([0, np.max(CI_upper)+100])
                        ax.set_xticks(np.arange(0,101,5))
                        ax.set_yticks(np.arange(0,max(CI_upper)+100, 1000))
                        ax.xaxis.set_tick_params(labelsize=16)
                        ax.yaxis.set_tick_params(labelsize=16, rotation=90)
                        ax.legend(loc="upper left", fontsize=16)
                        ax.grid()
                        
                        # Saving the plot
                        DirOUT_temp= Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h/VRE" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "/EFFCI" + f"{EFFCI:02d}"  + "/" + RegionName
                        FileNameOUT_temp = "FB_" + f"{Acc:02d}" + "h_VRE" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "_EFFCI" + f"{EFFCI:02d}" + "_" + RegionName + "_" +  f"{StepF_2_Plot:03d}" + ".jpeg"
                        if not os.path.exists(DirOUT_temp):
                              os.makedirs(DirOUT_temp)
                        plt.savefig(DirOUT_temp + "/" + FileNameOUT_temp)
                        
                        # Setting the plot metadata
                        ax.plot([-1,101], [1, 1], "-", color="grey", linewidth=2)
                        ax.set_title("Frequency Bias\n" + "StepF=" + f"{StepF_2_Plot:03d}" + r", EFFCI>=" + str(EFFCI) + ", VRE>=tp(" + str(MagnitudeInPerc_Rain_Event_FR) + "th percentile), Region=" +  RegionName + ", CL=" + str(CL) + "%", fontsize=20, pad=20)
                        ax.set_xlabel("Percentiles [-]", fontsize=18, labelpad=10)
                        ax.set_ylabel("Frequency Bias [-]", fontsize=18, labelpad=10)
                        ax.set_xlim([-1,101])
                        ax.set_ylim([0, 10])
                        ax.set_xticks(np.arange(0,101,5))
                        ax.set_yticks(np.arange(0,11))
                        ax.xaxis.set_tick_params(labelsize=16)
                        ax.yaxis.set_tick_params(labelsize=16)
                        ax.legend(loc="upper right", fontsize=16)
                        
                        # Saving the plot
                        FileNameOUT_temp = "ZoomedFB_" + f"{Acc:02d}" + "h_VRE" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "_EFFCI" + f"{EFFCI:02d}" + "_" + RegionName + "_" +  f"{StepF_2_Plot:03d}" + ".jpeg"
                        plt.savefig(DirOUT_temp + "/" + FileNameOUT_temp)
                        plt.close() 