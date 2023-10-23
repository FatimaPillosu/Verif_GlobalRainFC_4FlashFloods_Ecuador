import os
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator

#####################################################################################################################
# CODE DESCRIPTION
# 18_Plot_Count_YesFC_YesOBS.py plots the counts of yes forecast and observation events.
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
DateS = datetime(2020,1,1,0)
DateF = datetime(2020,12,31,0)
StepF_Start = 12
StepF_Final = 120
Disc_Step = 6
StepF_2_Plot = 72
Acc = 12
EFFCI_list = [6]
MagnitudeInPerc_Rain_Event_FR_list = [85,99]
RepetitionsBS = 100
RegionName_list = ["Costa","Sierra"]
SystemFC_list = ["ENS", "ecPoint"]
Colour_SystemFC_list = ["#ec4d37", "#00539CFF"]
NumEM_list = [51,99]
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
DirIN = "Data/Compute/15_Counts_FC_OBS_Exceeding_VRT"
DirOUT = "Data/Plot/18_Count_YesFC_YesOBS"
#####################################################################################################################


# Creating the list containing the steps to considered in the computations
StepF_list = np.arange(StepF_Start, (StepF_Final+1), Disc_Step)
m = len(StepF_list)
ind_StepF_2_Plot = np.where(StepF_list == StepF_2_Plot)[0][0]

# Generating the list of days in the verification period
TheDates_original = []
TheDate = DateS
while TheDate <= DateF:
      TheDates_original.append(TheDate)
      TheDate += timedelta(days=1)
n = len(TheDates_original)

# Computing the counts for a specific EFFCI index
for EFFCI in EFFCI_list:
      
      # Computing the counts for a specific VRT
      for MagnitudeInPerc_Rain_Event_FR in MagnitudeInPerc_Rain_Event_FR_list:

            # Computing the counts for a specific region
            for indRegion in range(len(RegionName_list)): 
            
                  # Selecting the region to consider
                  RegionName = RegionName_list[indRegion]

                  print(" - Plot the count of yes forecasts and observation events for  " + RegionName + ", EFFCI>=" + str(EFFCI) + ", VRT>=tp(" + str(MagnitudeInPerc_Rain_Event_FR) + "th percentile)")

                  # Setting the figure
                  fig, ax = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

                  # Computing the counts for a specific forecasting system
                  for indSystemFC in range(len(SystemFC_list)):
                        
                        # Selecting the forecasting system to consider and the colour to associate to it in the plots
                        SystemFC = SystemFC_list[indSystemFC]
                        Colour_SystemFC = Colour_SystemFC_list[indSystemFC]
                        NumEM = NumEM_list[indSystemFC]

                        # Initializing the variables containing the FB values, and the bootstrapped ones
                        tot_count_yes_fc = np.zeros([m,n+1])
                        tot_count_yes_obs = np.zeros([m,n+1])
                        
                        # Computing FB for a specific lead time
                        for indStepF in range(len(StepF_list)):
                              
                              # Selecting the StepF to consider
                              StepF = StepF_list[indStepF]
                              print("     - Considering " + SystemFC + " and StepF=" + str(StepF) + " ...")

                              # Storing information about the step computed
                              tot_count_yes_fc[indStepF, 0] = StepF
                              tot_count_yes_obs[indStepF, 0] = StepF

                              # Computing the counts for the selected dates
                              for ind_TheDate in range(n):
                                    TheDate = TheDates_original[ind_TheDate]
                                    FileIN = Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h/EFFCI" +  f"{EFFCI:02d}" + "/VRT" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "/" + f"{StepF:03d}" + "/" + SystemFC + "/" + RegionName + "/Count_FC_OBS_" + f"{Acc:02d}" + "h_EFFCI" + f"{EFFCI:02d}" + "_VRT" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "_" + SystemFC + "_" + RegionName + "_" + TheDate.strftime("%Y%m%d") + "_" + TheDate.strftime("%H") + "_" + f"{StepF:03d}" + ".npy"
                                    tot_count_yes_fc[indStepF, ind_TheDate+1] = int(np.load(FileIN)[0] / NumEM)
                                    tot_count_yes_obs[indStepF, ind_TheDate+1] = np.load(FileIN)[1]
                                    TheDate += timedelta(days=1)

                        print(tot_count_yes_fc)
                        
                        # Plotting the counts
                        ax[0].plot(TheDates_original, tot_count_yes_fc[ind_StepF_2_Plot,1:], ".-", color=Colour_SystemFC, label=SystemFC, linewidth=1)
                  
                  # Adding metadata to the plot
                  ax[1].bar(TheDates_original, tot_count_yes_obs[ind_StepF_2_Plot,1:], color="black", label="Flood reports")
                  fig.suptitle(r"$\bf{Counts\ of\ yes-events\ in\ forecasts\ and\ observations}$" + "\nEFFCI>=" +  str(EFFCI) + ", VRT=tp(" + str(MagnitudeInPerc_Rain_Event_FR) + "th perc), Region=" + RegionName + ", " + str(Acc) + "-hourly period ending at StepF=" + str(StepF_2_Plot), fontsize=16, color="#333333")
                  ax[0].legend(loc="upper right", fontsize=16)
                  ax[1].legend(loc="upper right", fontsize=16)
                  ax[1].set_xlabel("Days", fontsize=16, color="#333333")
                  ax[1].xaxis.set_major_formatter(DateFormatter("%d-%b-%y"))
                  ax[1].xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1, interval=1))
                  ax[1].xaxis.set_major_locator(MaxNLocator(integer=True))
                  ax[1].xaxis.set_tick_params(labelsize=16, rotation=45, colors="#333333")
                  ax[0].set_ylabel("Counts", fontsize=16, color="#333333")
                  ax[0].yaxis.set_major_locator(MaxNLocator(integer=True))
                  ax[0].yaxis.set_tick_params(labelsize=16, colors="#333333")
                  ax[1].set_ylabel("Counts", fontsize=16, labelpad=30, color="#333333")
                  ax[1].yaxis.set_major_locator(MaxNLocator(integer=True))
                  ax[1].yaxis.set_tick_params(labelsize=16, colors="#333333")
                  plt.tight_layout()

                  # Saving the plot
                  DirOUT_temp= Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h"
                  FileNameOUT_temp = "Counts_YesFC_YesOBS_" + f"{Acc:02d}" + "h_VRT" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "_EFFCI" + f"{EFFCI:02d}" + "_" + RegionName + "_"+ f"{StepF_2_Plot:03d}" + ".jpeg"
                  if not os.path.exists(DirOUT_temp):
                        os.makedirs(DirOUT_temp)
                  plt.savefig(DirOUT_temp + "/" + FileNameOUT_temp)
                  plt.close() 
                              