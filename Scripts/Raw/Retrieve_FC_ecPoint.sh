#!/bin/bash

################################################################
# CODE DESCRIPTION
# Retrieve_FC_ecPoint retrieves ecPoint-Rainfall forecasts from ECFS.
# Files contain global rainfall forecasts for the considered accumulation period, 
# ending at the time step indicated in the file name.

# INPUT PARAMETERS DESCRIPTION
# BaseDateS (date, in YYYYMMDD format): first forecast's basedate to retrieve
# BaseDateF (date, in YYYYMMDD format): last forecast's basedate to retrieve
# BaseTime (time, in H format, in UTC time): forecast's basetime to retrieve 
# Acc (number, in H format, in hours): observations' accumulation period 
# VersFC (string): forecasts versions.
#                             See which calibration versions are available in the following webpage:
#                             https://confluence.ecmwf.int/display/EVAL/1.+ecPoint-Rainfall%3A+Developed+or+Under-Development+Calibrations                               
# Git_repo (string): repository's local path
# DirOUT (string): relative path where to store the retrieved forecasts

# INPUT PARAMETERS
BaseDateS=20200101
BaseDateF=20201231
BaseTime=0
Acc=12
VersFC="1.2"
Git_repo="/ec/vol/ecpoint/mofp/PhD/Papers2Write/FlashFloods_Ecuador"
DirOUT="Data/Raw/FC/ecPoint"
################################################################


# Setting general variables
BaseDateS=$(date -d ${BaseDateS} +%Y%m%d)
BaseDateF=$(date -d ${BaseDateF} +%Y%m%d)
BaseTimeSTR=$(printf %02d ${BaseTime})
AccSTR=$(printf %03d ${Acc})

# Setting directories
EcfsDir="ec:/emos/ecpoint/Oper/ecPoint_Rainfall/${AccSTR}/Vers${VersFC}"
LocalDir=${Git_repo}/${DirOUT}
mkdir -p ${LocalDir}

# Retrieving forecasts from ECFS
BaseDate=${BaseDateS}
while [[ ${BaseDate} -le ${BaseDateF} ]]; do
    
    echo " "
    echo "Retrieving forecast for ${BaseDate}"

        DirIN_temp="${EcfsDir}/${BaseDate}${BaseTimeSTR}"
        DirOUT_temp="${LocalDir}/${BaseDate}${BaseTimeSTR}"
        mkdir -p ${DirOUT_temp}
        
        ecp ${DirIN_temp}/Pt_BiasCorr_RainPERC.tar ${DirOUT_temp}    
        tar -xvf "${DirOUT_temp}/Pt_BiasCorr_RainPERC.tar"
        mv "${DirOUT_temp}/sc2/tcwork/emos/emos_data/log/ecpoint_oper/emos/Forecasts/Oper/ecPoint_Rainfall/${AccSTR}/Vers${VersFC}/${BaseDate}${BaseTimeSTR}/Pt_BiasCorr_RainPERC/*" ${DirOUT_temp}
        
        rm -rf "${DirOUT_temp}/Pt_BiasCorr_RainPERC.tar" "${DirOUT_temp}/sc2"
        
    done
    
    BaseDate=$(date -d"${BaseDate} + 1 day" +"%Y%m%d")

done 