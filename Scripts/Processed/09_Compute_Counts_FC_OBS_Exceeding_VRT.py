import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import metview as mv 

##########################################################################################################
# CODE DESCRIPTION
# 09_Compute_Counts_FC_OBS_Exceeding_VRT.py computes daily counts of ensemble members and observations exceeding a 
# considered VRT. 
# Note: the code can take up 4 days to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Year (integer, in format YYYY): year to consider in the processing.
# StepF_Start (integer, in hours): first final step of the accumulation periods to consider.
# StepF_Final (integer, in hours): last final step of the accumulation periods to consider.
# Disc_Step (integer, in hours): discretization for the final steps to consider.
# Acc (number, in hours): rainfall accumulation to consider.
# EFFCI_list (list of integers, from 1 to 10): list of EFFCI indexes to consider.
# MagnitudeInPerc_Rain_Event_FR_list (list of integers, from 0 to 100): magnitude of potentially flash-flood-leading rainfall events.
# Perc_VRT (integer, from 0 to 100): percentile that defines the verifying rainfall event to consider.
# RegionCode_list (list of integers): list of codes for the domain's regions. 
# RegionName_list (list of strings): list of names for the domain's regions.
# SystemFC_list (list of strings): list of names of forecasting systems to consider.
# Git_repo (string): repository's local path.
# FileIN_Mask (string): relative path of the file containing the domain's mask.
# DirIN_Climate_Rain_FR (string): relative path of the file containing the climatology of the rainfall 
#     events associated with flash floods. 
# DirIN_FC (string): relative path of the directory containing the rainfall forecasts.
# DirIN_GridFR (string): relative path containing the gridded flood reports.
# DirOUT (string): relative path of the directory containing the daily probabilistic contingency tables.

# INPUT PARAMETERS
Year = 2020
StepF_Start = 12
StepF_Final = 246
Disc_Step = 6
Acc = 12
EFFCI_list = [1,6,10]
MagnitudeInPerc_Rain_Event_FR_list = [85, 99]
Perc_VRT = 25
RegionCode_list = [1,2];
RegionName_list = ["Costa","Sierra"];
SystemFC_list = ["ENS", "ecPoint"]
Git_repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
FileIN_Mask = "Data/Raw/Ecuador_Mask_ENS/Mask.grib"
DirIN_Climate_Rain_FR = "Data/Compute/07_Climate_Rain_FR"
DirIN_FC = "Data/Raw/FC"
DirIN_GridFR = "Data/Compute/03_GridFR_EFFCI_AccPer"
DirOUT = "Data/Compute/09_Counts_FC_OBS_Exceeding_VRT"
##########################################################################################################

# Sorting the range of dates to process
DateS = datetime(Year, 1, 1)
DateF = datetime(Year, 12,31)

# Reading the file containing the mask for the considered domain
mask = mv.values(mv.read(Git_repo + "/" + FileIN_Mask))

