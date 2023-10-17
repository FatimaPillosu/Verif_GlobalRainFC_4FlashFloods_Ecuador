import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import metview as mv 

##########################################################################################################
# CODE DESCRIPTION
# 12_Compute_Daily_Prob_Contingency_Tables.py computes daily probabilistic contingency tables, and stores them in a 3d-array 
# whose dimensions are (NumDays, NumProbThr, NumElementsCT).
# Note: the code can take up 4 days to run in serial. It is recommended to run separate months in parallel to take down the 
# runtime to 8 hours. 

# INPUT PARAMETERS DESCRIPTION
# DateS (date, in format YYYYMMDD): start date of the considered verification period.
# DateF (date, in format YYYYMMDD): final date of the considered verification period.
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
DateS = datetime(2020,2,1,0)
DateF = datetime(2020,2,29,0)
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
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
FileIN_Mask = "Data/Raw/Ecuador_Mask_ENS/Mask.grib"
DirIN_Climate_Rain_FR = "Data/Compute/07_Climate_Rain_FR"
DirIN_FC = "Data/Raw/FC"
DirIN_GridFR = "Data/Compute/03_GridFR_EFFCI_AccPer"
DirOUT = "Data/Compute/12_Daily_Prob_Contingency_Tables"
##########################################################################################################


# COSTUME FUNCTIONS

# Computation of daily probabilistic contingency tables
def daily_prob_ct(tp, obs, VRT, NumEM):
      
      # Counting how many ensemble members exceed the VRT
      count_members_exceeding_VRT = np.sum((tp >= VRT), axis=0)

      # Initializing the variable that will contained the daily probabilistic contingency table
      ct = np.empty([NumEM+1,5])

      # Computing the daily probabilistic contingency table
      for index in range(NumEM+1):
            count_members = NumEM - index
            OBS_yes_fc = obs[np.where(count_members_exceeding_VRT >= count_members)[0]] # observation instances for "yes" forecasts
            OBS_no_fc = obs[np.where(count_members_exceeding_VRT < count_members)[0]] # observation instances for "no" forecasts
            ct[index][0] = count_members # N. OF MEMBERS (AT LEAST) EXCEEDING VRT
            ct[index][1] = np.where(OBS_yes_fc > 0)[0].shape[0] # HITS
            ct[index][2] = np.where(OBS_yes_fc == 0)[0].shape[0] # FALSE ALARMS
            ct[index][3] = np.where(OBS_no_fc > 0)[0].shape[0] # MISSES
            ct[index][4] = np.where(OBS_no_fc == 0)[0].shape[0] # CORRECT NEGATIVES
            ct = ct.astype(int) # setting all values as integers

      return ct

################################################################################


# Reading the file containing the mask for the considered domain
mask = mv.values(mv.read(Git_repo + "/" + FileIN_Mask))

# Computing the daily probabilistic contingency tables
print(" ")
print("Computing daily probabilistic contingency tables for the period between " + DateS.strftime("%Y%m%d") + " and " + DateF.strftime("%Y%m%d"))

# Creating the daily probabilistic contingency tables for a specific forecasting system
for SystemFC in SystemFC_list:

      # Initializing the list containing, for a specific lead time, the dates for which the rainfall forecasts exist
      StepF_Dates_list = []

      # Creating the daily probabilistic contingency tables for a specific lead time
      for StepF in range(StepF_Start, (StepF_Final+1), Disc_Step):
            
            # Creating the daily probabilistic contingency tables for a specific date
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
                        
                        # Extracting the number of ensemble members in the considered forecasting system
                        NumEM = tp.shape[0]

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

                                    # Selecting the grid-boxes in the observational fileds belonging to the considered region
                                    GridFR_region = GridFR[ind_mask_region]
                                    
                                    # Reading the climatology of rainfall events associated with flash floods
                                    File_Rain_Climate_FR = Git_repo + "/" + DirIN_Climate_Rain_FR + "/" + f"{Acc:02d}" + "h/EFFCI" + f"{EFFCI:02d}" + "/Climate_Rain_FR_" + f"{Acc:02d}" + "h_EFFCI" + f"{EFFCI:02d}" + "_" + RegionName + ".csv"
                                    climate_rain_FR = pd.read_csv(File_Rain_Climate_FR)
                                    
                                    # Creating the daily probabilistic contingency tables for a specific magnitude of rainfall events associated with flash floods
                                    for MagnitudeInPerc_Rain_Event_FR in MagnitudeInPerc_Rain_Event_FR_list:
                              
                                          print("     - Computing ct for VRT>=tp(" + str(MagnitudeInPerc_Rain_Event_FR) + "th perc)" + "," + RegionName + ", EFFCI>=" + str(EFFCI))

                                          # Selecting the considered verifying rainfall event (VRT)
                                          VRT = climate_rain_FR["RainEvent_Magnitude_" + str(MagnitudeInPerc_Rain_Event_FR) + "th_Percentile"][Perc_VRT]

                                          # Selecting the grid-boxes in the forecast fields belonging to the considered region 
                                          tp_region = tp[:, ind_mask_region]
                                          
                                          # Computing the probabilistic contingecy table
                                          ct = daily_prob_ct(tp_region, GridFR_region, VRT, NumEM)

                                          # Saving the probabilistic contingency table
                                          DirOUT_temp= Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h/EFFCI" + f"{EFFCI:02d}" + "/VRT" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "/" + f"{StepF:03d}" + "/" + SystemFC + "/" + RegionName
                                          FileNameOUT_temp = "CT_" + f"{Acc:02d}" + "h_EFFCI" + f"{EFFCI:02d}" + "_VRT" + f"{MagnitudeInPerc_Rain_Event_FR:02d}" + "_" + SystemFC + "_" + RegionName + "_" + TheDate.strftime("%Y%m%d") + "_" + TheDate.strftime("%H") + "_" + f"{StepF:03d}" + ".csv"
                                          if not os.path.exists(DirOUT_temp):
                                                os.makedirs(DirOUT_temp)
                                          ct_df = pd.DataFrame(ct, columns = ["N. OF MEMBERS (AT LEAST) EXCEEDING VRT", "HITS", "FALSE ALARMS", "MISSES", "CORRECT NEGATIVES"])
                                          ct_df.to_csv(DirOUT_temp + "/" + FileNameOUT_temp, index=False)

                  else:

                        print("   - NOTE: the requested forecast is not present in the database.")

                  TheDate += timedelta(days=1)         
