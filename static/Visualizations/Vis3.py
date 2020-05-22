import numpy as np  # import auxiliary library, typical idiom
import pandas as pd
import csv
import math
import seaborn as sns
import matplotlib.pyplot as plt
from bokeh.layouts import gridplot, column, row, WidgetBox, layout
from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.io import output_file, show, curdoc
from bokeh.models import Select, Tabs, Panel, Button, ColumnDataSource, Grid, ImageURL, LinearAxis, Plot
from bokeh.models import Range1d, ColorBar, LinearColorMapper, LogColorMapper, LogTicker
from bokeh.models.callbacks import CustomJS
from PIL import Image
from bokeh.models.widgets import Dropdown
from bokeh.transform import transform
sns.set()  # set Seaborn defaults

#load dataset
df_paths = pd.read_csv('Uploads/fixation_data.csv', parse_dates=[0])
#C:\Users\20190756\Documents\GitHub\DBL-Project\static\Visualizations\Uploads\fixation_data.csv

#Global Variables
#users = []
stations = []

src = ColumnDataSource(data = dict(x=[], y=[], timestamp=[], station=[], user=[], closeness=[]))

df_paths = df_paths.astype({'Timestamp': int, 'StimuliName': str, 'FixationIndex': float, 'FixationDuration': float, 
                            'MappedFixationPointX': int, 'MappedFixationPointY' : int, 'user': str, 'description': str})

#Choosing the data we want
def make_dataset():
    plot_data = df_paths[(df_paths['StimuliName'] == selectStation.value)].copy() # & (df_paths['user'] == selectUser.value)
    length = len(plot_data.index) #number of rows in the dataframe is calculated
    list_closeness = [0] * length #A list is created such that: number of 0s = number of rows
    plot_data['closeness'] = list_closeness #the list is added to the dataframe as a new column named "closeness" and only contains 0s

    close = 15
    #close = (p*w*h) / (math.Pi* n**t)
    for index, row in plot_data.iterrows(): #Iterates every row one by one
        closeness_val = int(row['closeness'])
        xi_val = int(row['MappedFixationPointX'])
        yi_val = int(row['MappedFixationPointY'])
        for index2, OtherRow in plot_data.iterrows(): #Iterates every row. 
            if index != index2: #If the row found is not the same row, the distance between the two points is calculated.
                xi2_val = int(OtherRow['MappedFixationPointX'])
                yi2_val = int(OtherRow['MappedFixationPointY'])
                if ( (((xi2_val - xi_val)**2 + (yi2_val - yi_val)**2 )) < close**2 ) : #Checks if distance is 'close enough'.
                    closeness_val = closeness_val + 1 
                    plot_data.loc[index, 'closeness' ] = closeness_val #This line changes the actual row on the data frame
                else: closeness_val == closeness_val
    return plot_data

#making the plot
def make_plot(src):
    p = figure(
        plot_width=990,
        plot_height=720,
        x_range=(0,1500), 
        y_range=(0,1500),
        title = 'Heatmap',
        x_axis_label = 'x coordinate',
        y_axis_label = 'y coordinate'
    )

    #p.image_url(url = ['images/03_Bordeaux_S1.jpg'], x = 0 , y = 1500, w = 1500 , h = 1500)
    #image = PIL.Image.open("sample.png")
    #width, height = image.size

    #dropwdown = ['hello', 'goodbye', ...]
    #x = select.dropwdown
    #image name = str(images/) + str(x)
    p.image_url(url = [srt(image_name)], x = 0 , y = 1500, w = 1500 , h = 1500)

    colors = ["#0000FF", "#0072FF", "#00FF00", "#D1FF00", "#FFC500", "#FF6C00", "#FF0000"]
    cmap = LinearColorMapper(palette=colors)
    wid = 15
    hei = wid*11/8
    p.ellipse(x="x", y="y", source=src, line_color=None, 
              fill_color=transform('closeness', cmap), width=wid, height=hei)
    color_bar = ColorBar(color_mapper=cmap, ticker=LogTicker(),
                     label_standoff=12, border_line_color=None, location=(0,0))
    p.add_layout(color_bar, 'right')

    return p

#Select
for station in df_paths['StimuliName']:
    stations.append(station)
#for person in df_paths['user']:
#    users.append(person)
#to remove duplicates
stations = list(dict.fromkeys(stations))
#users = list(dict.fromkeys(users))

selectStation = Select(title="Station:", value = '09_Tokyo_S1.jpg', options=stations)
#selectUser = Select(title='User:', value='p1', options=users)

image_name = str('static/Stimuli/') + str(selectStation.value)
#C:\Users\20190756\Documents\GitHub\DBL-Project\static\Stimuli

#Update
def update():
    new_src = make_dataset()
    src.data = dict(
        x=new_src['MappedFixationPointX'],
        y=new_src['MappedFixationPointY'],
        timestamp=new_src['Timestamp'],
        station=new_src['StimuliName'],
        user=new_src['user'],
        closeness=new_src['closeness']
    )

selectStation.on_change('value', lambda attr, old, new: update())
#selectUser.on_change('value', lambda attr, old, new: update())
selections = [selectStation] #, selectUser

#widgets = column(*selections, width = 320, height = 200)
widgets = column(selectStation) #, selectUser
plot = make_plot(src)
layout = row(plot, widgets)
update()
curdoc().add_root(layout)