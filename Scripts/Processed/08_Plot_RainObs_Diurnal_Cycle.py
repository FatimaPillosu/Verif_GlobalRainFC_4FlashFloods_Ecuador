import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv
import matplotlib.pyplot as plt

#####################################################################
# CODE DESCRIPTION
# 08_Plot_RainObs_Diurnal_Cycle.py plots the rainfall's diurnal cycle in Ecuador. 
# Code runtime: negligible.

# INPUT PARAMETERS DESCRIPTION
# Acc (number, in hours): rainfall accumulation to consider.
# DateS (date, in format YYYYMMDD): start day of the period to consider.
# DateF (date, in format YYYYMMDD): final day of the period to consider.
# CornersDomain_list (list of floats): coordinates [N/E/S/W] of the domain to plot.
# RegionName_list (list of strings): names for the domain's regions to consider.
# RegionColour_list (list of strings): rgb-codes for the domain's regions to consider.
# Git_repo (string): repository's local path.
# DirIN (string): relative path containing the rainfall observations.
# DirOUT (string): relative path containing the plots.

# INPUT PARAMETERS
Acc = 12
DateS = datetime(2010,1,1,0)
DateF = datetime(2020,12,31,0)
AccPerF_list = [12,0]
RegionName_list = ["Costa", "Sierra", "Oriente"]
RegionColour_list = ["#ffea00", "#c19a6b", "#A9FE00"]
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
DirIN = "Data/Compute/06_Extract_RainObs_Region_AccPer"
DirOUT = "Data/Plot/08_RainObs_Diurnal_Cycle"
#####################################################################

# Starting the figure that will containg the rainfall's diurnal cycle
fig, ax = plt.subplots(figsize=(14, 8))

# Reading the rainfall observations for a specific region
for ind_Region in range(len(RegionName_list)):

      # Starting the variable that will stored the avearge rainfall at different times of the day
      rain_diurnal_cycle = np.empty(len(AccPerF_list)) * np.nan   

      # Select the region to consider for the computation of the observational rainfall climatology
      RegionName = RegionName_list[ind_Region]
      RegionColour = RegionColour_list[ind_Region]

      # Reading the rainfall observations for a specific accumulation period
      for ind_AccPerF in range(len(AccPerF_list)):
            
            AccPerF = AccPerF_list[ind_AccPerF]
            
            # Initializing the variables that will contain the  rainfall observations
            obs_vals = np.array([])

            # Reading the rainfall observations for each day of the considered time period
            TheDate = DateS
            while TheDate <= DateF:

                  print("Reading rainfall observations for " + RegionName + " for the " + f"{Acc:02d}" + "-hourly rainfall observations for the accumulation period ending on " + TheDate.strftime("%Y%m%d") + " at " +  f"{AccPerF:02d}" + " UTC") 

                  # Reading the observations
                  FileIN = Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h/" + TheDate.strftime("%Y%m%d") + "/tp" +  f"{Acc:02d}" + "_obs_" + TheDate.strftime("%Y%m%d") + f"{AccPerF:02d}" + "_" + RegionName + ".npy"
                  obs_vals = np.concatenate((obs_vals, np.load(FileIN)[2,:]))

                  TheDate += timedelta(days=1)

            # Computing the avearge rainfall for a specific accumulation period
            rain_diurnal_cycle[ind_AccPerF] = np.average(obs_vals)

      # Create the average rainfall
      av_rain_diurnal_cycle = np.average(rain_diurnal_cycle)

      # Create the variable to plot
      AccPerF_multiple = np.hstack([AccPerF_list] * 5)
      rain_diurnal_cycle_multiple = np.hstack([rain_diurnal_cycle] * 5)
      av_rain_diurnal_cycle_multiple = np.hstack([av_rain_diurnal_cycle] * len(rain_diurnal_cycle) * 5)
      
      # Plotting the distribution of the rainfall  totals
      xtick_labels = []
      for rep in range(5):
            for AccPerF in AccPerF_list:
                  xtick_labels.append(f"{AccPerF:02d}")
      x_axis = np.arange(len(rain_diurnal_cycle_multiple))
      ax.plot(x_axis, rain_diurnal_cycle_multiple, "o-", color=RegionColour, linewidth=3, label=RegionName)
      ax.plot(x_axis, av_rain_diurnal_cycle_multiple, "--", color=RegionColour, linewidth=2)
      ax.set_title("Rainfall diurnal cycle from SYNOP observations\n Averaged between " + DateS.strftime("%Y%m%d") + " and " + DateF.strftime("%Y%m%d"),  fontsize=16, pad=30, color="#333333", weight="bold")
      ax.set_xlabel("End of the " + str(Acc) + "-hourly accumulation periods [UTC]", fontsize=14, labelpad=10, color="#333333")
      ax.set_ylabel("Rainfall [mm/" + str(Acc) + "h]", fontsize=14, labelpad=10, color="#333333")
      ax.set_ylim([0,7])
      ax.set_xticks(x_axis)
      ax.set_xticklabels(xtick_labels)
      ax.xaxis.set_tick_params(labelsize=14, color="#333333")
      ax.yaxis.set_tick_params(labelsize=14, color="#333333")
      ax.legend(loc="upper center",  bbox_to_anchor=(0.5, 1.07), ncol=3, fontsize=14, frameon=False)
      ax.grid()

# Saving the distribution plot
DirOUT_temp = Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h"
if not os.path.exists(DirOUT_temp):
      os.makedirs(DirOUT_temp)
FileOUT = DirOUT_temp + "/Diurnal_Cycle_" + f"{Acc:02d}" + "h_" + DateS.strftime("%Y%m%d") + "_" + DateF.strftime("%H")
plt.savefig(FileOUT)