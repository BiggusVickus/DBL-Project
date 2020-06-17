import os
#import magic
import urllib.request
#from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from threading import Thread
from tornado.ioloop import IOLoop
from bokeh.embed import server_document
import numpy as np  # import auxiliary library, typical idiom
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, Select, Tabs, Panel, Button, ImageURL, Slider, Grid, LinearAxis, Plot
from bokeh.models import Range1d, ColorBar, LinearColorMapper, LogColorMapper, LogTicker, Div, Select, Slider, TextInput
from bokeh.layouts import column, row, WidgetBox, layout
from bokeh.models.callbacks import CustomJS
from PIL import Image
from bokeh.server.server import Server
from bokeh.themes import Theme
from bokeh.client import pull_session
from bokeh.embed import server_session
from flask.helpers import url_for
from bokeh.models.callbacks import CustomJS
from PIL import Image
import PIL
from bokeh.models.widgets import Dropdown
from bokeh.transform import transform
import sqlite3 as sql
from os.path import dirname, join
import pandas.io.sql as psql
import random
import glob
from bokeh.transform import dodge
from math import pi

df_map = pd.read_csv('static/Visualizations/Uploads/fixation_data.csv', parse_dates=[0])

#Global Variables
stations = []
users = []
alp = 0.5 #transparency
dia = 15 #size of circles
#p_val = 0.1
#dia = (p_val * width * height) / (math.Pi)
dia2 = dia**2

src = ColumnDataSource(data = dict(url = [], x=[], y=[], timestamp=[], station=[], user=[], fixation_duration=[]))
src_heatmap = ColumnDataSource(data = dict(url = [], x=[], y=[], timestamp=[], station=[], user=[], closeness=[]))

#Select
for station in df_map['StimuliName']:
    stations.append(station)
for person in df_map['user']:
    users.append(person)
#to remove duplicates
stations = list(dict.fromkeys(stations))
users = list(dict.fromkeys(users))

selectStation = Select(title="Station:", value = '03_Bordeaux_S1.jpg', options=stations)
selectUser = Select(title='User:', value='p1', options=users)

def make_dataset():
    plot_data = df_map[(df_map['StimuliName'] == selectStation.value) & (df_map['user'] == selectUser.value)].copy()
    return plot_data

def make_dataset_heatmap():
    plot_data = df_map[(df_map['StimuliName'] == selectStation.value)].copy() # & (df_map['user'] == selectUser.value)

    plot_data = plot_data.sort_values(by=['MappedFixationPointX']).reset_index().drop('index', axis=1)#sort by x coordinate
   
    plot_data['closeness'] = 0 #the list is added to the dataframe as a new column named "closeness" and only contains 0s

    for index, row in plot_data.iterrows(): #Iterates every row one by one
        xi_val = int(row['MappedFixationPointX'])
        yi_val = int(row['MappedFixationPointY'])
        closeness_val = 0
        for index2, OtherRow in plot_data.iterrows(): #Iterates every row. 
                if index != index2: #If the row found is not the same row, the distance between the two points is calculated.
                        xi2_val = int(OtherRow['MappedFixationPointX'])
                        yi2_val = int(OtherRow['MappedFixationPointY'])
                        if (xi2_val - xi_val > dia):
                            break
                        if ( (((xi2_val - xi_val)**2 + (yi2_val - yi_val)**2 )) < dia2 ) : #Checks if distance is 'close enough'.
                            closeness_val = closeness_val + 1 
        plot_data.loc[index, 'closeness' ] = closeness_val #This line changes the actual row on the data frame  
    return plot_data


def make_plot_1(src):
    fig = figure(
        title='Scanpath', 
        plot_width = print_width, 
        plot_height = print_height, 
        x_range = (0, width), 
        y_range = (height, 0),
		x_axis_label = 'x-coordinate of fixation',
		y_axis_label = 'y-coordinate of fixation'
    )
    image = ImageURL(url = "url", x=0, y=0, w=width, h=height)
    fig.add_glyph(src, image)
    fig.line(x = 'x', y = 'y', source=src, line_width = 3)
    fig.circle(
        x='x',
        y='y', 
        size = 'fixation_duration', 
        alpha = 0.5,
        source = src
    )
    return fig

