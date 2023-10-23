import os
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt

############################################################################
# CODE DESCRIPTION
# 08_Plot_Obs_Rain_Climate.py plots the observational rainfall climatology for each region
# in the domain of interest. 
# Code runtime: negligible.

# INPUT PARAMETERS DESCRIPTION
# Acc (number, in hours): rainfall accumulation to consider.
# DateS (date, in format YYYYMMDD): start day of the period to consider.
# DateF (date, in format YYYYMMDD): final day of the period to consider.
# RegionName_list (list of strings): list of names for the domain's regions.
# Git_repo (string): repository's local path.
# DirIN (string): relative path containing the rainfall observations.
# DirOUT (string): relative path where the observational rainfall climatologies will be stored.

# INPUT PARAMETERS
Acc = 12
DateS = datetime(2010,1,1,0)
DateF = datetime(2019,12,31,0)
RegionName_list = ["Costa", "Sierra"]
RegionColour_list = ["#ffea00", "#c19a6b"]
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
DirIN = "Data/Compute/07_Obs_Rain_Climate"
DirOUT = "Data/Plot/08_Obs_Rain_Climate"
############################################################################


# Setting the figure where to plot the observational rainfall climatologies
fig, ax = plt.subplots(figsize=(10, 9))

# Plotting the observational rainfall climatologies for all considered regions
for ind_Region in range(len(RegionName_list)):

      RegionName = RegionName_list[ind_Region]
      RegionColour = RegionColour_list[ind_Region]

      # Reading the observational rainfall climatologies
      DirIN_temp = Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h"
      FileIN_percs = "Percs_computed_" + DateS.strftime("%Y%m%d") + "_" + DateF.strftime("%Y%m%d") + ".npy"
      FileIN_rain_climate = "Obs_Rain_Climate_" + f"{Acc:02d}" + "h_" + DateS.strftime("%Y%m%d") + "_" + DateF.strftime("%Y%m%d") + "_" + RegionName + ".npy"
      percs = np.load(DirIN_temp + "/" + FileIN_percs)
      rain_climate = np.load(DirIN_temp + "/" + FileIN_rain_climate)

      # Plotting the observational rainfall climatologies
      ax.plot(rain_climate, percs, "-o", color=RegionColour, linewidth=4, markersize=8, label=RegionName)
      
# Completing the plot
ax.set_title("Observational rainfall climatology", fontsize=20, pad=30, weight="bold", color="#333333")
ax.set_xlabel("Rainfall [mm/" + str(Acc) + "h]", fontsize=20, labelpad=10, color="#333333")
ax.set_ylabel("Percentiles [-]", fontsize=20, labelpad=10, color="#333333")
ax.set_xlim([0,110])
ax.set_ylim([70,101])
ax.set_xticks(range(0, 111, 5))
ax.set_yticks((np.concatenate((np.arange(70,100,5), np.array([99,100])))).tolist())
ax.xaxis.set_tick_params(labelsize=20, rotation=90, color="#333333")
ax.yaxis.set_tick_params(labelsize=20, color="#333333")
ax.legend(loc="upper center",  bbox_to_anchor=(0.5, 1.08), ncol=7, fontsize=20, frameon=False)
ax.grid()

# Saving the plot
DirOUT_temp = Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h"
FileNameOUT_temp = "Obs_Rain_Climate_" + f"{Acc:02d}" + ".png"
if not os.path.exists(DirOUT_temp):
      os.makedirs(DirOUT_temp)
plt.savefig(DirOUT_temp + "/" + FileNameOUT_temp)