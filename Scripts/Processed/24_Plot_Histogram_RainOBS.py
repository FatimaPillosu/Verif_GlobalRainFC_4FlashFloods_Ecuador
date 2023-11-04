import os
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

######################################################################################
# CODE DESCRIPTION
# 24_Plot_Histogram_RainOBS.py plots the histogram for rainfall observations in a considered period.
# Note: runtime code negligible.

# INPUT PARAMETERS DESCRIPTION
# Acc (number, in hours): rainfall accumulation to consider.
# DateTimeS (date, in format YYYYMMDD): start date of the considered verification period.
# DateTimeF (date, in format YYYYMMDD): final date of the considered verification period.
# AccPerF_list (list of integer, inUTC hours): list of the final times of the accumulation periods to consider.
# SystemFC_list (list of strings): list of forecasting systems to consider.
# RegionName_list (list of strings): list of names for the domain's regions.
# Git_repo (string): repository's local path.
# DirIN_FC (string): relative path containing the annual rainfall average from forecasts.
# DirIN_OBS (string): relative path containing the annual rainfall average from observations.
# DirOUT (string): relative path of the plots containing the annual rainfall average.

# INPUT PARAMETERS
Acc = 12
DateTimeS = datetime(2020,1,1,0)
DateTimeF = datetime(2020,12,31,0)
AccPerF_list = [12,0]
RegionName_list = ["Costa", "Sierra"]
RegionColour_list = ["#ffea00", "#c19a6b"]
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
DirIN = "Data/Compute/20_AverageYear_RainOBS"
DirOUT = "Data/Plot/24_Histogram_RainOBS"
######################################################################################

# Plot the timeserie of the rainfall observations for a specific accumulation period
for AccPerF in AccPerF_list:

      # Plot the timeserie of the values of the rainfall observations for a specific region
      for ind_Region in range(len(RegionName_list)):

            RegionName = RegionName_list[ind_Region]
            RegionColour = RegionColour_list[ind_Region]
            
            # Setting the figure where to plot the timeseries
            fig, ax = plt.subplots(figsize=(15, 12), sharex=True)

            # Reading the values of the rainfall observations
            FileIN = Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h/vals_obs_" + f"{Acc:02d}" + "h_" + RegionName + "_" + f"{AccPerF:02d}" + "UTC.npy"
            vals_obs = np.load(FileIN)

            # Plot the timeseries
            ax.hist(vals_obs, bins=np.arange(0, int(np.max(vals_obs)+10)), color=RegionColour, edgecolor='black')
            ax.set_title("Rainfall observations for accumulation periods ending at " + f"{AccPerF:02d}" + " UTC in " + RegionName + "\nObservations between " + DateTimeS.strftime("%Y%m%d") + " and " + DateTimeF.strftime("%Y%m%d"), fontsize=24, pad=10, color="#333333", weight="bold")
            ax.set_xlabel("Bins [mm/" + str(Acc) + "h]", fontsize=24, labelpad=20, color="#333333")
            ax.set_ylabel("Counts", fontsize=24, labelpad=24, color="#333333")
            ax.set_xticks(np.arange(0, int(np.max(vals_obs)+10), 10))
            ax.set_ylim([0,70])
            ax.xaxis.set_tick_params(labelsize=24, rotation=30, color="#333333")
            ax.yaxis.set_tick_params(labelsize=24, color="#333333")
            ax.grid()
            
            # Saving the plot
            DirOUT_temp= Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h"
            FileNameOUT_temp = "Histogram_RainOBS_" + f"{Acc:02d}" + "h_" + RegionName  + "_" + f"{AccPerF:02d}" + "UTC.jpeg"
            if not os.path.exists(DirOUT_temp):
                  os.makedirs(DirOUT_temp)
            plt.savefig(DirOUT_temp + "/" + FileNameOUT_temp)
            plt.close()