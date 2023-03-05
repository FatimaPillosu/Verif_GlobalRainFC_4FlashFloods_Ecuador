import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# INPUT PARAMETERS
DateS = datetime(2020,1,1,0)
DateF = datetime(2020,12,31,0)
StepF_Start = 12
StepF_Final = 246
Disc_Step = 6
Acc = 12
EFFCI_list = [1,6,10]
VRE_InPerc_list = [85,99]
RegionName_list = ["Costa", "Sierra"]
Lines_Region_list = [".-", ".--"]
SystemFC_list = ["ENS", "ecPoint"]
NumEM_list = [51,99]
Colour_SystemFC_list = ["magenta", "cyan"]
Git_repo="/ec/vol/ecpoint/mofp/PhD/Papers2Write/FlashFloods_Ecuador"
DirIN = "Data/Compute/07_Daily_Prob_Contingency_Tables"
DirOUT = "Data/Plot/08_ROC"
###############################################################################

# Plotting ROC curves for a specific EFFCI index
for EFFCI in EFFCI_list:
       
       # Plotting ROC curves for a specific VRE
      for VRE_InPerc in VRE_InPerc_list:

            # Plotting ROC curves for a specific lead time
            for StepF in range(StepF_Start, (StepF_Final+1), Disc_Step):
                  
                  print("Plotting the ROC curves for EFFCI>=" + str(EFFCI) + ", VRE>=tp(" + str(VRE_InPerc) + "th percentile), and StepF=" + str(StepF) + " ...") 

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
                                    DirIN_temp = Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h/VRE" + f"{VRE_InPerc:02d}" + "/" + SystemFC + "/EFFCI" + f"{EFFCI:02d}" + "/" + TheDate.strftime("%Y%m%d%H")
                                    FileNameIN_temp = "CT_" + f"{Acc:02d}" + "h_VRE" + f"{VRE_InPerc:02d}" + "_" + SystemFC + "_EFFCI" + f"{EFFCI:02d}" + "_" + TheDate.strftime("%Y%m%d") + "_" + TheDate.strftime("%H") + "_" + f"{StepF:03d}" + "_" + RegionName + ".csv"
                                    if os.path.isfile(DirIN_temp + "/" + FileNameIN_temp):
                                          ct_daily = pd.read_csv(DirIN_temp + "/" + FileNameIN_temp).to_numpy()[:,1:]
                                          ct_tot = ct_tot + ct_daily
                                    TheDate += timedelta(days=1)     
                              
                              # Computing hit rates and false alarm rates 
                              hr = ct_tot[:,0] / (ct_tot[:,0] + ct_tot[:,2])
                              far = ct_tot[:,1] / (ct_tot[:,1] + ct_tot[:,3])

                              # Plotting the ROC curves
                              ax.plot(far, hr, Lines_Region, color=Colour_SystemFC, label=SystemFC + " - " + RegionName)
                              ax.plot([0,1], [0,1], "-", color="black")

                  # Setting the plot metadata
                  ax.set_title("ROC curve\n" + r"EFFCI>=" + str(EFFCI) + " - VRE>=tp(" + str(VRE_InPerc) + "th percentile) - StepF=" + str(StepF), fontsize=20, pad=20)
                  ax.set_xlabel("False Alarm Rate [-]", fontsize=18, labelpad=10)
                  ax.set_ylabel("Hit Rate [-]", fontsize=18, labelpad=10)
                  ax.set_xlim([0,1])
                  ax.set_ylim([0,1])
                  ax.xaxis.set_tick_params(labelsize=16)
                  ax.yaxis.set_tick_params(labelsize=16)
                  ax.legend(loc="lower right", fontsize=16)
                  ax.grid()
                  
                  # Saving the plot
                  DirOUT_temp= Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h/EFFCI" + f"{EFFCI:02d}" + "/VRE" + str(VRE_InPerc)
                  FileNameOUT = "ROC_" + f"{Acc:02d}" + "h _EFFCI" + f"{EFFCI:02d}" + "_VRE" + str(VRE_InPerc) + "_" + f"{StepF:03d}" + ".jpeg"
                  FileOUT = DirOUT_temp + "/" + FileNameOUT
                  if not os.path.exists(DirOUT_temp):
                        os.makedirs(DirOUT_temp)
                  plt.savefig(FileOUT)