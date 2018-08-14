"""
////////////////////////////////////////////////////////////////////////////////////////////
// gapminderplot.py - Generates a word frequecies graph                                   //
//                                                                                        //
////////////////////////////////////////////////////////////////////////////////////////////
"""

import pandas as pd
import numpy as np

from bokeh.core.properties import field
from bokeh.layouts import column,layout,row,widgetbox
from bokeh.models import (
    ColumnDataSource, HoverTool, SingleIntervalTicker, Slider, Button, Label,
    CategoricalColorMapper,
)
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from sklearn.utils import shuffle
from bokeh.layouts import column

def createGapMinder(pds, features, curdoc):
    """Generates a gap minder plot.

    :param pds: list of dicitionaries.
    :param features: the list of features
    :param curdoc: The curdoc instance
    :returns: The gapminder plot and a slider
    :rtype: bokeh.layouts.row, bokeh.models.Slider

    """
    
    mysource = ColumnDataSource(data=pds[0])
    myplot = figure(x_range=(0, 10), y_range=(0, 10), title='Word Frequencies with Ratings', plot_height=300)
    myplot.xgrid.grid_line_color = None
    myplot.ygrid.grid_line_color = None
    myplot.toolbar.logo = None
    myplot.toolbar_location = None
    myplot.xaxis.axis_label = "Hover on Circles to see the words"
    
    color_mapper = CategoricalColorMapper(palette=['red','blue',"green","yellow","black"], factors=["1","2","3","4","5"])
    myplot.circle(
        x="xval",
        y="yval",
        size="freq",
        source=mysource,
        fill_color={'field': 'sentiment', 'transform': color_mapper},
        fill_alpha=0.8,
        line_color='#7c7e71',
        line_width=0.5,
        line_alpha=0.2,
        legend=field('sentiment')
    )
    myplot.add_tools(HoverTool(tooltips="@word", show_arrow=False, point_policy='follow_mouse'))
    myslider = Slider(start=0, end=2, value=0, step=1, title=features[0])
    mybutton = Button(label='Play', width=60)
    
    
    
    
    def animate():
        """The slider animate function

        :returns: nothing
        :rtype: None

        """
        global callback_id
        if mybutton.label == 'Play' :
            mybutton.label = 'Pause'
            callback_id = curdoc.add_periodic_callback(animate_update, 1000)
            
        else:
            mybutton.label = 'Play'
            curdoc.remove_periodic_callback(callback_id)
            
    def slider_update(attrname, old, new):
        """The slider update function
        """
        val = myslider.value
        myslider.title = features[val]
        mysource.data = pds[val]

    def animate_update():
        val = myslider.value + 1
        if val > 2:
            val = 0
        myslider.value = val

    myslider.on_change('value', slider_update)
    mybutton.on_click(animate)
    inputs = widgetbox(myslider,mybutton)
    r = row(myplot,inputs)
    # layout = layout([[myplot], [myslider, mybutton]], sizing_mode='fixed')
    return r, myslider