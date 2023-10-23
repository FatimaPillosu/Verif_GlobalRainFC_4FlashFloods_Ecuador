import os
from datetime import datetime, time, timedelta
import numpy as np
import pandas as pd
import metview as mv

##########################################################################################################
# CODE DESCRIPTION
# 09_Compute_Climate_Rain_FR.py computes the climatology of rainfall events associated with flash floods.
# Note: the code can take up 3 hours to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Year (year, in YYYY format): year to consider.
# Acc (number, in hours): accumulation to consider.
# EFFCI_list (list of integers, from 1 to 10): EFFCI indexes to consider.
# MagnitudeInPerc_Rain_Event_FR_list (list of integers, from 0 to 100): magnitude of potentially flash-flood-leading rainfall events.
# Climate_Percs (list of floats, from 0 to 100): list of percentiles to compute for the rainfall climatology.
# Format_Climate_Percs (string): format in the output files for the climatology percentiles.
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
Climate_Percs = range(0,100)
Format_Climate_Percs = "%d"
RegionName_list = ["La Costa","La Sierra"]
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
FileIN_FR = "Data/Compute/01_Clean_PointFR/Ecu_FF_Hist_ECMWF.csv"
DirIN_FC = "Data/Raw/FC/ecPoint"
DirOUT = "Data/Compute/09_Climate_Rain_FR"
##########################################################################################################

# Reading the cleaned point point flood reports for the considered year
PointFR = pd.read_csv(Git_repo + "/" + FileIN_FR)

# Creating the headers for the final .csv output files as a string (comma separated),
# and the string that will define the values format for each column
Headers = "Climate_Percentiles"
Format = Format_Climate_Percs
for MagnitudeInPerc_Rain_Event_FR in MagnitudeInPerc_Rain_Event_FR_list:
      Headers = Headers + ",RainEvent_Magnitude_" + str(MagnitudeInPerc_Rain_Event_FR) + "th_Percentile"
      Format = Format + ",%.2f"

# Computing the climatology of rainfall events associated with flash floods for a specific EFFCI index 
for EFFCI in EFFCI_list:

      # Computing the climatology of rainfall events associated with flash floods for a specific region
      for RegionName in RegionName_list:

            print(" ")
            print("Computing the rainfall climatologies for EFFCI: " + str(EFFCI) + ", Region: " + RegionName)

            # Extracting the point point flood reports for a specific year, EFFCI  index and region
            PointFR_temp = PointFR.loc[(PointFR["year"] == Year) & (PointFR["EFFCI"] >= EFFCI) & (PointFR["Georegion"] == RegionName)]

            # Extracting some parameters from the point point flood reports database
            lat_list = list(PointFR_temp["Y_DD"])
            lon_list = list(PointFR_temp["X_DD"])
            date_time_list = list(PointFR_temp["ReportDateTimeUTC"])

            # Initializing the variable that will contain the rainfall events associated with the point point flood reports
            rain_event_FR = np.array(MagnitudeInPerc_Rain_Event_FR_list)

            # Computing the rainfall climatology
            for ind_PointFR in range(len(PointFR_temp)):
                  
                  print(" - Considering point flood report n." + str(ind_PointFR+1) + " of " + str(len(PointFR_temp)))

                  # Extracting the lat/lon coordinates and the date/time of single point point flood reports
                  lat_temp = lat_list[ind_PointFR]
                  lon_temp = lon_list[ind_PointFR]
                  date_time_temp = datetime.strptime(date_time_list[ind_PointFR], "%Y-%m-%d %H:%M:%S")

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
                  for ind_FC in range(len(FileIN_FC_list)):
                        FileIN_FC = FileIN_FC_list[ind_FC]
                        if os.path.isfile(FileIN_FC):
                              fc = mv.read(FileIN_FC)
                              fc_FR.extend(mv.nearest_gridpoint(fc, lat_temp, lon_temp))

                  # Computing different magnitudes of rainfall events associated with the point flood reports
                  rain_event_FR = np.vstack([rain_event_FR, np.percentile(np.array(fc_FR), MagnitudeInPerc_Rain_Event_FR_list)])

            # Computing the rainfall climatology for the different events' magnitudes
            climate_rain_FR = np.percentile(rain_event_FR[1:], Climate_Percs, axis=0) # eliminate the first row of values which come from the initialization of the variable

            # Adding a column at the beginning of the matrix to indicate the percentiles each column corresponds to
            climate_rain_FR = np.column_stack((np.array(Climate_Percs),climate_rain_FR))
            
            # Savin in a .csv file the climatology of rainfall events associated with flash floods
            DirOUT_temp= Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h/EFFCI" + f"{EFFCI:02d}"
            FileNameOUT = "Climate_Rain_FR_" + f"{Acc:02d}" + "h_EFFCI" + f"{EFFCI:02d}" + "_" +  RegionName.split()[1] + ".csv"
            if not os.path.exists(DirOUT_temp):
                  os.makedirs(DirOUT_temp)
            np.savetxt(DirOUT_temp + "/" + FileNameOUT, climate_rain_FR, delimiter=",", fmt=Format, header=Headers, comments='')            