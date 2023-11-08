import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import metview as mv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

########################################################################################################
# CODE DESCRIPTION
# 07_Plot_RainObs_Loc_Distr.py plots a map with the location of rainfall observations, and the distribution of the rainfall totals.
# Code runtime: negligible.

# INPUT PARAMETERS DESCRIPTION
# Acc (number, in hours): rainfall accumulation to consider.
# DateS (date, in format YYYYMMDD): start day of the period to consider.
# DateF (date, in format YYYYMMDD): final day of the period to consider.
# AccPerF_list (list of integer, inUTC hours): list of the final times of the accumulation periods to consider.
# CornersDomain_list (list of floats): coordinates [N/E/S/W] of the domain to plot.
# RegionCode_list (list of integers): codes for the domain's regions to consider. 
# RegionName_list (list of strings): names for the domain's regions to consider.
# RegionColour_list (list of strings): rgb-codes for the domain's regions to consider.
# Git_repo (string): repository's local path.
# FileIN_Mask (string): relative path of the file containing the domain's mask.
# DirIN (string): relative path containing the rainfall observations.
# DirOUT (string): relative path where the map plot with the observations location and the observations distribution are stored.

# INPUT PARAMETERS
Acc = 12
DateS = datetime(2010,1,1,0)
DateF = datetime(2020,12,31,0)
AccPerF_list = [12,0]
CornersDomain_list = [2,-81.5,-5.5,-74.5] 
RegionCode_list = [1,2,3]
RegionName_list = ["Costa", "Sierra", "Oriente"]
RegionColour_list = ["#ffea00", "#c19a6b", "#A9FE00"]
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
FileIN_Mask = "Data/Raw/Ecuador_Mask_ENS/Mask.grib"
DirIN = "Data/Compute/06_Extract_RainObs_Region_AccPer"
DirOUT = "Data/Plot/07_RainObs_Loc_Distr"
########################################################################################################

# Creating the output directory
DirOUT_temp = Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h"
if not os.path.exists(DirOUT_temp):
      os.makedirs(DirOUT_temp)

# Reading the domain's mask
FileIN_Mask = Git_repo + "/" + FileIN_Mask
mask = mv.read(FileIN_Mask)

# Creating the array containing all the dates in the considered period
dates = pd.date_range(start=DateS, end=DateF, freq='D')

# Initializing the variables that contain all the rainfall observations
obs_lats_all = np.array([])
obs_lons_all = np.array([])

# Creating the figure for all the count plots
fig1, ax1 = plt.subplots(len(RegionName_list), len(AccPerF_list), figsize=(12, 10), sharex=True)
fig2, ax2 = plt.subplots(len(RegionName_list), len(AccPerF_list), figsize=(12, 10), sharex=True)

# Reading the rainfall observations for a specific region
ind_Region = 0
for in_Region in range(len(RegionName_list)):

      # Select the region to consider for the computation of the observational rainfall climatology
      RegionName = RegionName_list[in_Region]
      RegionCode = RegionCode_list[in_Region]
      RegionColour = RegionColour_list[in_Region]

      # Reading the rainfall observations for a specific accumulation period
      ind_AccPerF = 0
      for AccPerF in AccPerF_list:

            # Initializing the variables that will contain the  rainfall observations
            obs_lats = np.array([])
            obs_lons = np.array([])
            obs_vals = np.array([])
            obs_counts = []

            # Reading the rainfall observations for each day of the considered time period
            TheDate_list = []
            TheDate = DateS
            while TheDate <= DateF:

                  print("Reading rainfall observations for " + RegionName + " for the " + f"{Acc:02d}" + "-hourly rainfall observations for the accumulation period ending on " + TheDate.strftime("%Y%m%d") + " at " +  f"{AccPerF:02d}" + " UTC") 

                  # Reading the observations
                  FileIN = Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h/" + TheDate.strftime("%Y%m%d") + "/tp" +  f"{Acc:02d}" + "_obs_" + TheDate.strftime("%Y%m%d") + f"{AccPerF:02d}" + "_" + RegionName + ".npy"
                  temp = np.load(FileIN)
                  obs_lats = np.concatenate((obs_lats, temp[0,:]))
                  obs_lons = np.concatenate((obs_lons, temp[1,:]))
                  obs_vals = np.concatenate((obs_vals, temp[2,:]))
                  obs_counts.append(temp.shape[1])

                  # Creating the list containing the dates in the period of interest
                  TheDate_list.append(TheDate)

                  TheDate += timedelta(days=1)

            # Concatenating all the observations
            obs_lats_all = np.concatenate((obs_lats_all, obs_lats))
            obs_lons_all = np.concatenate((obs_lons_all, obs_lons))

            # Plotting the rainfall observation counts
            ax1[ind_Region, ind_AccPerF].bar(dates, obs_counts, color=RegionColour)
            ax1[ind_Region, ind_AccPerF].set_ylim(0, np.max(obs_counts)+2)
            ax1[ind_Region, ind_AccPerF].set_yticks(np.arange(0, np.max(obs_counts)+2, 2))
            ax1[ind_Region, ind_AccPerF].yaxis.set_tick_params(labelsize=12, colors="#333333")
            if ind_AccPerF == 0:
                  ax1[ind_Region, ind_AccPerF].set_ylabel("Counts", fontsize=12, labelpad=10, color="#333333")  
            if ind_AccPerF == len(AccPerF_list):
                  ax1[ind_Region, ind_AccPerF].set_xlabel("Days", fontsize=12, color="#333333")
                  ax1[ind_Region, ind_AccPerF].xaxis.set_major_formatter(DateFormatter('%Y'))
                  ax1[ind_Region, ind_AccPerF].xaxis.set_major_locator(mdates.YearLocator(month=1, day=1))
                  ax1[ind_Region, ind_AccPerF].xaxis.set_tick_params(labelsize=12, rotation=30, colors="#333333")
            
            # Plotting the distribution of rainfall observations
            ax2[ind_Region, ind_AccPerF].hist(obs_vals, bins=np.arange(0, 501, 2), color=RegionColour)
            inset_ax = ax2[ind_Region, ind_AccPerF].inset_axes([0.2, 0.2, 0.77, 0.77])
            inset_ax.hist(obs_vals, bins=np.arange(0, 501, 2), color=RegionColour)
            inset_ax.set_ylim([0,20])
            if ind_AccPerF == 0:
                  ax2[ind_Region, ind_AccPerF].set_ylabel("Counts", fontsize=12, labelpad=10, color="#333333")  
            if ind_AccPerF == len(AccPerF_list):
                  ax2[ind_Region, ind_AccPerF].set_xlabel("Rainfall mm" + str(Acc) + "h]", fontsize=12, color="#333333")
                  ax2[ind_Region, ind_AccPerF].xaxis.set_major_formatter(DateFormatter('%Y'))
                  ax2[ind_Region, ind_AccPerF].xaxis.set_major_locator(mdates.YearLocator(month=1, day=1))
                  ax2[ind_Region, ind_AccPerF].xaxis.set_tick_params(labelsize=12, rotation=30, colors="#333333")
            
            ind_AccPerF += 1
      
      ind_Region += 1


