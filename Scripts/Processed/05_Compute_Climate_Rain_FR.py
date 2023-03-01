import os
from datetime import datetime, time, timedelta
import numpy as np
import pandas as pd
import metview as mv

########################################################################
# CODE DESCRIPTION
# 05_Compute_Climate_Rain_FR.py computes the climatology of rainfall events 
# associated with flash floods.

# INPUT PARAMETERS DESCRIPTION
# Year (year, in YYYY format): year to consider.
# Acc (number, in hours): accumulation to consider.
# EFFCI_list (list of integers, from 1 to 10): EFFCI indexes to consider.
# MagnitudeInPerc_Rain_Event_FR_list (list of integers, from 0 to 100): magnitude, in 
#     percentile, of rainfall events that can potentially conduct to flash floods.
# RegionName_list (list of strings): names for the domain's regions.
# Git_repo (string): repository's local path.
# FileIN_FR (string): relative path of the file containing the cleaned point point flood reports.
# DirIN_FC (string): relative path of the directory containing the ecPoint rainfall forecasts.
# DirOUT (string): relative path of the directory containing the rainfall climatology.

# INPUT PARAMETERS
Year = 2019
Acc = 12
EFFCI_list = [1,6,10]
MagnitudeInPerc_Rain_Event_FR_list = [50, 75, 85, 90, 95, 98, 99]
RegionName_list = ["La Costa","La Sierra"]
Git_repo="/ec/vol/ecpoint/mofp/PhD/Papers2Write/FlashFloods_Ecuador"
FileIN_FR = "Data/Compute/01_Clean_PointFR/Ecu_FF_Hist_ECMWF.csv"
DirIN_FC = "Data/Raw/FC/ecPoint"
DirOUT = "Data/Compute/05_Climate_Rain_FR"
########################################################################

# Reading the cleaned point point flood reports for the considered year
PointFR = pd.read_csv(Git_repo + "/" + FileIN_FR)

