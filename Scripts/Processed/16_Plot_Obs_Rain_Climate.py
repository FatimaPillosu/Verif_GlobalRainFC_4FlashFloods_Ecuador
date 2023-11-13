import os
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

############################################################################
# CODE DESCRIPTION
# 16_Plot_Obs_Rain_Climate.py plots the observational rainfall climatology for each region
# in the domain of interest. 
# Code runtime: negligible.

# INPUT PARAMETERS DESCRIPTION
# Acc (number, in hours): rainfall accumulation to consider.
# DateS (date, in format YYYYMMDD): start day of the period to consider.
# DateF (date, in format YYYYMMDD): final day of the period to consider.
# CL (integer from 0 to 100, in percent): confidence level for the definition of the confidence intervals.
# RegionName_list (list of strings): list of names for the domain's regions.
# Git_repo (string): repository's local path.
# DirIN (string): relative path containing the rainfall observations.
# DirOUT (string): relative path where the observational rainfall climatologies will be stored.

# INPUT PARAMETERS
Acc = 12
DateS = datetime(2010,1,1,0)
DateF = datetime(2019,12,31,0)
CL = 95
RegionName_list = ["Costa", "Sierra"]
RegionColour_list = ["#ffea00", "#c19a6b"]
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
DirIN = "Data/Compute/15_Obs_Rain_Climate"
DirOUT = "Data/Plot/16_Obs_Rain_Climate"
############################################################################

# Plotting the observational rainfall climatologies for all considered regions
for ind_Region in range(len(RegionName_list)):

      RegionName = RegionName_list[ind_Region]
      RegionColour = RegionColour_list[ind_Region]

      # Reading the observational rainfall climatologies
      DirIN_temp = Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h"
      FileIN_percs = "Percs_computed_"+ f"{Acc:02d}" + "h_" + DateS.strftime("%Y%m%d") + "_" + DateF.strftime("%Y%m%d") + ".npy"
      FileIN_rain_climate = "Obs_Rain_Climate_" + f"{Acc:02d}" + "h_" + DateS.strftime("%Y%m%d") + "_" + DateF.strftime("%Y%m%d") + "_" + RegionName + ".npy"
      percs = np.load(DirIN_temp + "/" + FileIN_percs)
      rain_climate_original = np.load(DirIN_temp + "/" + FileIN_rain_climate)[:,0]
      rain_climate_BS = np.load(DirIN_temp + "/" + FileIN_rain_climate)[:,1:]

      # Computing the confidence intervals from the bootstrapped rainfall values
      alpha = 100 - CL # significance level (in %)
      CI_lower = np.nanpercentile(rain_climate_BS, alpha/2, axis=1)
      CI_upper = np.nanpercentile(rain_climate_BS, 100 - (alpha/2), axis=1)
      
      # Plotting the observational rainfall climatologies
      fig, ax = plt.subplots(figsize=(8, 8))
      ax.fill_betweenx(percs, CI_lower, CI_upper, color=RegionColour, alpha=0.3)
      ax.plot(rain_climate_original, percs, "-o", color=RegionColour, linewidth=2, markersize=5, markerfacecolor=RegionColour, markeredgecolor='black', markeredgewidth=0.5)

      # Completing the plot
      ax.set_title("Observational rainfall climatology (" + DateS.strftime("%Y%-m-%d") + " to " + DateF.strftime("%Y-%m-%d") + ")\n Region=" + RegionName + ", CL = " + str(CL) + "%", fontsize=16, pad=10, weight="bold", color="#333333")
      ax.set_xlabel("Rainfall [mm/" + str(Acc) + "h]", fontsize=16, labelpad=10, color="#333333")
      ax.set_ylabel("Percentiles [-]", fontsize=16, labelpad=10, color="#333333")
      ax.set_xlim([0,int(CI_upper[-1])+1])
      ax.set_ylim([80,101])
      ax.set_xticks(range(0, int(CI_upper[-1])+1, 5))
      ax.set_yticks((np.concatenate((np.arange(80,100,5), np.array([99,100])))).tolist())
      ax.xaxis.set_tick_params(labelsize=14, rotation=45, color="#333333")
      ax.yaxis.set_tick_params(labelsize=14, color="#333333")
      ax.grid()

      # Saving the plot
      DirOUT_temp = Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h"
      FileNameOUT_temp = "Obs_Rain_Climate_" + f"{Acc:02d}" + "h_" + RegionName + ".png"
      if not os.path.exists(DirOUT_temp):
            os.makedirs(DirOUT_temp)
      plt.savefig(DirOUT_temp + "/" + FileNameOUT_temp)
      plt.close()