import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter


# INPUT PARAMETERS
DateS = datetime(2020,1,1)
DateF = datetime(2020,12,31)
Acc = 12
AccPerS_list = [0,6,12,18]
EFFCI_list = [1,6,10]
Git_repo="/ec/vol/ecpoint/mofp/PhD/Papers2Write/FlashFloods_Ecuador"
DirIN = "Data/Compute/03_GridFR_EFFCI_AccPer"
DirOUT = "Data/Plot/04_Distr_PointFR_GridFR_EFFCI_AccPer"
###############################################################################


# Considering a specific EFFCI index
for EFFCI in EFFCI_list: 

      # Considering a specific accumulation period
      for AccPerS in AccPerS_list:
            
            print("Creating and saving the plot of the distribution of point and gridded flood reports per grid-box with EFFCI>=" + str(EFFCI) + ", accumulated over " + str(Acc) + "-hourly periods starting at " + str(AccPerS) + " UTC")
            
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

            # Creating the plot of the distribution of point and gridded flood reports per grid-box in the considered domain
            fig, ax = plt.subplots(figsize=(20, 8))
            idx = np.asarray([i for i in range(len(TheDate_list))])
            width = 0.5
            ax.bar(idx, Num_PointFR, color='orange', width=width, label="PointFR")
            ax.bar(idx+width, Num_GridFR, color='green', width=width, label="GridFR")
            ax.set_title("Flood reports per grid-box with EFFCI>=" + str(EFFCI) + ", accumulated over " + str(Acc) + "-hourly periods starting at " + str(AccPerS) + " UTC between " + DateS.strftime("%d-%m-%Y") + " and " + DateF.strftime("%d-%m-%Y"), fontsize=20, pad=30)
            ax.legend(loc="upper right", fontsize=18)
            ax.set_xlabel("Days", fontsize=18, labelpad=10)
            ax.set_xlim([0, (len(TheDate_list)+1)])
            ax.set_xticks(idx)
            ax.set_xticklabels(TheDate_list)
            ax.xaxis.set_major_formatter(DateFormatter("%b-%d"))
            ax.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1, interval=1))
            ax.xaxis.set_tick_params(labelsize=14)
            ax.set_ylabel("N. of Flood Reports", fontsize=18, labelpad=10)
            ax.set_ylim([0,12])
            ax.set_yticks(np.arange(0, 13))
            ax.yaxis.set_tick_params(labelsize=14)
            ax.grid()
            
            # Saving the plot
            DirOUT_temp= Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h/EFFCI" + f"{EFFCI:02d}"
            FileNameOUT = "Distr_PointFR_GridFR_" + DateS.strftime("%Y%m%d") + "_" + DateF.strftime("%Y%m%d") + "_" + f"{Acc:02d}" + "h _EFFCI" + f"{EFFCI:02d}" + "_" +  f"{AccPerS:02d}" + ".jpeg"
            FileOUT = DirOUT_temp + "/" + FileNameOUT
            if not os.path.exists(DirOUT_temp):
                  os.makedirs(DirOUT_temp)
            plt.savefig(FileOUT)

            