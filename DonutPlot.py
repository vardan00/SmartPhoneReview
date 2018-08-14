"""
    DonutPlot.py - This file provides necessary functions to create a                      
                   donut plot along with its animation.                                    
"""

from random import random
from bokeh.layouts import column, widgetbox
from bokeh.models import Button, HoverTool
from bokeh.models.glyphs import AnnularWedge
from bokeh.models.widgets import Div
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc
from math import radians

annularWedgesList = None

def update_donut():
    global annularWedgesList
    for wl in annularWedgesList:
        wl.start_angle-=.005
        wl.end_angle-=0.005


def plot(classPercentages, curdoc, rating=4.8):
    """Function to generate donut plot. Input format of the plot 
    
    :param classPercentages: Dictionary representing class and percentage 
    :param rating: rating to be displayed.
    :returns: returns a donut figure and list of annular wedges.
    :rtype: bokeh.plotting.figure, bokeh.models.glyphs.AnnularWedge

    """
    global annularWedgesList
    donutPlot = figure(width=400, height=350, x_range=(-1.5,3), y_range=(-1,1), title="Average Rating")
    donutPlot.xgrid.grid_line_color = None
    donutPlot.ygrid.grid_line_color = None
    donutPlot.axis.visible = None
    donutPlot.axis.visible = None
    donutPlot.toolbar.logo = None
    donutPlot.toolbar_location = None
    donutPlot.legend.location=(0, -8)
    classes = list(classPercentages.keys())
    classes.sort()
    colors = {"negative":"#B22222", "neutral":"yellow",  "positive":"green"}


    annularWedgesList = []
    start_angle = 0
    for Class in classes:
        if classPercentages[Class] == 0:
            continue
        
        end_angle = (classPercentages[Class]*360)/100.0
        annularWedgesList.append(AnnularWedge(x=0, y=0, inner_radius=1, outer_radius=0.5,
                                            start_angle=radians(start_angle), end_angle=radians(start_angle + end_angle-2),
                                            fill_color=colors[Class],fill_alpha=0.6,line_width=1,
                                            line_alpha=0.3, line_color=colors[Class]))
        
        donutPlot.annular_wedge(x=[0], y=[0], inner_radius=0, outer_radius=0.0,
                                start_angle=radians(start_angle), end_angle=radians(start_angle + end_angle-2),
                                color=colors[Class], alpha=0.5,line_width=1,line_alpha=0, line_color=colors[Class],
                                legend="class "+Class+" - "+str(classPercentages[Class])+"%")
        
        start_angle = end_angle+start_angle

    for annularWedge in annularWedgesList:
        donutPlot.add_glyph(annularWedge)

    donutPlot.wedge(x=[0], y=[0], radius=0.48, start_angle=radians(0), end_angle=radians(360), 
                    color="orange", alpha=1, direction="clock")

    donutPlot.text(x=[0], y=[0], text=[str(rating)],text_baseline="middle",
                 text_align="center", text_font_size="30pt", alpha=1, text_color="black")
    
 
    curdoc.add_periodic_callback(update_donut, 10)
 
    return (donutPlot, annularWedgesList)
