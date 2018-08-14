"""
////////////////////////////////////////////////////////////////////////////////////////////
// main.py - This is the serveer file. It contains functions to                           //
//              respond to user inputs.                                                   //
////////////////////////////////////////////////////////////////////////////////////////////
"""
import DonutPlot, BarPlot, gapminderplot, pickle, twitterFetchTweets, Classification, wordCloud
import pandas as pd
from bokeh.layouts import column, widgetbox, row, layout
from bokeh.models import Button, HoverTool, ColumnDataSource
from bokeh.models.glyphs import AnnularWedge
from bokeh.models.widgets import Div, Select, TextInput
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc
from math import radians
import numpy as np
import pprint as pp


analysis = {}
wedgeList = []
secondRow = row()
thirdRow = row()
donutCallBackId = None
features = ["overall","battery", "camera"]
phoneName = None
PhoneSpecs = None

def initialize(curdoc, newVal=""):
  """Initialize the document.

  :param curdoc: The curdoc() to append divs etc
  :param newVal: The model name 
  :returns: returns Nothing
  :rtype: None

  """

  global phoneName, PhoneSpecs
  phoneName = TextInput(title="SmartPhone Model Name", value=newVal)
  phoneName.on_change("value", lambda attr, old, new: updatePhoneModelInput())
  
  PhoneSpecs = Select(title="Select Features", options=features, value=features[0])
  PhoneSpecs.on_change("value", lambda attr, old, new: updatePhoneSpecs())
  
  
  firstRow = row(column(phoneName, PhoneSpecs))
  curdoc.add_root(firstRow)
  curdoc.title = "SmartPhone Review"


def updatePhoneSpecs():
  """Called when a phone specification (like camera, battery etc) is selected.

  :returns: returns nothing
  :rtype: None

  """
  global donutCallBackId
  print(PhoneSpecs.value)
  f = PhoneSpecs.value
  slider.value = features.index(f)
  if len(curdoc().roots) > 1:
    curdoc().remove_root(curdoc().roots[3])
  if f == "overall":
    donutPlot, wedgeList = DonutPlot.plot(analysis[f]["donutPlot"],  curdoc(), analysis[f]["averageRating"])
  else:
    donutPlot, wedgeList = DonutPlot.plot(analysis[f]["donutPlot"],  curdoc(),analysis[f]["averageRating"+f])
  barPlot = BarPlot.plot(analysis[f]["barPlot"])
  secondRow = row(barPlot, donutPlot)
  curdoc().add_root(secondRow)
  

def updatePhoneModelInput():
  """Called when new model input is given. Calls required functions to get the plots.

  :returns: returns Nothing
  :rtype: none

  """
  global analysis, wedgeList, secondRow, thirdRow,slider, donutCallBackId
  print(phoneName.value)
  analysis = None
  # nimg = Div(text="<img class='theImage' src='SmartPhoneReview/static/images/loading.gif' style=''>")
  t = phoneName.value
  print(len(curdoc().roots))
  if len(curdoc().roots) > 1:
    curdoc().clear()
    initialize(curdoc(), str(phoneName.value))
  # curdoc().add_root(nimg)



  analysis = Classification.classify(str(phoneName.value))
  
  dPlot = analysis["overall"]["donutPlot"].copy()
  
  donutPlot, wedgeList = DonutPlot.plot(dPlot, curdoc(),analysis["overall"]["averageRating"])

  barPlot = BarPlot.plot(analysis["overall"]["barPlot"])
  
  secondRow = row(barPlot, donutPlot)
  wc = wordCloud.wordCloud(phoneName.value, analysis["overall"]["tweets"])
  gapMinder, slider = gapminderplot.createGapMinder(analysis["gapminderplot"], features, curdoc())

  if len(phoneName.value ) > 10:
    t = t.split()[0]
  
  img = Div(text="<img class='theImage' src='SmartPhoneReview/static/images/"+"".join(t)+".png' style=''>")
  curdoc().add_root(img)
  curdoc().add_root(gapMinder)
  curdoc().add_root(secondRow)

initialize(curdoc())


