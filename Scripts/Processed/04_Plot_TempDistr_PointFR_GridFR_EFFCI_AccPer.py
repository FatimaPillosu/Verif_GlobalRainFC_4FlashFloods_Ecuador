import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

##############################################################################
# CODE DESCRIPTION
# 04_Plot_TempDistr_PointFR_GridFR_EFFCI_AccPer.py plots the temporal distribution of point 
# and gridded flood reports for each day in the verification period, EFFCI index, and 
# accumulation period.
# Note: the code takes 5 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# DateS (date, in format YYYYMMDD): start date of the considered period of time.
# DateF (date, in format YYYYMMDD): final date of the considered period of time.
# Acc (number, in hours): accumulation to consider.
# AccPerS_list (list of numbers, in UTC hour): start of the accumulation periods to consider.
# EFFCI_list (list of integers, from 1 to 10): EFFCI indexes to consider.
# MaxFR (integer): maximum number of flood reports in the whole period.
# Git_repo (string): repository's local path.
# DirIN (string): relative path of the directory containing the gridded, accumulated flood reports.
# DirOUT (string): relative path of the directory containing the distribution's plots.

# INPUT PARAMETERS
DateS = datetime(2020,1,1)
DateF = datetime(2020,12,31)
Acc = 12
AccPerS_list = [0,6,12,18]
EFFCI_list = [1,6,10]
MaxFR = 12
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
DirIN = "Data/Compute/03_GridFR_EFFCI_AccPer"
DirOUT = "Data/Plot/04_TempDistr_PointFR_GridFR_EFFCI_AccPer"
##############################################################################


# Considering a specific EFFCI index
for EFFCI in EFFCI_list: 

      print("Creating and saving the distribution plots of the point and gridded flood reports, per grid-box, with EFFCI>=" + str(EFFCI) + ", for " + str(len(AccPerS_list)) + " " + str(Acc) + "-hourly accumulation periods")
            
      # Create the figure for all the plots
      fig, axarr = plt.subplots(len(AccPerS_list), 1, figsize=(10, 10), sharex=True)
      ind_plot = 0

      # Considering a specific accumulation period
      for AccPerS in AccPerS_list:
            
            # Defining the end of the considered accumulation period
            AccPerF = AccPerS + Acc

            # Creating the list that will store the number of point and gridded flood reports per grid-box in the considered domain for each date in the period of interest
            Num_PointFR = []
            Num_GridFR = []

            # Considering specific dates in the period of interest
            TheDate_list = []
            TheDate = DateS
            while TheDate <= DateF:
                  
                  # Defining the valid date for the considered end of the accumulation period
                  Date_AccPerF = TheDate + timedelta(hours=AccPerF) 

                  # Reading the file containing the number of point flood reports per grid-box in the considered domain
                  FileIN= Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h/EFFCI" + f"{EFFCI:02d}" + "/" + Date_AccPerF.strftime("%Y%m%d") + "/" + "GridFR_" + f"{Acc:02d}" + "h_EFFCI" + f"{EFFCI:02d}" + "_" + Date_AccPerF.strftime("%Y%m%d") + "_" + Date_AccPerF.strftime("%H") + ".grib"
                  FR = mv.values(mv.read(FileIN))
                  
                  # Extracting the number of point and gridded flood reports per grid-box in the considered domain
                  Num_PointFR.append(int(np.sum(FR)))
                  Num_GridFR.append(np.sum(FR>0))
                  
                  # Creating the list containing the dates in the period of interest
                  TheDate_list.append(TheDate)

                  TheDate += timedelta(days=1) 
            
            # Plot data on each subplot
            width = 0.9
            idx = np.asarray([i for i in range(len(TheDate_list))])
            axarr[ind_plot].bar(idx, Num_PointFR, color="#372800", width=width, label="Point_FR")
            axarr[ind_plot].bar(idx, Num_GridFR, color="#f67293", width=width, label="Grid_FR")
            
            ind_plot = ind_plot + 1

      # Complete the figure
      fig.suptitle("Counts of flood reports (FR) in " +  str(DateS.year) + " with EFFCI>=" + str(EFFCI) + ", accumulated over " + str(Acc) + "-hourly periods", fontsize=14, weight="bold", color="#333333")
      legend = axarr[0].legend()
      for text in legend.get_texts():
            text.set_color("#333333")
      axarr[0].legend(loc="upper center",  bbox_to_anchor=(0.5, 1.3), ncol=2,  fontsize=14, frameon=False)
      axarr[3].set_xlabel("Days", fontsize=14, labelpad=10, color="#333333")
      ind_plot = 0
      for ax in axarr:
            # setting legend for each sub-plot
            ax.text(0.84, 0.85, "Period starting at " + f"{AccPerS_list[ind_plot]:02d}" + " UTC", transform=ax.transAxes, ha="center", va="center", fontsize=14, bbox=dict(facecolor="white", alpha=1, edgecolor="#333333"), color="#333333")
            ind_plot = ind_plot + 1
            # setting x-axis
            ax.set_xlim(-1, (len(TheDate_list)+1))
            ax.xaxis.set_major_formatter(DateFormatter("%b-%d"))
            ax.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1, interval=1))
            ax.xaxis.set_tick_params(labelsize=14, rotation=45, colors="#333333")
            # setting y-axis
            ax.set_ylabel("Counts", fontsize=14, color="#333333")
            ax.set_yticks(np.arange(0, MaxFR+1, 2))
            ax.yaxis.set_tick_params(labelsize=14, colors="#333333")
            # setting the plot grid
            ax.grid()
      plt.tight_layout()

      # Saving the plot
      DirOUT_temp= Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h"
      FileNameOUT = "TempDistr_PointFR_GridFR_AccPer_" + DateS.strftime("%Y%m%d") + "_" + DateF.strftime("%Y%m%d") + "_" + f"{Acc:02d}" + "h _EFFCI" + f"{EFFCI:02d}" + ".png"
      FileOUT = DirOUT_temp + "/" + FileNameOUT
      if not os.path.exists(DirOUT_temp):
            os.makedirs(DirOUT_temp)
      fig.savefig(FileOUT)
      plt.close()