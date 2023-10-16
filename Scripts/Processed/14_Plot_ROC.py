import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#####################################################################################
# CODE DESCRIPTION
# 12_Plot_ROC.py plots ROC curves.
# Note: the code can take up 20 minutes to run in serial.

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
# Perc_VRE (integer, from 0 to 100): percentile that defines the verifying rainfall event to consider.
# RegionName_list (list of strings): list of names for the domain's regions.
# Lines_Region_list (list of strings): types of lines used to plot ROC curves for different regions. 
# SystemFC_list (list of strings): list of names of forecasting systems to consider.
# NumEM_list (list of integers): numer of ensemble members in the considered forecasting systems.
# Colour_SystemFC_list (list of strings): colours used to plot ROC curves for different forecasting systems.
# Git_repo (string): repository's local path.
# DirIN (string): relative path containing the daily probabilistic contingency tables.
# DirOUT (string): relative path of the directory containing the ROC curve plots.

# INPUT PARAMETERS
DateS = datetime(2020,1,1,0)
DateF = datetime(2020,12,31,0)
StepF_Start = 12
StepF_Final = 246
Disc_Step = 6
Acc = 12
EFFCI_list = [1,6,10]
MagnitudeInPerc_Rain_Event_FR_list = [85,99]
RegionName_list = ["Costa", "Sierra"]
Lines_Region_list = ["o-", "o--"]
SystemFC_list = ["ENS", "ecPoint"]
NumEM_list = [51,99]
Colour_SystemFC_list = ["magenta", "cyan"]
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
DirIN = "Data/Compute/07_Daily_Prob_Contingency_Tables"
DirOUT = "Data/Plot/12_ROC"
#####################################################################################

# Plotting ROC curves for a specific EFFCI index
for EFFCI in EFFCI_list:
       
       # Plotting ROC curves for a specific VRE
      for MagnitudeInPerc_Rain_Event_FR in MagnitudeInPerc_Rain_Event_FR_list:

            # Plotting ROC curves for a specific lead time
            for StepF in range(StepF_Start, (StepF_Final+1), Disc_Step):
                  
                  print("Plotting the ROC curves for EFFCI>=" + str(EFFCI) + ", VRE>=tp(" + str(MagnitudeInPerc_Rain_Event_FR) + "th percentile), and StepF=" + str(StepF) + " ...") 

                  # Setting the figure for the plot of the ROC curve
                  fig, ax = plt.subplots(figsize=(10, 8))

                  # Plotting ROC curves for a specific forecasting system
                  for indSystemFC in range(len(SystemFC_list)):
                        
                        # Selecting the forecasting system to plot, and its correspondent colour in the plot
                        SystemFC = SystemFC_list[indSystemFC]
                        NumEM = NumEM_list[indSystemFC]
                        Colour_SystemFC = Colour_SystemFC_list[indSystemFC]

                          # Plotting ROC curves for a specific region
                        for indRegion in range(len(RegionName_list)): 

                              # Selecting the region to plot, and its correspondent line type in the plot
                              RegionName = RegionName_list[indRegion]
                              Lines_Region = Lines_Region_list[indRegion]

                              # Reading the daily probabilistic contingency tables, and adding them over the verification period
                              ct_tot = np.zeros((NumEM+1,4), dtype=int)
                              TheDate = DateS
                              while TheDate <= DateF:
                                    DirIN_temp= Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h/EFFCI" + f"{EFFCI:02d}" + "/VRE" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "/" + f"{StepF:03d}" + "/" + SystemFC
                                    FileNameIN_temp = "CT_" + f"{Acc:02d}" + "h_EFFCI" + f"{EFFCI:02d}" + "_VRE" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "_" + SystemFC + "_" + TheDate.strftime("%Y%m%d") + "_" + TheDate.strftime("%H") + "_" + f"{StepF:03d}" + ".csv"
                                    if os.path.isfile(DirIN_temp + "/" + FileNameIN_temp):
                                          ct_daily = pd.read_csv(DirIN_temp + "/" + FileNameIN_temp).to_numpy()[:,1:]
                                          ct_tot = ct_tot + ct_daily
                                    TheDate += timedelta(days=1)     
                              
                              # Computing hit rates and false alarm rates 
                              hr = ct_tot[:,0] / (ct_tot[:,0] + ct_tot[:,2])
                              far = ct_tot[:,1] / (ct_tot[:,1] + ct_tot[:,3])

                              # Plotting the ROC curves
                              ax.plot(far, hr, Lines_Region, color=Colour_SystemFC, label=SystemFC + " - " + RegionName, linewidth=2)
                              
                  # Setting the plot metadata
                  ax.plot([0,1], [0,1], "-", color="grey", linewidth=2)
                  ax.set_title("ROC curve\n" + r"EFFCI>=" + str(EFFCI) + " - VRE>=tp(" + str(MagnitudeInPerc_Rain_Event_FR) + "th percentile) - StepF=" + str(StepF), fontsize=20, pad=20)
                  ax.set_xlabel("False Alarm Rate [-]", fontsize=18, labelpad=10)
                  ax.set_ylabel("Hit Rate [-]", fontsize=18, labelpad=10)
                  ax.set_xlim([0,1])
                  ax.set_ylim([0,1])
                  ax.set_xticks(np.arange(0,1.1, 0.1))
                  ax.set_yticks(np.arange(0,1.1, 0.1))
                  ax.xaxis.set_tick_params(labelsize=16)
                  ax.yaxis.set_tick_params(labelsize=16)
                  ax.legend(loc="lower right", fontsize=16)
                  ax.grid()
                  
                  # Saving the plot
                  DirOUT_temp= Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h/EFFCI" + f"{EFFCI:02d}" + "/VRE" + f"{MagnitudeInPerc_Rain_Event_FR:02d}"
                  FileNameOUT_temp = "ROC_" + f"{Acc:02d}" + "h_EFFCI" + f"{EFFCI:02d}" + "_VRE" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "_" + f"{StepF:03d}" + ".jpeg"
                  if not os.path.exists(DirOUT_temp):
                        os.makedirs(DirOUT_temp)
                  plt.savefig(DirOUT_temp + "/" + FileNameOUT_temp)
                  plt.close()