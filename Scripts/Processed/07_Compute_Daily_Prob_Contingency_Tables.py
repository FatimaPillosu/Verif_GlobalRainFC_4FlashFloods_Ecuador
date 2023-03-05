import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import metview as mv

#################################################################################
# CODE DESCRIPTION
# 05_Compute_Climate_Rain_FR.py computes the climatology of rainfall events 
# associated with flash floods.

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
DateS = datetime(2020,1,1,0)
DateF = datetime(2020,12,31,0)
StepF_Start = 12
StepF_Final = 246
Disc_Step = 6
Acc = 12
EFFCI_list = [1,6,10]
MagnitudeInPerc_Rain_Event_FR_list = [85, 99]
Perc_VRE = 25
RegionCode_list = [1,2];
RegionName_list = ["Costa","Sierra"];
SystemFC_list = ["ENS", "ecPoint"]
Git_repo="/ec/vol/ecpoint/mofp/PhD/Papers2Write/FlashFloods_Ecuador"
FileIN_Mask = "Data/Raw/Ecuador_Mask_ENS/Mask.grib"
DirIN_Climate_Rain_FR = "Data/Compute/05_Climate_Rain_FR"
DirIN_FC = "Data/Raw/FC"
DirIN_GridFR = "Data/Compute/03_GridFR_EFFCI_AccPer"
DirOUT = "Data/Compute/07_Daily_Prob_Contingency_Tables"
#################################################################################

# Reading the file containing the mask for the considered domain
mask = mv.values(mv.read(Git_repo + "/" + FileIN_Mask))

# Computing the daily probabilistic contingency tables
print(" ")
print("Computing daily probabilistic contingency tables for the period between " + DateS.strftime("%Y%m%d") + " and " + DateF.strftime("%Y%m%d"))
print(" ")

# Creating the daily probabilistic contingency tables for a specific forecasting system
for SystemFC in SystemFC_list:

      # Creating the daily probabilistic contingency tables for a specific date
      TheDate = DateS
      while TheDate <= DateF:
            
            # Creating the daily probabilistic contingency tables for a specific lead time
            for StepF in range(StepF_Start, (StepF_Final+1), Disc_Step):
                  
                  # Defining the beginning of the accumulation period
                  StepS = StepF - Acc

                  # Defining the valid time for the accumulation period
                  ValidTimeS = TheDate + timedelta(hours=StepS)
                  ValidTimeF = TheDate + timedelta(hours=StepF)

                  print(" - for " + SystemFC + ", FC: "  + TheDate.strftime("%Y%m%d") + " at " + TheDate.strftime("%H") + " UTC (t+" + str(StepS) + ",t+" + str(StepF) + "), VT: " + ValidTimeS.strftime("%Y%m%d") + " at " + ValidTimeS.strftime("%H") + " UTC and " + ValidTimeF.strftime("%Y%m%d") + " at " + ValidTimeF.strftime("%H") + " UTC")
                  
                  # Reading the rainfall forecasts
                  tp = []
                  if SystemFC == "ENS":
                        # Note: converting the forecasts in accumulated rainfall over the considered period. Converting also their units from m to mm.
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
                  
                  # Checking that the requested forecasts exists and were read correctly. If not, the following lead time is considered.
                  if len(tp) != 0:
                        
                        # Extracting the number of ensemble members in the considered forecasting system
                        num_em = tp.shape[0]

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

                                    # Selecting the gird-boxes from the domain belonging to the considered region
                                    ind_mask_region = np.where(mask == RegionCode)[0]

                                    # Selecting the grid-boxes in the observational fileds belonging to the considered region
                                    GridFR_region = GridFR[ind_mask_region]
                                    
                                    # Reading the climatology of rainfall events associated with flash floods
                                    File_Rain_Climate_FR = Git_repo + "/" + DirIN_Climate_Rain_FR + "/" + f"{Acc:02d}" + "h/EFFCI" + f"{EFFCI:02d}" + "/Climate_Rain_FR_" + f"{Acc:02d}" + "h_EFFCI" + f"{EFFCI:02d}" + "_" + RegionName + ".csv"
                                    climate_rain_FR = pd.read_csv(File_Rain_Climate_FR)
                                    
                                    # Creating the daily probabilistic contingency tables for a specific magnitude of rainfall events associated with flash floods
                                    for MagnitudeInPerc_Rain_Event_FR in MagnitudeInPerc_Rain_Event_FR_list:
                              
                                          print("   - for VRE>=tp(" + str(MagnitudeInPerc_Rain_Event_FR) + "th perc)" + "," + RegionName + ", EFFCI>=" + str(EFFCI))

                                          # Selecting the considered verifying rainfall event (VRE)
                                          vre = round(climate_rain_FR[f"{MagnitudeInPerc_Rain_Event_FR:.2f}"][Perc_VRE])

                                          # Selecting the grid-boxes in the forecast fields belonging to the considered region and counting how many
                                          # ensemble members exceed the VRE
                                          tp_region = tp[:, ind_mask_region]
                                          count_members_exceeding_vre = np.sum((tp_region >= vre), axis=0)
                                          
                                          # Computing the probabilistic contingecy table
                                          ct = np.empty([num_em+1,5])
                                          for count_members in range(num_em+1):
                                                GridFR_region_fc_yes = GridFR_region[np.where(count_members_exceeding_vre >= count_members)[0]]
                                                GridFR_region_fc_no = GridFR_region[np.where(count_members_exceeding_vre < count_members)[0]]
                                                ct[count_members][0] = int(count_members)
                                                ct[count_members][1] = np.where(GridFR_region_fc_yes > 0)[0].shape[0] # HITS
                                                ct[count_members][2] = np.where(GridFR_region_fc_yes == 0)[0].shape[0] # FALSE ALARMS
                                                ct[count_members][3] = np.where(GridFR_region_fc_no > 0)[0].shape[0] # MISSES
                                                ct[count_members][4] = np.where(GridFR_region_fc_no == 0)[0].shape[0] # CORRECT NEGATIVES
                                          ct = ct.astype(int)

                                          # Saving the probabilistic contingency table
                                          DirOUT_temp= Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h/VRE" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "/" + SystemFC + "/EFFCI" + f"{EFFCI:02d}" + "/" + TheDate.strftime("%Y%m%d%H")
                                          FileNameOUT_temp = "CT_" + f"{Acc:02d}" + "h_VRE" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "_" + SystemFC + "_EFFCI" + f"{EFFCI:02d}" + "_" + TheDate.strftime("%Y%m%d")  + "_" + TheDate.strftime("%H") + "_" + f"{StepF:03d}" + "_" + RegionName + ".csv"
                                          if not os.path.exists(DirOUT_temp):
                                                os.makedirs(DirOUT_temp)
                                          ct_df = pd.DataFrame(ct, columns = ["N. OF MEMBERS (AT LEAST) EXCEEDING VRE", "HITS", "FALSE ALARMS", "MISSES", "CORRECT NEGATIVES"])
                                          ct_df.to_csv(DirOUT_temp + "/" + FileNameOUT_temp, index=False)

                  else:

                        print("   - NOTE: the requested forecast is not present in the database.")

            TheDate += timedelta(days=1)             