def make_plot_2(src):
    #Writing X-path
    p1 = figure(title="X path", plot_width = print_width, plot_height = print_height, x_range = (0, width))
    p1.grid.grid_line_alpha=0.3
    p1.xaxis.axis_label = 'X'
    p1.yaxis.axis_label = 'Time'
    p1.y_range.flipped = True
    p1.line(x='x', y='timestamp', source = src, line_width = 3)

    #Writing Y-path
    p2 = figure(title= "Y path", plot_width = print_width, plot_height = print_height, y_range = (height, 0))
    p2.grid.grid_line_alpha=0.3
    p2.xaxis.axis_label = 'Time'
    p2.yaxis.axis_label = 'Y'
    p2.line(x='timestamp', y='y', source = src, line_width = 3)
    
    #writing general path
    p3 = figure(title="General Path", plot_width = print_width, plot_height = print_height, x_range = (0, width), y_range = (height, 0))
    p3.grid.grid_line_alpha=0.3
    image = ImageURL(url = "url", x=0, y=0, w=width, h=height)
    p3.add_glyph(src, image)
    p3.xaxis.axis_label = 'X'
    p3.yaxis.axis_label = 'Y'
    p3.line(x='x', y='y', source = src, line_width = 3)
    return [p1, p2, p3]

def make_plot_3(src_heatmap):
    p = figure(
        plot_width = print_width,
        plot_height = print_height,
        x_range = (0, width), 
        y_range = (height, 0), #y value is manipulated to have the correct coordinates.
                                #in the dataset origin is treated to be the upper left corner. While graphing it is lower left. 
                                #Therefore we "flip" the y axis in the dataset.           
        title = 'Heatmap',
        x_axis_label = 'x coordinate',
        y_axis_label = 'y coordinate'
    )
    image = ImageURL(url="url", x = 0 , y = 0, w = width, h = height)
    #p.image_url(url = ["https://www.jelter.net/stimuli/" + selectStation.value], 
    #            x = 0 , y = 0, w = width, h = height) #'../../' + 
    p.add_glyph(src_heatmap, image)
    colors = ["#0000FF", "#0072FF", "#00FF00", "#D1FF00", "#FFC500", "#FF6C00", "#FF0000"]
    cmap = LinearColorMapper(palette=colors)
    p.ellipse(x="x", y="y", source=src_heatmap, line_color=None, 
              fill_color=transform('closeness', cmap), width=dia, height=dia, alpha=alp)
    color_bar = ColorBar(color_mapper=cmap, ticker=LogTicker(),
                     label_standoff=12, border_line_color=None, location=(0,0))
    p.add_layout(color_bar, 'right')
    return p


def update():
    new_src = make_dataset()
    new_src_heatmap = make_dataset_heatmap()
    N = new_src.size//8
    N_heatmap = new_src_heatmap.size//9
    src.data = dict(
        url = ["https://www.jelter.net/stimuli/" + selectStation.value]*N,
        x=new_src['MappedFixationPointX'],
        y=new_src['MappedFixationPointY'],
        timestamp=new_src['Timestamp'],
        station=new_src['StimuliName'],
        user=new_src['user'],
        fixation_duration=(new_src['FixationDuration']/10)
    )
    src_heatmap.data = dict(
        url = ["https://www.jelter.net/stimuli/" + selectStation.value]*N_heatmap,
        x=new_src_heatmap['MappedFixationPointX'],
        y=new_src_heatmap['MappedFixationPointY'],
        timestamp=new_src_heatmap['Timestamp'],
        station=new_src_heatmap['StimuliName'],
        user=new_src_heatmap['user'],
        closeness=new_src_heatmap['closeness']
    )

selectStation.on_change('value', lambda attr, old, new: update())
selectUser.on_change('value', lambda attr, old, new: update())

image = PIL.Image.open('static/Visualizations/Stimuli/' + selectStation.value)
width, height = image.size

ratio = width/height

print_width = int(ratio * 720)
print_height = int(720)

widgets = column(selectStation, selectUser)
plot_1 = make_plot_1(src)
plot_2 = make_plot_2(src)
plot_3 = make_plot_3(src_heatmap)
layout = layout = layout([
                [plot_2[2], plot_2[1], widgets],
                [plot_2[0]],
                [plot_1, plot_3]])
update()
curdoc().add_root(layout)