# Completing the figures
fig1.suptitle("Counts of " + str(Acc) + "-hourly rainfall observations in each day between " +  str(DateS.year) + " and " +  str(DateF.year), fontsize=14, weight="bold", color="#333333")
fig1.tight_layout()
fig2.suptitle("Distribution of " + str(Acc) + "-hourly observed point-rainfall totals between " +  str(DateS.year) + " and " +  str(DateF.year), fontsize=14, weight="bold", color="#333333")
fig2.tight_layout()

# Saving the distribution plot
FileOUT_distr = DirOUT_temp + "/Obs_Counts_" + f"{Acc:02d}" + "h_" + DateS.strftime("%Y%m%d") + "_" + DateF.strftime("%Y%m%d")
fig1.savefig(FileOUT_distr)
FileOUT_distr = DirOUT_temp + "/Obs_Distr_" + f"{Acc:02d}" + "h_" + DateS.strftime("%Y%m%d") + "_" + DateF.strftime("%Y%m%d")
fig2.savefig(FileOUT_distr)

# Plotting the location of the rainfall gauges
obs_geo = mv.create_geo(
      type = "xyv",
      latitudes = obs_lats_all,
      longitudes = obs_lons_all,
      values = np.zeros(obs_lons_all.shape)
      )

coastlines = mv.mcoast(
      map_coastline_resolution = "full",
      map_coastline_colour = "charcoal",
      map_coastline_thickness = 1,
      map_coastline_sea_shade = "on",
      map_coastline_sea_shade_colour = "rgb(0.6455,0.903,0.9545)",
      map_boundaries = "on",
      map_boundaries_colour = "charcoal",
      map_boundaries_thickness = 1,
      map_grid = "on",
      map_grid_latitude_increment  = 2,
      map_grid_longitude_increment = 2,
      map_label = "on",
      map_label_font = "arial",
      map_label_colour = "charcoal",
      map_label_height = 0.6
      )

geo_view = mv.geoview(
      map_area_definition = "corners",
      area = CornersDomain_list,
      coastlines = coastlines
      )

RegionCode_list_temp = (np.array(([0] + RegionCode_list), dtype=float) + 0.1).tolist()
mask_shading = mv.mcont(
      legend = "off",
      contour = "off",
      contour_level_selection_type = "level_list",
      contour_level_list = RegionCode_list_temp,
      contour_label = "off",
      contour_shade = "on",
      contour_shade_technique = "grid_shading",
      contour_shade_colour_method = "list",
      contour_shade_colour_list = RegionColour_list
      )

obs_geo_contour = mv.msymb(
                  legend = "off",
                  symbol_type = "marker",
                  symbol_table_mode = "on",
                  symbol_outline = "on",
                  symbol_min_table = [-0.1],
                  symbol_max_table = [0.1],
                  symbol_colour_table = "black",
                  symbol_marker_table = 15,
                  symbol_height_table = 0.3
                  )

title = mv.mtext(
      text_line_count = 2,
      text_line_1 = "Spatial distribution of rainfall observations between " + DateS.strftime("%Y%m%d") + " and " + DateF.strftime("%Y%m%d"),
      text_line_2 = " ",
      text_font = "sansserif",
      text_colour = "charcoal",
      text_font_size = 0.6,
      text_font_style = "bold"
      )

# Saving the plot with the location of the rainfall observations
FileOUT_loc = DirOUT_temp + "/Obs_Loc_" + f"{Acc:02d}" + "h_" + DateS.strftime("%Y%m%d") + "_" + DateF.strftime("%Y%m%d")
png = mv.png_output(output_name = FileOUT_loc)
mv.setoutput(png)
mv.plot(geo_view, mask, mask_shading, obs_geo, obs_geo_contour, title)