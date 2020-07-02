#Note to the examiner:
#In the future slider bars and other interactive methods will be added to allow user to customize the plotting.
#Right now 3 slider bars are present but not yet been made interactive.

import numpy as np  # import auxiliary library, typical idiom
import pandas as pd
import csv
import math
import seaborn as sns
#import urllib3 as urllib
import io
import matplotlib.pyplot as plt
from bokeh.layouts import gridplot, column, row, WidgetBox, layout
from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.io import output_file, show, curdoc
from bokeh.models import Select, Tabs, Panel, Button, ColumnDataSource, Grid, ImageURL, LinearAxis, Plot
from bokeh.models import Range1d, ColorBar, LinearColorMapper, LogColorMapper, LogTicker, Div, Select, Slider, TextInput
from bokeh.models.callbacks import CustomJS
from PIL import Image
import PIL
from bokeh.models.widgets import Dropdown
from bokeh.transform import transform
import sqlite3 as sql
from os.path import dirname, join
import pandas.io.sql as psql
sns.set()  # set Seaborn defaults

#load dataset
df_paths = pd.read_csv('Uploads/fixation_data.csv', parse_dates=[0])

#Global Variables
stations = []

src = ColumnDataSource(data = dict(url = [], x=[], y=[], timestamp=[], station=[], user=[], closeness=[]))

df_paths = df_paths.astype({'Timestamp': int, 'StimuliName': str, 'FixationIndex': float, 'FixationDuration': float, 
                            'MappedFixationPointX': int, 'MappedFixationPointY' : int, 'user': str, 'description': str})

alp = 0.5 #transparency
dia = 15 #size of circles
#p_val = 0.1
#dia = (p_val * width * height) / (math.Pi)
dia2 = dia**2

#Choosing the data we want
def make_dataset():
    plot_data = df_paths[(df_paths['StimuliName'] == selectStation.value)].copy() # & (df_paths['user'] == selectUser.value)

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
    image = PIL.Image.open('static/Visualizations/Stimuli/'+selectStation.value)
    width, height = image.size
    ratio = width/height
    print_width = int(ratio * 360)
    print_height = int(360)
    plot_data['width'] = width
    plot_data['height'] = height
    return plot_data

#making the plot
def make_plot(src):
    p = figure(
        plot_width = print_width,
        plot_height = print_height,
        x_range = (0, 1900), 
        y_range = (1200, 0), #y value is manipulated to have the correct coordinates.
                                #in the dataset origin is treated to be the upper left corner. While graphing it is lower left. 
                                #Therefore we "flip" the y axis in the dataset.           
        title = 'Heatmap',
        x_axis_label = 'x coordinate',
        y_axis_label = 'y coordinate'
    )
    image = ImageURL(url="url", x = 0 , y = 0, w = 'w', h = 'h')
    #p.image_url(url = ["https://www.jelter.net/stimuli/" + selectStation.value], 
    #            x = 0 , y = 0, w = width, h = height) #'../../' + 
    p.add_glyph(src, image)
    colors = ["#0000FF", "#0072FF", "#00FF00", "#D1FF00", "#FFC500", "#FF6C00", "#FF0000"]
    cmap = LinearColorMapper(palette=colors)
    p.ellipse(x="x", y="y", source=src, line_color=None, 
              fill_color=transform('closeness', cmap), width=dia, height=dia, alpha=alp)
    color_bar = ColorBar(color_mapper=cmap, ticker=LogTicker(),
                     label_standoff=12, border_line_color=None, location=(0,0))
    p.add_layout(color_bar, 'right')
    return p

#Select
for station in df_paths['StimuliName']:
    stations.append(station)
stations = list(dict.fromkeys(stations))

selectStation = Select(title="Station:", value = '01_Antwerpen_S1.jpg', options=stations)


#Update
def update():
    new_src = make_dataset()
    N = new_src.size//9
    src.data = dict(
        url = ["https://www.jelter.net/stimuli/" + selectStation.value]*N,
        x=new_src['MappedFixationPointX'],
        y=new_src['MappedFixationPointY'],
        w=new_src['width'],
        h=new_src['height'],
        timestamp=new_src['Timestamp'],
        station=new_src['StimuliName'],
        user=new_src['user'],
        closeness=new_src['closeness']
    )

selectStation.on_change('value', lambda attr, old, new: update())
selections = [selectStation]

image = PIL.Image.open('Stimuli/' + selectStation.value)
width, height = image.size

ratio = width/height

print_width = int(ratio * 720)
print_height = int(720)

widgets = column(selectStation)
plot = make_plot(src)
layout = row(plot, widgets)
update()
curdoc().add_root(layout)