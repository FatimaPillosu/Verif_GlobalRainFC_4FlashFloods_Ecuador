import os
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator

#####################################################################################################################
# CODE DESCRIPTION
# 26_Plot_Count_YesFC_YesOBS.py plots the counts of yes forecast and observation events.
# Note: runtime code negligible.

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
# Colour_SystemFC_list (list of strings): colours used to plot the counts of yes forecasts and observation events for different forecasting systems.
# NumEM_list (list of integers): numer of ensemble members in the considered forecasting systems.
# Git_repo (string): repository's local path.
# DirIN (string): relative path containing the daily probabilistic contingency tables.
# DirOUT (string): relative path of the directory containing the FB values, including the bootstrapped ones.

# INPUT PARAMETERS
Acc = 12
DateS = datetime(2020,1,1,0)
DateF = datetime(2020,12,31,0)
StepF_2_Plot = 72
EFFCI = 6
Max_Count_Plot_yaxis = 40
MagnitudeInPerc_Rain_Event_FR_list = [85,99]
RegionName_list = ["Costa", "Sierra"]
SystemFC_list = ["ENS", "ecPoint"]
NumEM_list = [51, 99]
Colour_SystemFC_list = ["#ec4d37", "#00539CFF"]
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
DirIN = "Data/Compute/23_Counts_FC_OBS_Exceeding_VRT"
DirOUT = "Data/Plot/26_Count_YesFC_YesOBS"
#####################################################################################################################


# Plotting the counts for a specific VRT
for MagnitudeInPerc_Rain_Event_FR in MagnitudeInPerc_Rain_Event_FR_list:

      # Plotting the counts for a specific region
      for indRegion in range(len(RegionName_list)): 
      
            RegionName = RegionName_list[indRegion]
            print(" - Plot the count of yes forecasts and observation events for  " + RegionName + ", EFFCI>=" + str(EFFCI) + ", VRT>=tp(" + str(MagnitudeInPerc_Rain_Event_FR) + "th percentile), StepF=" + str(StepF_2_Plot))
    
            # Setting the figure where to plot the counts
            fig, ax1 = plt.subplots(figsize=(12, 8), sharex=True)

            # Initializing the variable that contains the maximum count in the forecasts
            max_count_yes_fc_list = []
                  
            # Plotting the counts for a specific forecasting system
            for indSystemFC in range(len(SystemFC_list)):
                        
                  SystemFC = SystemFC_list[indSystemFC]
                  Colour_SystemFC = Colour_SystemFC_list[indSystemFC]
                  NumEM = NumEM_list[indSystemFC]

                  # Initializing the variables containing the considered dates, and the correspondent forecasts and observations counts
                  count_yes_fc = []
                  count_yes_obs = []
                  TheDates_list = []

                  # Reading the counts for the selected dates
                  TheDate = DateS
                  while TheDate <= DateF:
                        TheDates_list.append(TheDate)
                        FileIN = Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h/EFFCI" +  f"{EFFCI:02d}" + "/VRT" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "/" + f"{StepF_2_Plot:03d}" + "/" + SystemFC + "/" + RegionName + "/Count_FC_OBS_" + f"{Acc:02d}" + "h_EFFCI" + f"{EFFCI:02d}" + "_VRT" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "_" + SystemFC + "_" + RegionName + "_" + TheDate.strftime("%Y%m%d") + "_" + TheDate.strftime("%H") + "_" + f"{StepF_2_Plot:03d}" + ".npy"
                        count_yes_fc.append(np.load(FileIN)[0] / NumEM)
                        count_yes_obs.append(np.load(FileIN)[1])
                        TheDate += timedelta(days=1)

                  # Computing the max count in the forecasts
                  max_count_yes_fc_list.append(np.max(np.array(count_yes_fc)))

                  # Plotting the counts
                  ax1.plot(TheDates_list, count_yes_fc, ".-", color=Colour_SystemFC, label=SystemFC, linewidth=1)

            # Adding metadata to the plot
            max_count_yes_fc = np.max(np.array(max_count_yes_fc_list))
            ax1.set_title(r"$\bf{Count\ of\ yes-events\ in\ forecasts\ and\ observations}$" + "\nEFFCI>=" +  str(EFFCI) + ", VRT=tp(" + str(MagnitudeInPerc_Rain_Event_FR) + "th perc), Region=" + RegionName + ", " + str(Acc) + "-hourly period ending at StepF=" + str(StepF_2_Plot),  pad=40, fontsize=16, color="#333333")
            ax1.set_xlabel("Days", fontsize=16, color="#333333")
            ax1.xaxis.set_major_formatter(DateFormatter("%d-%b"))
            ax1.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1, interval=1))
            ax1.xaxis.set_tick_params(labelsize=16, rotation=20, colors="#333333")
            ax1.set_ylabel("Forecasts", fontsize=16, labelpad=10, color="#333333")
            ax1.set_ylim([0, Max_Count_Plot_yaxis])
            ax1.yaxis.set_tick_params(labelsize=16, colors="#333333")
            ax1.legend(loc="upper right",  bbox_to_anchor=(0.5, 1.1), ncol=7, fontsize=20, frameon=False)
            ax1.yaxis.grid(False)
            ax1.xaxis.grid(True)

            #ax1.yaxis.tick_right()  # Move y-axis ticks to the right
            ax2 = ax1.twinx()
            ax2.bar(TheDates_list, count_yes_obs, color="#333333", label="Flood reports")
            ax2.invert_yaxis()
            ax2.set_ylabel("Observations", fontsize=16, labelpad=10, color="#333333")
            ax2.set_ylim([10, 0])
            ax2.yaxis.set_tick_params(labelsize=16, colors="#333333")
            ax2.legend(loc="upper left",  bbox_to_anchor=(0.6, 1.1), fontsize=20, frameon=False)
            
            # Saving the plot
            DirOUT_temp= Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h"
            FileNameOUT_temp = "Counts_YesFC_YesOBS_" + f"{Acc:02d}" + "h_VRT" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "_EFFCI" + f"{EFFCI:02d}" + "_" + RegionName + "_"+ f"{StepF_2_Plot:03d}" + "MaxY" + str(Max_Count_Plot_yaxis) + ".jpeg"
            if not os.path.exists(DirOUT_temp):
                  os.makedirs(DirOUT_temp)
            plt.savefig(DirOUT_temp + "/" + FileNameOUT_temp)
            plt.close()                     