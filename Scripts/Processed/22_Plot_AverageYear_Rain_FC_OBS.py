import os
import numpy as np
import matplotlib.pyplot as plt

##################################################################################
# CODE DESCRIPTION
# 22_Plot_AverageYear_Rain_FC_OBS.py plots the annual average rain for different accumulation 
# periods.
# Note: runtime code negligible.

# INPUT PARAMETERS DESCRIPTION
# Acc (number, in hours): rainfall accumulation to consider.
# AccPerF_list (list of integer, inUTC hours): list of the final times of accumulation periods to consider.
# StepF_S (integer, in hours): lead time indicating the end of the first accumulation period to consider.
# StepF_F (integer, in hours): lead time indicating the end of the last accumulation period to consider.
# Disc_StepF (integer, in hours): discretization between accumulation periods.
# SystemFC_list (list of strings): list of forecasting systems to consider.
# Colour_SystemFC_list (list of strings): colours used to plot the FB for different forecasting systems.
# RegionName_list (list of strings): list of names for the domain's regions.
# RegionPlot_list (list of strings): list of line types to use when plotting the different regions.
# Git_repo (string): repository's local path.
# DirIN_FC (string): relative path containing the annual rainfall average from forecasts.
# DirIN_OBS (string): relative path containing the annual rainfall average from observations.
# DirOUT (string): relative path of the plots containing the annual rainfall average.

# INPUT PARAMETERS
Acc = 12
AccPerF_list = [12,0]
StepF_S = 12
StepF_F = 240
Disc_StepF = 12
SystemFC_list = ["ENS", "ecPoint"]
Colour_SystemFC_list = ["#ec4d37", "#00539CFF"]
RegionName_list = ["Costa", "Sierra"]
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
DirIN_FC = "Data/Compute/19_AverageYear_RainFC"
DirIN_OBS = "Data/Compute/21_AverageYear_RainOBS"
DirOUT = "Data/Plot/22_AverageYear_Rain_FC_OBS"
##################################################################################


# Setting some general variables
Num_StepF = np.arange(StepF_S, StepF_F+1, Disc_StepF).shape[0]
Num_AccPerF = len(AccPerF_list)
Num_Region = len(RegionName_list)
Num_SystemFC = len(SystemFC_list)

# Plotting the annual rainfall average for a specific region
for ind_Region in range(Num_Region):

      RegionName = RegionName_list[ind_Region]

      # Setting the figure where to plot the counts
      fig, ax = plt.subplots(figsize=(25, 16), sharex=True)

      # Preparing the variable containing the annual rainfall average from observations and plotting it
      FileIN_OBS= Git_repo + "/" + DirIN_OBS + "/" + f"{Acc:02d}" + "h/AverageYear_RainOBS_" + f"{Acc:02d}" + "h_" + RegionName + ".npy"
      tp_av_year_obs = np.load(FileIN_OBS)
      tp_av_year_obs_allLT = np.vstack([tp_av_year_obs] * int((Num_StepF/Num_AccPerF)))
      ax.plot(np.arange(StepF_S, StepF_F+1, Disc_StepF), tp_av_year_obs_allLT[:,1], "o-", color="grey", label="OBS", linewidth=4, markersize=10)

      # Creating the trend line and plotting it
      coefficients = np.polyfit(tp_av_year_obs_allLT[:,0], tp_av_year_obs_allLT[:,1], 0)
      polynomial = np.poly1d(coefficients)
      y_trend = polynomial(tp_av_year_obs_allLT[:,0])
      ax.plot(np.arange(StepF_S, StepF_F+1, Disc_StepF), y_trend, "--", color="grey", linewidth=2)
      
      # Plotting the annual rainfall average for a specific forecasting system
      for ind_SystemFC in range(Num_SystemFC):

            SystemFC = SystemFC_list[ind_SystemFC]
            Colour_SystemFC = Colour_SystemFC_list[ind_SystemFC]

            # Reading the annual rainfall average from forecasts
            FileIN_FC = Git_repo + "/" + DirIN_FC + "/" + f"{Acc:02d}" + "h/AverageYear_RainFC_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + RegionName + ".npy"
            tp_av_year_FC = np.load(FileIN_FC)
            
            # Plotting the annual rainfall average from forecasts and observations
            ax.plot(tp_av_year_FC[:,0], tp_av_year_FC[:,1], "o-", color=Colour_SystemFC, label=SystemFC, linewidth=4, markersize=10)

            # Creating the trend line and plotting it
            coefficients = np.polyfit(tp_av_year_FC[:,0], tp_av_year_FC[:,1], 0)
            polynomial = np.poly1d(coefficients)
            y_trend = polynomial(tp_av_year_FC[:,0])
            ax.plot(np.arange(StepF_S, StepF_F+1, Disc_StepF), y_trend, "--", color=Colour_SystemFC, linewidth=2)
            
      # Completing the plot
      xtick_labels = []
      for i in range(Num_StepF):
            xtick_labels.append("t+" + str(int(tp_av_year_FC[i,0])) + "\n" + f"{int(tp_av_year_obs_allLT[i,0]):02d}" + " UTC")
      ax.set_title("Annual rainfall average from forecasts and observations, " + RegionName, fontsize=24, pad=40, color="#333333", weight="bold")
      ax.set_xlabel("Step ad the end of the " + str(Acc) + "-hourly accumulation periods [hours], and correspondent valid time [UTC]", fontsize=24, labelpad=20, color="#333333")
      ax.set_ylabel("Annual rainfall average [mm/" + str(Acc) + "h]", fontsize=24, labelpad=20, color="#333333")
      ax.set_xlim([tp_av_year_FC[0,0]-1, tp_av_year_FC[-1,0]+1])
      ax.set_xticks(tp_av_year_FC[:,0].astype(int))
      ax.set_xticklabels(xtick_labels)
      ax.xaxis.set_tick_params(labelsize=20, rotation=90, color="#333333")
      ax.yaxis.set_tick_params(labelsize=24, color="#333333")
      ax.legend(loc="upper center",  bbox_to_anchor=(0.5, 1.05), ncol=3, fontsize=20, frameon=False)
      ax.grid()

      # Saving the plot
      DirOUT_temp= Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h"
      FileNameOUT_temp = "AverageYear_Rain_FC_OBS_" + f"{Acc:02d}" + "h_" + RegionName + ".jpeg"
      if not os.path.exists(DirOUT_temp):
            os.makedirs(DirOUT_temp)
      plt.savefig(DirOUT_temp + "/" + FileNameOUT_temp)
      plt.close()