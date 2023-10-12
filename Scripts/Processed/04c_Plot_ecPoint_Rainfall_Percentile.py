import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import metview as mv

#######################################################################################################################
# CODE DESCRIPTION
# 04c_Plot_ecPoint_Rainfall_Percentile.py plots a map that shows rainfall totals associated with a specific percentile.
# Note: runtime negligible.

# INPUT PARAMETERS DESCRIPTION
# Date (date, in YYYY format): date to plot.
# Acc (number, in hours): accumulation to consider.
# EFFCI (integer, from 1 to 10): EFFCI index.
# RegionCode_list (list of integers): codes for the domain's regions to consider. 
# RegionName_list (list of strings): names for the domain's regions to consider.
# RegionColour_list (list of strings): rgb-codes for the domain's regions to consider.
# Git_repo (string): repository's local path.
# FileIN_Mask (string): relative path of the file containing the domain's mask.
# FileIN (string): relative path of the file containing the clean point flood reports.
# DirOUT (string): relative path where to store the map plots.

# INPUT PARAMETERS
BaseDate = datetime(2020,2,28,0)
BaseTime = 0
StepF = 12
Acc = 12
Perc_list = [50, 85, 99]
CornersDomain_list = [2,-81.5,-5.5,-74.5] 
SystemFC_list = ["ENS", "ecPoint"]
Git_repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Verif_Flash_Floods_Ecuador"
DirIN = "Data/Raw/FC"
DirOUT = "Data/Plot/04c_ecPoint_Rainfall_Percentile"
#######################################################################################################################


StepS = StepF - Acc

for SystemFC in SystemFC_list:

    for Perc in Perc_list:
    
        print("Plotting the " + str(Perc) + "th percentile for " + SystemFC)

        if SystemFC == "ENS":
            FileIN1 = Git_repo + "/" + DirIN + "/" + SystemFC + "/" + BaseDate.strftime("%Y%m%d") + f"{BaseTime:02d}" + "/tp_" + BaseDate.strftime("%Y%m%d") + "_" + f"{BaseTime:02d}" + "_" + f"{StepS:03d}" + ".grib"
            FileIN2 = Git_repo + "/" + DirIN + "/" + SystemFC + "/" + BaseDate.strftime("%Y%m%d") + f"{BaseTime:02d}" + "/tp_" + BaseDate.strftime("%Y%m%d") + "_" + f"{BaseTime:02d}" + "_" + f"{StepF:03d}" + ".grib"
            tp1 = mv.read(FileIN1)
            tp2 = mv.read(FileIN2)
            tp = (tp2-tp1) * 1000
            tp_perc = mv.percentile(interpolation = "linear", percentiles = Perc, data = tp)
        elif SystemFC == "ecPoint":
            FileIN = Git_repo + "/" + DirIN + "/" + SystemFC + "/" + BaseDate.strftime("%Y%m%d") + f"{BaseTime:02d}" + "/Pt_BC_PERC_" + f"{Acc:03d}" + "_" + BaseDate.strftime("%Y%m%d") + "_" + f"{BaseTime:02d}" + "_" + f"{StepF:03d}" + ".grib"
            tp = mv.read(FileIN)
            tp_perc = tp[Perc-1]
            
            
        # Plotting the maps
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

        contouring = mv.mcont(
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

        ValidityDateS = BaseDate + timedelta(hours = (BaseTime + StepS))
        DayVS = ValidityDateS.strftime("%d")
        MonthVS = ValidityDateS.strftime("%B")
        YearVS = ValidityDateS.strftime("%Y")
        TimeVS = ValidityDateS.strftime("%H")
        ValidityDateF = BaseDate + timedelta(hours = (BaseTime + StepF))
        DayVF = ValidityDateF.strftime("%d")
        MonthVF = ValidityDateF.strftime("%B")
        YearVF = ValidityDateF.strftime("%Y")
        TimeVF = ValidityDateF.strftime("%H")
        title_plot1 = SystemFC + " Rainfall - " + str(Perc) + "th percentile (mm/" + str(Acc) + "h)"
        title_plot2 = "RUN: " + BaseDate.strftime("%d") + " " + BaseDate.strftime("%B") + " " + BaseDate.strftime("%Y") + ", " + f"{BaseTime:02d}" + " UTC" + " " + "(t+" + str(StepS) + ", t+" + str(StepF) + ")"
        title_plot3 = "VT: " + DayVS + " " + MonthVS + " " + YearVS + " " + TimeVS + " UTC - " + DayVF + " " + MonthVF + " " + YearVF + " " + TimeVF  + " UTC"          
        title = mv.mtext(
            text_line_count = 4,
            text_line_1 = title_plot1,
            text_line_2 = title_plot2,
            text_line_3 = title_plot3,
            text_line_4 = " ",
            text_colour = "charcoal",
            text_font = "arial",
            text_font_size = 0.6
            )
        
        # Saving the maps
        DirOUT_temp = Git_repo + "/" + DirOUT
        if not os.path.exists(DirOUT_temp):
            os.makedirs(DirOUT_temp)
        FileOUT = DirOUT_temp + "/" + SystemFC + "_Rainfall_" + str(Perc) + "th_" + BaseDate.strftime("%Y%m%d") + "_" + f"{BaseTime:02d}" + "_" + f"{StepF:03d}"
        png = mv.png_output(output_name = FileOUT)
        mv.setoutput(png)
        mv.plot(tp_perc, geo_view, contouring, legend, title)