# Creating the daily counts of forecasts and observations exceeding a VRT
for SystemFC in SystemFC_list:

      # Creating the daily counts for a specific lead time
      for StepF in range(StepF_Start, (StepF_Final+1), Disc_Step):
            
            # Creating the daily counts for a specific date
            TheDate = DateS

            while TheDate <= DateF:
                  
                  print(" ")
                  print(" - Reading " + SystemFC + ", StepF=" + str(StepF) + ", FC date: " + TheDate.strftime("%Y-%m-%d") + " at " + TheDate.strftime("%H") + " UTC")

                  # Reading the rainfall forecasts for the considered date
                  tp = [] # variable needed to asses whether the forecasts for the considered date exist
                  if SystemFC == "ENS":
                        # Note: converting the forecasts in accumulated rainfall over the considered period. Converting also their units from m to mm.
                        StepS = StepF - Acc
                        FileIN_FC_temp1= Git_repo + "/" + DirIN_FC + "/" + SystemFC + "/" + TheDate.strftime("%Y%m%d%H") + "/tp_" + TheDate.strftime("%Y%m%d") + "_" + TheDate.strftime("%H") + "_" + f"{StepS:03d}" + ".grib"
                        FileIN_FC_temp2= Git_repo + "/" + DirIN_FC + "/" + SystemFC + "/" + TheDate.strftime("%Y%m%d%H") + "/tp_" + TheDate.strftime("%Y%m%d") + "_" + TheDate.strftime("%H") + "_" + f"{StepF:03d}" + ".grib"
                        if os.path.isfile(FileIN_FC_temp1) and os.path.isfile(FileIN_FC_temp1):
                              tp1 = mv.read(FileIN_FC_temp1)
                              tp2 = mv.read(FileIN_FC_temp2)
                              tp = mv.values((tp2-tp1) * 1000)
                  elif SystemFC == "ecPoint":
                        # Note: the forecasts are already accumulated over the considered period, and are already expressed in mm. The forecasts are stored in files whose name indicates the end of the accumulated period.
                        FileIN_FC_temp= Git_repo + "/" + DirIN_FC + "/" + SystemFC + "/" + TheDate.strftime("%Y%m%d%H") + "/Pt_BC_PERC_" + f"{Acc:03d}" + "_" + TheDate.strftime("%Y%m%d") + "_" + TheDate.strftime("%H") + "_" + f"{StepF:03d}" + ".grib"
                        if os.path.isfile(FileIN_FC_temp):
                              tp = mv.values(mv.read(FileIN_FC_temp))
                                  
                  # Checking that the rainfall forecasts exist for the considered date. If not, they are not added in the 3d-array
                  if len(tp) != 0:

                        # Defining the valid time for the accumulation period
                        ValidTimeF = TheDate + timedelta(hours=StepF)

                        # Creating the daily probabilistic contingency tables for a specific EFFCI index
                        for EFFCI in EFFCI_list: 
                              
                              # Reading the accumulated gridded flood reports
                              # Note: the accumulated gridded flood reports are stored in files whose name indicates the end of the accumulated period.
                              FileIN_GridFR_temp = Git_repo + "/" + DirIN_GridFR + "/" + f"{Acc:02d}" + "h/EFFCI" + f"{EFFCI:02d}" + "/" + ValidTimeF.strftime("%Y%m%d") + "/GridFR_" + f"{Acc:02d}" + "h_EFFCI" + f"{EFFCI:02d}" + "_" + ValidTimeF.strftime("%Y%m%d") + "_" + ValidTimeF.strftime("%H") + ".grib"
                              GridFR = mv.values(mv.read(FileIN_GridFR_temp))
                              
                              # Creating the daily probabilistic contingency tables for a specific region
                              for indReg in range(len(RegionCode_list)):

                                    # Extracting the name and the code of the region of interest
                                    RegionName = RegionName_list[indReg]
                                    RegionCode = RegionCode_list[indReg]

                                    # Selecting the grid-boxes belonging to the considered region
                                    ind_mask_region = np.where(mask == RegionCode)[0]

                                    # Selecting the grid-boxes in the forecast fields belonging to the considered region 
                                    tp_region = tp[:, ind_mask_region].flatten()

                                    # Selecting the grid-boxes in the observational fields belonging to the considered region
                                    GridFR_region = GridFR[ind_mask_region]
                                    count_obs_exceed_VRT = np.sum(GridFR_region > 0)
                                    
                                    # Reading the climatology of rainfall events associated with flash floods
                                    File_Rain_Climate_FR = Git_repo + "/" + DirIN_Climate_Rain_FR + "/" + f"{Acc:02d}" + "h/EFFCI" + f"{EFFCI:02d}" + "/Climate_Rain_FR_" + f"{Acc:02d}" + "h_EFFCI" + f"{EFFCI:02d}" + "_" + RegionName + ".csv"
                                    climate_rain_FR = pd.read_csv(File_Rain_Climate_FR)
                                    
                                    # Creating the daily probabilistic contingency tables for a specific magnitude of rainfall events associated with flash floods
                                    for MagnitudeInPerc_Rain_Event_FR in MagnitudeInPerc_Rain_Event_FR_list:
                              
                                          print("     - Computing ct for VRT>=tp(" + str(MagnitudeInPerc_Rain_Event_FR) + "th perc)" + "," + RegionName + ", EFFCI>=" + str(EFFCI))

                                          # Selecting the considered verifying rainfall event (VRT)
                                          VRT = climate_rain_FR["RainEvent_Magnitude_" + str(MagnitudeInPerc_Rain_Event_FR) + "th_Percentile"][Perc_VRT]

                                          # Computing the counts of forecasts and observations exceeding the considered VRT
                                          count_fc_exceed_VRT = np.sum(tp_region >= VRT)
                                          count_fc_obs_exceed_VRT = np.hstack([count_fc_exceed_VRT,count_obs_exceed_VRT])
                                          
                                          # Saving the counts
                                          DirOUT_temp= Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h/EFFCI" + f"{EFFCI:02d}" + "/VRT" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "/" + f"{StepF:03d}" + "/" + SystemFC + "/" + RegionName
                                          FileNameOUT_temp = "Count_FC_OBS_" + f"{Acc:02d}" + "h_EFFCI" + f"{EFFCI:02d}" + "_VRT" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "_" + SystemFC + "_" + RegionName + "_" + TheDate.strftime("%Y%m%d") + "_" + TheDate.strftime("%H") + "_" + f"{StepF:03d}"
                                          if not os.path.exists(DirOUT_temp):
                                                os.makedirs(DirOUT_temp)
                                          np.save(DirOUT_temp + "/" + FileNameOUT_temp, count_fc_obs_exceed_VRT)

                  else:

                        print("   - NOTE: the requested forecast is not present in the database.")

                  TheDate += timedelta(days=1)         
