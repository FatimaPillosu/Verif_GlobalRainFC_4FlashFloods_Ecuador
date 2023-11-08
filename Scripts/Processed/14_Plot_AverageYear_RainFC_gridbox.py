import os
import math
import metview as mv

##################################################################################
# CODE DESCRIPTION
# 14_Plot_AverageYear_RainFC_gridbox.py plots a map that shows the annual rainall average for 
# different accumulation periods.
# Note: runtime code negligible.

# INPUT PARAMETERS DESCRIPTION
# Acc (number, in hours): rainfall accumulation to consider.
# StepF_list (list of integer, in hours): list of final steps of the accumulation period.
# CornersDomain_list (list of floats): coordinates [N/E/S/W] of the domain to plot.
# SystemFC_list (list of strings): list of forecasting systems to consider.
# Git_repo (string): repository's local path.
# DirIN (string): relative path containing the annual rainfall average from forecasts.
# DirOUT (string): relative path of the plots containing the annual rainfall average.

# INPUT PARAMETERS
Acc = 12
StepF_list = [60, 72]
CornersDomain_list = [2,-81.5,-5.5,-74.5] 
SystemFC_list = ["ENS", "ecPoint"]
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
DirIN = "Data/Compute/13_AverageYear_RainFC_gridbox"
DirOUT = "Data/Plot/14_AverageYear_RainFC_gridbox"
##################################################################################


# Plotting the annual rainfall average for a specific accumulation period
for StepF in StepF_list:

      AccPerF = int(math.modf(StepF/24)[0] * 24)

      # Plotting the annual rainfall average for a specific forecasting system
      for SystemFC in SystemFC_list:
            
            # Reading the annual rainfall average
            FileIN_FC = Git_repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h/AverageYear_RainFC_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + f"{StepF:03d}" + ".grib"
            tp_fc = mv.read(FileIN_FC)

            # Plotting the annual rainfall average
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

            fc_contouring = mv.mcont(
                  legend = "on",
                  contour = "off",
                  contour_level_selection_type = "level_list",
                  contour_level_list = [0,0.5,2,5,10,20,30,40,50,60,80,100,125,150,200,300,500,5000],
                  contour_label = "off",
                  contour_shade = "on",
                  contour_shade_colour_method = "list",
                  contour_shade_method = "area_fill",
                  contour_shade_colour_list = ["white","RGB(0.75,0.95,0.93)","RGB(0.45,0.93,0.78)","RGB(0.07,0.85,0.61)","RGB(0.53,0.8,0.13)","RGB(0.6,0.91,0.057)","RGB(0.9,1,0.4)","RGB(0.89,0.89,0.066)","RGB(1,0.73,0.0039)","RGB(1,0.49,0.0039)","red","RGB(0.85,0.0039,1)","RGB(0.63,0.0073,0.92)","RGB(0.37,0.29,0.91)","RGB(0.04,0.04,0.84)","RGB(0.042,0.042,0.43)","RGB(0.45,0.45,0.45)"]
                  )

            legend = mv.mlegend(
                  legend_text_colour = "charcoal",
                  legend_text_font = "arial",
                  legend_text_font_size = 0.6,
                  legend_entry_plot_direction = "column",
                  legend_automatic_posiution = "right",
                  legend_box_blanking = "on",
                  legend_entry_text_width = 30
                  )
            
            title = mv.mtext(
                  text_line_count = 2,
                  text_line_1 = "Annual rainfall average for " + SystemFC + " and (t+"  f"{StepF:02d}" + "), and location of rain gauges",
                  text_line_2 = " ",
                  text_font = "sansserif",
                  text_colour = "charcoal",
                  text_font_size = 0.6,
                  text_font_style = "bold"
                  )

            # Saving the plots
            DirOUT_temp= Git_repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h"
            FileNameOUT_temp = "AverageYear_RainFC_LocOBS_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + f"{StepF:02d}"
            if not os.path.exists(DirOUT_temp):
                  os.makedirs(DirOUT_temp)
            png = mv.png_output(output_name = DirOUT_temp + "/" + FileNameOUT_temp)
            mv.setoutput(png)
            mv.plot(geo_view, tp_fc, fc_contouring, legend, title)