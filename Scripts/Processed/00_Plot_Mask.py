import os
import numpy as np
import metview as mv

###################################################################
# CODE DESCRIPTION
# 00_Plot_Mask.py plots the map that shows the mask for the domain of interest. 
# Note: runtime negligible.

# INPUT PARAMETERS DESCRIPTION
# CornersDomain_list (list of floats): coordinates [N/E/S/W] of the domain to plot.
# RegionCode_list (list of integers): codes for the domain's regions to consider. 
# RegionName_list (list of strings): names for the domain's regions to consider.
# RegionColour_list (list of strings): rgb-codes for the domain's regions to consider.
# Git_repo (string): repository's local path.
# FileIN (string): relative path of the file containing the domain's mask.
# DirOUT (string): relative path where to store the mask's map plot.

# INPUT PARAMETERS
CornersDomain_list = [2,-81.5,-5.5,-74.5]
RegionCode_list = [1,2,3]
RegionName_list = ["La Costa", "La Sierra", "El Oriente"]
RegionColour_list = ["RGB(255/255,234/255,0/255)", "RGB(193/255,154/255,107/255)", "RGB(170/255,255/255,0/255)"]
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
FileIN = "Data/Raw/Ecuador_Mask_ENS/Mask.grib"
DirOUT = "Data/Plot/00_Mask"
###################################################################


# Reading the domain's mask and extracting the coordinates of the domain's points
FileIN = Git_repo + "/" + FileIN
mask = mv.read(FileIN)
mask_vals = mv.values(mask)
mask_lats = mv.latitudes(mask)
mask_lons = mv.longitudes(mask)
mask_vals_domain = mv.filter(mask_vals, mask_vals>0)
mask_lats_domain = mv.filter(mask_lats, mask_vals>0)
mask_lons_domain = mv.filter(mask_lons, mask_vals>0)

# Convert the coordinates of the domain's points into geopoints
mask_points_geo = mv.create_geo(
      type = "xyv",
      latitudes = mask_lats_domain,
      longitudes = mask_lons_domain,
      values = mask_vals_domain,
)

# Plotting the domain's mask
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

mask_points_symbol = mv.msymb(
      legend = "off",
      symbol_type = "marker",
      symbol_table_mode = "on",
      symbol_outline = "on",
      symbol_min_table = [0.1],
      symbol_max_table = [3.1],
      symbol_colour_table = "charcoal",
      symbol_marker_table = 15,
      symbol_height_table = 0.3
      )

no_title = mv.mtext(
      text_line_1 = " "
      )

# Saving the plot
print("Saving the map plot ...")
DirOUT= Git_repo + "/" + DirOUT
if not os.path.exists(DirOUT):
      os.makedirs(DirOUT)
FileOUT = DirOUT + "/Mask"
png = mv.png_output(output_name = FileOUT)
mv.setoutput(png)
mv.plot(geo_view, mask, mask_shading, mask_points_geo, mask_points_symbol, no_title)