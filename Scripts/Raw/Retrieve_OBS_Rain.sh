#!/bin/bash

#####################################################################
# CODE DESCRIPTION
# Retrieve_OBS_Rain.sh retrieves rainfall observations from STVL. The files contain
# rainfall observations from global rain gauges, for the considered accumulation 
# period, ending at the time (in UTC) indicated in the file name.

# INPUT PARAMETERS DESCRIPTION
# DateS (date, in YYYYMMDD format): first date of observations to retrieve
# DateF (date, in YYYYMMDD format): last date of observations to retrieve
# Acc (number, in H format, in hours): observations' accumulation period 
# Git_repo (string): repository's local path
# DirOUT (string): relative path where to store the retrieved observations

# INPUT PARAMETERS
DateS=20100101
DateF=20191231
Acc=12
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
DirOUT="Data/Raw/OBS/Rain"
#####################################################################


# Setting general variables
DateS=$(date -d ${DateS} +%Y%m%d)
DateF=$(date -d ${DateF} +%Y%m%d)
AccSTR=$(printf %02d ${Acc})

# Setting the main output directory
MainDirOUT="${Git_repo}/${DirOUT}_${AccSTR}h"

# Retrieving observations from STVL
TheDate=${DateS}
while [[ ${TheDate} -le ${DateF} ]]; do
    mkdir -p ${MainDirOUT}/${TheDate}
    /home/moz/bin/stvl_getgeo --sources synop hdobs efas --parameter tp --period ${Acc} --dates ${TheDate} --times 0 12 --columns value_0 --outdir ${MainDirOUT}/${TheDate} --flattree
    TheDate=$(date -d"${TheDate} + 1 day" +"%Y%m%d")
done