import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv
import matplotlib.pyplot as plt

########################################################################################################
# CODE DESCRIPTION
# 08a_Plot_Obs_Loc_Distr.py plots the map with the location of rainfall observations used in the definition of the observational 
# rainfall climatology, and the distribution of the rainfall totals.
# Code runtime: negligible.

# INPUT PARAMETERS DESCRIPTION
# Acc (number, in hours): rainfall accumulation to consider.
# DateS (date, in format YYYYMMDD): start day of the period to consider.
# DateF (date, in format YYYYMMDD): final day of the period to consider.
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
DateF = datetime(2019,12,31,0)
CornersDomain_list = [2,-81.5,-5.5,-74.5] 
RegionCode_list = [1,2,3]
RegionName_list = ["Costa", "Sierra", "Oriente"]
RegionColour_list = ["RGB(255/255,234/255,0/255)", "RGB(193/255,154/255,107/255)", "RGB(170/255,255/255,0/255)"]
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
FileIN_Mask = "Data/Raw/Ecuador_Mask_ENS/Mask.grib"
DirIN = "Data/Compute/07_Obs_Rain_Climate"
DirOUT = "Data/Plot/08a_Obs_Loc_Distr"
########################################################################################################

# Creating the output directory
DirOUT_temp = Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h"
if not os.path.exists(DirOUT_temp):
      os.makedirs(DirOUT_temp)

# Reading the domain's mask
FileIN_Mask = Git_repo + "/" + FileIN_Mask
mask = mv.read(FileIN_Mask)

# Reading the values and the location of the rainfall observations
DirIN_temp= Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h"
obs_vals = np.array([])
obs_lats = np.array([])
obs_lons = np.array([])
for RegionName in RegionName_list[0:-1]:
      FileNameIN_RainOBS_vals = "Obs_Rain_Vals_" + f"{Acc:02d}" + "h_" + DateS.strftime("%Y%m%d") + "_" + DateF.strftime("%Y%m%d") + "_" + RegionName + ".npy"
      FileNameIN_RainOBS_lats = "Obs_Rain_Lats_" + f"{Acc:02d}" + "h_" + DateS.strftime("%Y%m%d") + "_" + DateF.strftime("%Y%m%d") + "_" + RegionName + ".npy"
      FileNameIN_RainOBS_lons = "Obs_Rain_Lons_" + f"{Acc:02d}" + "h_" + DateS.strftime("%Y%m%d") + "_" + DateF.strftime("%Y%m%d") + "_" + RegionName + ".npy"
      obs_vals = np.concatenate((obs_vals, np.load(DirIN_temp + "/" + FileNameIN_RainOBS_vals)))
      obs_lats = np.concatenate((obs_lats, np.load(DirIN_temp + "/" + FileNameIN_RainOBS_lats)))
      obs_lons = np.concatenate((obs_lons, np.load(DirIN_temp + "/" + FileNameIN_RainOBS_lons)))

# Converting the observations into geopoints
obs_geo = mv.create_geo(
      type = "xyv",
      latitudes = obs_lats,
      longitudes = obs_lons,
      values = np.zeros(obs_lons.shape)
      )

# Plotting the location of the rainfall observations
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

RegionCode_list = (np.array(([0] + RegionCode_list), dtype=float) + 0.1).tolist()
mask_shading = mv.mcont(
      legend = "off",
      contour = "off",
      contour_level_selection_type = "level_list",
      contour_level_list = RegionCode_list,
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
FileOUT_loc = DirOUT_temp + "/Obs_Loc_" + f"{Acc:02d}" + "h_" + DateS.strftime("%Y%m%d") + "_" + DateS.strftime("%H")
png = mv.png_output(output_name = FileOUT_loc)
mv.setoutput(png)
mv.plot(geo_view, mask, mask_shading, obs_geo, obs_geo_contour, title)

# Plotting the distribution of the rainfall  totals
fig, ax = plt.subplots(figsize=(12, 8))
ax.hist(obs_vals, bins=np.arange(0, 501, 2), color="grey", edgecolor="red")
ax.set_title("Rainfall totals from point observations", fontsize=20, pad=30, weight="bold", color="#333333")
ax.set_xlabel("Rainfall [mm/" + str(Acc) + "h]", fontsize=16, labelpad=10, color="#333333")
ax.set_ylabel("Frequency [-]", fontsize=16, labelpad=10, color="#333333")
ax.set_xlim([0,500])
ax.set_xticks(np.arange(0, 501, 50))
ax.xaxis.set_tick_params(labelsize=16, rotation=45, color="#333333")
ax.yaxis.set_tick_params(labelsize=16, color="#333333")
ax.grid()

# Saving the distribution plot
FileOUT_distr = DirOUT_temp + "/Obs_Distr_" + f"{Acc:02d}" + "h_" + DateS.strftime("%Y%m%d") + "_" + DateS.strftime("%H")
plt.savefig(FileOUT_distr)
plt.close()

# Plotting the distribution of the rainfall  totals
fig, ax = plt.subplots(figsize=(12, 8))
ax.hist(obs_vals, bins=np.arange(0, 501, 2), color="grey", edgecolor="red")
ax.set_title("Rainfall totals from point observations", fontsize=20, pad=30, weight="bold", color="#333333")
ax.set_xlabel("Rainfall [mm/" + str(Acc) + "h]", fontsize=16, labelpad=10, color="#333333")
ax.set_ylabel("Frequency [-]", fontsize=16, labelpad=10, color="#333333")
ax.set_xlim([0,500])
ax.set_ylim([0,100])
ax.set_xticks(np.arange(0, 501, 50))
ax.xaxis.set_tick_params(labelsize=16, rotation=45, color="#333333")
ax.yaxis.set_tick_params(labelsize=16, color="#333333")
ax.grid()

# Saving the distribution plot
FileOUT_distr = DirOUT_temp + "/Obs_Distr_Zoomed_" + f"{Acc:02d}" + "h_" + DateS.strftime("%Y%m%d") + "_" + DateS.strftime("%H")
plt.savefig(FileOUT_distr)
plt.close()