# Considering a specific EFFCI index for the point point flood reports to use in the computation 
# of the climatology of rainfall events associated with flash floods 
for EFFCI in EFFCI_list:

      # Computing the climatology of rainfall events associated with flash floods for a 
      # specific region
      for RegionName in RegionName_list:

            print(" ")
            print("EFFCI: ", EFFCI, ", Region: ", RegionName)
            print("  Considering the following point point flood reports...")

            # Extracting the point point flood reports for a specific year, EFFCI  index and region
            PointFR_temp = PointFR.loc[(PointFR["year"] == Year) & (PointFR["EFFCI"] >= EFFCI) & (PointFR["Georegion"] == RegionName)]

            # Extracting some parameters from the point point flood reports database
            lat_list = list(PointFR_temp["Y_DD"])
            lon_list = list(PointFR_temp["X_DD"])
            date_time_list = list(PointFR_temp["ReportDateTimeUTC"])

            # Initializing the variable that will contain the rainfall events associated with the point point flood reports
            rain_event_FR = np.array(MagnitudeInPerc_Rain_Event_FR_list)
            
            for ind in range(len(PointFR_temp)):
                  
                  print("     - ", (ind+1), "/", len(PointFR_temp))

                  # Extracting the lat/lon coordinates and the date/time of single point point flood reports
                  lat_temp = lat_list[ind]
                  lon_temp = lon_list[ind]
                  date_time_temp = datetime.strptime(date_time_list[ind], "%Y-%m-%d %H:%M:%S")

                  # Selecting the forecasts to read based on the report's time
                  DateSTR_x = datetime.strftime(date_time_temp.date(), "%Y%m%d")
                  DateSTR_1x = datetime.strftime(date_time_temp.date() - timedelta(days=1), "%Y%m%d")
                  if date_time_temp.time() >= time(0,0) and date_time_temp.time() < time(6,0):
                        FileIN_FC_list = [Git_repo + "/" + DirIN_FC + "/" + DateSTR_1x + "00/Pt_BC_PERC_" + f"{Acc:03d}" + "_" + DateSTR_1x + "_00_030.grib",
                                                      Git_repo + "/" + DirIN_FC + "/" + DateSTR_1x + "12/Pt_BC_PERC_" + f"{Acc:03d}" + "_" + DateSTR_1x + "_12_018.grib",
                                                      Git_repo + "/" + DirIN_FC + "/" + DateSTR_x + "00/Pt_BC_PERC_" + f"{Acc:03d}" + "_" + DateSTR_x + "_00_012.grib",
                                                      Git_repo + "/" + DirIN_FC + "/" + DateSTR_1x + "12/Pt_BC_PERC_" + f"{Acc:03d}" + "_" + DateSTR_1x + "_12_024.grib"]
                  elif date_time_temp.time() >= time(6,0) and date_time_temp.time() < time(12,0):
                        FileIN_FC_list = [Git_repo + "/" + DirIN_FC + "/" + DateSTR_x + "00/Pt_BC_PERC_" + f"{Acc:03d}" + "_" + DateSTR_x + "_00_012.grib",
                                                      Git_repo + "/" + DirIN_FC + "/" + DateSTR_1x + "12/Pt_BC_PERC_" + f"{Acc:03d}" + "_" + DateSTR_1x + "_12_024.grib",
                                                      Git_repo + "/" + DirIN_FC + "/" + DateSTR_x + "00/Pt_BC_PERC_" + f"{Acc:03d}" + "_" + DateSTR_x + "_00_018.grib",
                                                      Git_repo + "/" + DirIN_FC + "/" + DateSTR_1x + "12/Pt_BC_PERC_" + f"{Acc:03d}" + "_" + DateSTR_1x + "_12_030.grib"]
                  elif date_time_temp.time() >= time(12,0) and date_time_temp.time() < time(18,0):
                        FileIN_FC_list = [Git_repo + "/" + DirIN_FC + "/" + DateSTR_x + "00/Pt_BC_PERC_" + f"{Acc:03d}" + "_" + DateSTR_x + "_00_018.grib",
                                                      Git_repo + "/" + DirIN_FC + "/" + DateSTR_1x + "12/Pt_BC_PERC_" + f"{Acc:03d}" + "_" + DateSTR_1x + "_12_030.grib",
                                                      Git_repo + "/" + DirIN_FC + "/" + DateSTR_x + "00/Pt_BC_PERC_" + f"{Acc:03d}" + "_" + DateSTR_x + "_00_024.grib",
                                                      Git_repo + "/" + DirIN_FC + "/" + DateSTR_x + "12/Pt_BC_PERC_" + f"{Acc:03d}" + "_" + DateSTR_x + "_12_012.grib"]
                  else:
                        FileIN_FC_list = [Git_repo + "/" + DirIN_FC + "/" + DateSTR_x + "00/Pt_BC_PERC_" + f"{Acc:03d}" + "_" + DateSTR_x + "_00_024.grib",
                                                      Git_repo + "/" + DirIN_FC + "/" + DateSTR_x + "12/Pt_BC_PERC_" + f"{Acc:03d}" + "_" + DateSTR_x + "_12_012.grib",
                                                      Git_repo + "/" + DirIN_FC + "/" + DateSTR_x + "00/Pt_BC_PERC_" + f"{Acc:03d}" + "_" + DateSTR_x + "_00_030.grib",
                                                      Git_repo + "/" + DirIN_FC + "/" + DateSTR_x + "12/Pt_BC_PERC_" + f"{Acc:03d}" + "_" + DateSTR_x + "_12_018.grib"]

                  # Reading the forecasts and extracting the rainfall totals for the nearest gridpoint to the flood report
                  fc_FR = []
                  for indFC in range(len(FileIN_FC_list)):
                        FileIN_FC = FileIN_FC_list[indFC]
                        if os.path.isfile(FileIN_FC):
                              fc = mv.read(FileIN_FC)
                              fc_FR.extend(mv.nearest_gridpoint(fc, lat_temp, lon_temp))

                  # Computing different magnitudes of rainfall events associated with the point flood reports
                  rain_event_FR = np.vstack([rain_event_FR, np.percentile(np.array(fc_FR), MagnitudeInPerc_Rain_Event_FR_list)])

            # Computing the climatology of rainfall events associated with flash floods
            climate_rain_FR = np.percentile(rain_event_FR[1:], range(0,100), axis=0)
            climate_rain_FR = np.vstack([np.array(MagnitudeInPerc_Rain_Event_FR_list),climate_rain_FR])
            climate_rain_FR = np.column_stack((np.array(range(-1,100)),climate_rain_FR))
            
            # Savin in a .csv file the climatology of rainfall events associated with flash floods
            DirOUT_temp= Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h/EFFCI" + f"{EFFCI:02d}"
            FileNameOUT = "Climate_Rain_FR_" + f"{Acc:02d}" + "h _EFFCI" + f"{EFFCI:02d}" + "_" +  RegionName.split()[1] + ".csv"
            if not os.path.exists(DirOUT_temp):
                  os.makedirs(DirOUT_temp)
            np.savetxt(DirOUT_temp + "/" + FileNameOUT, climate_rain_FR, delimiter=",", fmt='%0.2f')            