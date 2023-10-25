import os
import numpy as np
import matplotlib.pyplot as plt

######################################################################################
# CODE DESCRIPTION
# 21_Plot_AverageYear_Rain_FC_OBS.py plots the annual average rain for different accumulation 
# periods.
# Note: runtime code negligible.

# INPUT PARAMETERS DESCRIPTION
# Acc (number, in hours): rainfall accumulation to consider.
# DateS (date, in format YYYYMMDD): start date of the considered verification period.
# DateF (date, in format YYYYMMDD): final date of the considered verification period.
# AccPerS_list (list of integer, inUTC hours): list of the start times of the accumulation periods to consider.
# RegionName_list (list of strings): list of names for the domain's regions.
# RegionCode_list (list of integers): codes for the domain's regions to consider. 
# Git_repo (string): repository's local path.
#
# DirIN (string): relative path containing the raw rainfall observations.
# DirOUT (string): relative path of the plots containing the annual average rain.

# INPUT PARAMETERS
Acc = 12
AccPerS_list = [0,12]
LT_S = 1
LT_F = 10
SystemFC_list = ["ENS", "ecPoint"]
Colour_SystemFC_list = ["#ec4d37", "#00539CFF"]
RegionName_list = ["La Costa", "La Sierra"]
RegionPlot_list = ["o-", "o--"]
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
DirIN_FC = "Data/Compute/19_AverageYear_RainFC"
DirIN_OBS = "Data/Compute/20_AverageYear_RainOBS"
DirOUT = "Data/Compute/21_AverageYear_Rain_FC_OBS"
######################################################################################

# Setting the figure where to plot the counts
fig, ax = plt.subplots(figsize=(12, 8), sharex=True)
x = np.arange(0,(LT_F*len(AccPerS_list)))

# Plotting the annual rainfall average from observations
for ind_Region in range(len(RegionName_list)):
      RegionName = RegionName_list[ind_Region]
      RegionPlot = RegionPlot_list[ind_Region]
      av_year_obs_region = []
      for LT in range(LT_S, LT_F+1):
            for AccPerS in AccPerS_list:
                  FileIN_OBS = Git_repo + "/" + DirIN_OBS + "/" + f"{Acc:02d}" + "h/AverageYear_RainOBS_" + f"{Acc:02d}" + "h_AccPerS_" + f"{AccPerS:02d}" + "UTC.npy"
                  av_year_obs = np.load(FileIN_OBS)
                  av_year_obs_region.append(av_year_obs[0])
      ax.plot(x, av_year_obs_region, RegionPlot, color="grey", label="OBS - " + RegionName , linewidth=2)

# Plotting the annual rainfall average from forecasts
for ind_Region in range(len(RegionName_list)):
      RegionName = RegionName_list[ind_Region]
      RegionPlot = RegionPlot_list[ind_Region]
      for ind_SystemFC in range(len(SystemFC_list)):
            SystemFC = SystemFC_list[ind_SystemFC]
            Colour_SystemFC = Colour_SystemFC_list[ind_SystemFC]
            av_year_fc_region = []
            for LT in range(LT_S, LT_F+1):
                  for AccPerS in AccPerS_list:
                        FileIN_FC = Git_repo + "/" + DirIN_FC + "/" + f"{Acc:02d}" + "h/AverageYear_RainFC_" + f"{Acc:02d}" + "h_AccPerS_" + f"{AccPerS:02d}" + "UTC_LT" + f"{LT:02d}" + "day_" + SystemFC + ".npy"
                        av_year_fc = np.load(FileIN_FC)
                        av_year_fc_region.append(av_year_fc[0])
            ax.plot(x, av_year_fc_region, RegionPlot, color=Colour_SystemFC, label=SystemFC + " - " + RegionName , linewidth=2)

plt.show()