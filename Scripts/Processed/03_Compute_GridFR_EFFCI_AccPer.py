import os
from datetime import datetime, timedelta
import pandas as pd
import metview as mv

###############################################################################
# CODE DESCRIPTION
# 03_Compute_GridFR_EFFCI_AccPer.py computes the gridded flood observational fields from 
# the point flood reports, for specific EFFCI indexes and accumulation periods. The fields are 
# saved in .grib files that contain the number of flood reports in each grid-box of the domain of 
# interest. The file names contain the end time of the accumulation period.

# INPUT PARAMETERS DESCRIPTION
# Year (year, in YYYY format): year to consider.
# Acc (number, in hours): accumulation to consider.
# AccPerS_list (list of numbers, in UTC hour): start of the accumulation periods to consider.
# EFFCI_list (list of integers, from 1 to 10): EFFCI indexes to consider.
# Git_repo (string): repository's local path.
# FileIN_Mask (string): relative path of the file containing the domain's mask.
# FileIN_PointFR (string): relative path of the file containing the clean point flood reports.
# DirOUT (string): relative path of the directory containing the gridded flood observational fields.

# INPUT PARAMETERS
DateS = datetime(2020,1,1)
DateF = datetime(2021,1,10)
Acc = 12
AccPerS_list = [0,6,12,18]
EFFCI_list = [1,6,10]
Git_repo="/ec/vol/ecpoint/mofp/PhD/Papers2Write/FlashFloods_Ecuador"
FileIN_Mask = "Data/Raw/Ecuador_Mask_ENS/Mask.grib"
FileIN_PointFR = "Data/Compute/01_Clean_PointFR/Ecu_FF_Hist_ECMWF.csv"
DirOUT = "Data/Compute/03_GridFR_EFFCI_AccPer"
###############################################################################

# Setting some general parameters
AccSTR = f"{Acc:02d}"

# Reading Ecuador's mask
FileIN_Mask = Git_repo + "/" + FileIN_Mask
Mask = mv.read(FileIN_Mask)

# Reading the cleaned point flood reports
FileIN_PointFR = Git_repo + "/" + FileIN_PointFR
PointFR = pd.read_csv(FileIN_PointFR)
PointFR["ReportDateTimeUTC"] = pd.to_datetime(PointFR["ReportDateTimeUTC"] )

# Selecting the point flood reports for EFFCI indexes of interest
for EFFCI in EFFCI_list: 
    
    EFFCI_STR = f"{EFFCI:02d}"
    PointFR_EFFCI = PointFR.loc[PointFR["EFFCI"] >= EFFCI]
    
    # Selecting the point flood reports for the days of interest
    TheDate = DateS
    while TheDate <= DateF:

        print("Creating the gridded flood observational fields for EFFCI>=" + str(EFFCI) + " on " + TheDate.strftime("%Y%m%d"))

        # Selecting the point flood reports for the accumulation periods of interest
        for AccPerS in AccPerS_list:
            
            AccPerF = AccPerS + Acc
            
            # Setting the template for the flood observational fields
            GridFR_template = mv.values(Mask * 0)
            
            # Selecting the point flood reports for the considered accumulation period
            Date_AccPerS = TheDate + timedelta(hours=AccPerS) 
            Date_AccPerF = TheDate + timedelta(hours=AccPerF) 
            ind = PointFR_EFFCI.index[ (PointFR_EFFCI["ReportDateTimeUTC"]>=Date_AccPerS) & (PointFR_EFFCI["ReportDateTimeUTC"]<Date_AccPerF) ]
            
            if ind.shape[0] != 0: # Assigning the point flood reports to the correspondent grid boxes
                lats = PointFR_EFFCI.loc[ind, "Y_DD"].to_numpy()
                lons = PointFR_EFFCI.loc[ind, "X_DD"].to_numpy()
                for i in range(len(lats)):
                    temp = mv.nearest_gridpoint_info(Mask, lats[i], lons[i])
                    temp_list = str(temp[0]).split(",")
                    PointFR_index_grid = int(float((temp_list[2].split(":"))[1]))
                    GridFR_template[PointFR_index_grid] = GridFR_template[PointFR_index_grid] + 1
                GridFR_grib_temp = mv.set_values (Mask,GridFR_template)
            else: # Saving an observational field full of zeros because there are no point flood reports in the considered accumulation period
                GridFR_grib_temp = Mask * 0 

            # Saving the gridded flood observational fields
            DirOUT_temp= Git_repo + "/" + DirOUT + "/" + AccSTR + "h/EFFCI" + EFFCI_STR + "/" + Date_AccPerF.strftime("%Y%m%d")
            FileOUT = "GridFR_" + AccSTR + "h_EFFCI" + EFFCI_STR + "_" + Date_AccPerF.strftime("%Y%m%d") + "_" + Date_AccPerF.strftime("%H") + ".grib"
            if not os.path.exists(DirOUT_temp):
                os.makedirs(DirOUT_temp)
            mv.write(DirOUT_temp + "/" + FileOUT, GridFR_grib_temp)
        
        TheDate += timedelta(days=1) 