import os
from datetime import datetime
from dateutil import tz
from dateutil.parser import parse
import numpy as np
import pandas as pd

##################################################################
# CODE DESCRIPTION
# 01_Compute_Clean_PointFR.py cleans the point flood reports by checking that 
# instances with no lat/lon corrdinates, time and date are deleted. It also 
# converts the local reporting times into outc times, and checks that the reports 
# are assigned to the appropriate region according to the developed mask. The 
# cleaned reports are saved in a .csv table that has the same format of the raw 
# reports. 

# INPUT PARAMETERS DESCRIPTION
# TimeZone (string): time zone to consider for the point flood reports.
# Git_repo (string): repository's local path.
# FileIN (string):  relative path of the file containing the raw point flood reports.
# FileOUT (string): relative path of the file storing the cleaned point flood reports.

# INPUT PARAMETERS
TimeZone = "America/Lima"
Git_repo="/ec/vol/ecpoint/mofp/PhD/Papers2Write/FlashFloods_Ecuador"
FileIN = "Data/Raw/OBS/PointFR/Ecu_FF_Hist_ECMWF.csv"
FileOUT = "Data/Compute/01_Clean_PointFR/Ecu_FF_Hist_ECMWF.csv"
##################################################################


# Setting general variables
FileIN = Git_repo + "/" + FileIN
FileOUT= Git_repo + "/" + FileOUT
if not os.path.exists(os.path.split(FileOUT)[0]):
    os.makedirs(os.path.split(FileOUT)[0])

# Reading the raw point flood reports and counting how many raw point flood reports there are
PointFR = pd.read_csv(FileIN)
year_list = PointFR["year"].to_numpy()
year_list = np.unique(year_list)
print(" ")
print("Number of raw reports per year... ")
for year in year_list:
    PointFR_Year = PointFR.loc[PointFR["year"] == year]
    print(year, ":", PointFR_Year.shape[0])

# Deleting instances with no lat/lon corrdinates, time and date and counting how many cleaned point flood reports are left
PointFR = PointFR.dropna(subset = ["Y_DD", "X_DD", "Date","Hora"])
PointFR = PointFR.reset_index(drop=True)
print(" ")
print("Number of cleaned reports per year... ")
for year in year_list:
    PointFR_Year = PointFR.loc[PointFR["year"] == year]
    print(year, ":", PointFR_Year.shape[0])

# Converting the reporting date/times from LOCAL to UTC
print(" ")
print("Converting reporting times from local to utc ...")
PointFR["ReportDateTimeUTC"] = np.nan
from_zone = tz.gettz(TimeZone)
to_zone = tz.gettz("UTC")
for i in range(PointFR.shape[0]):
    DateTimeSTR_local = PointFR.loc[i,"Date"] + " " + PointFR.loc[i,"Hora"]
    DateTime_local = (parse(DateTimeSTR_local)).replace(tzinfo=from_zone)
    DateTime_utc = DateTime_local.astimezone(to_zone)
    DateTime_utc = datetime.strptime(DateTime_utc.strftime("%Y%m%d %H%M%S"),"%Y%m%d %H%M%S")
    PointFR.loc[i,"ReportDateTimeUTC"] = DateTime_utc  

# Checking that the reports are assigned to the correct region 
print(" ")
print("Checking that the reports are assigned to the correct region ...")
ind = PointFR.index[ (PointFR["Georegion"]=="La Costa") & (PointFR["Y_DD"]<0.53) & (PointFR["Y_DD"]>-0.27) & (PointFR["X_DD"]>-79) ]
PointFR.loc[ind,"Georegion"] = "La Sierra"
ind = PointFR.index[ (PointFR["Georegion"]=="La Costa") & (PointFR["Y_DD"]<-1.31) & (PointFR["Y_DD"]>-1.91) & (PointFR["X_DD"]>-79.3) ]
PointFR.loc[ind,"Georegion"] = "La Sierra"
ind = PointFR.index[ (PointFR["Georegion"]=="La Costa") & (PointFR["Y_DD"]<-3.64) & (PointFR["X_DD"]>-80.27) ]
PointFR.loc[ind,"Georegion"] = "La Sierra"
ind = PointFR.index[ (PointFR["Georegion"]=="El Oriente") & (PointFR["X_DD"]<-77.34) ]
PointFR.loc[ind,"Georegion"] = "La Sierra"

# Saving the cleaned flood reports as a .csv table
print(" ")
print("Saving the cleaned flood reports as a .csv table ...")
PointFR.to_csv(FileOUT, sep=",", mode = "w", index=False)