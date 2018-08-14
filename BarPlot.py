"""
	twitterFetchTweets.py - generate a barplot
"""

from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.layouts import row, widgetbox,layout
from bokeh.io import curdoc
from bokeh.models import HoverTool


def plot(classFrequencies):
	"""Generate a bar plot(5 classes) based on the given data.
	
	:param classFrequencies: dicitioanry with class and frequency
	:returns: returns the barplot figure
	:rtype: bokeh.plotting.figure.
	
	"""
	classes = list(classFrequencies.keys())
	classes.sort()
	frequencies = [classFrequencies[x]  for x in classes]
	hovers = classes.copy()
	colors = ["#B22222", "#FA8072", "yellow", "#7CFC00", "green"]

	source = ColumnDataSource(data=dict(classes=classes, frequencies=frequencies, color=colors))

	barPlot = figure(x_range=classes, plot_height=350, toolbar_location=None, title="Tweets Distribution")
	barPlot.vbar(x='classes', top='frequencies', width=0.9, source=source, legend="classes",
       line_color='black', color="color", alpha=0.5)

	barPlot.xgrid.grid_line_color = None
	barPlot.y_range.start = 0
	barPlot.y_range.end = max(frequencies)+10
	barPlot.legend.orientation = "horizontal"
	barPlot.legend.location = "top_center"
	barPlot.xaxis.axis_label = "Ratings"
	barPlot.yaxis.axis_label = "Percentage of Tweets"

	barPlot.add_tools(HoverTool( tooltips=[("Rating : ", "@classes")]))

	return barPlot
