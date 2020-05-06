#import matplotlib as mlp
#import matplotlib.pyplot as plt 
#import seaborn as sns 
import bokeh as bk 
from bokeh.plotting import figure, show, curdoc
from bokeh.io import output_file, output_notebook, show 
from bokeh.models import ColumnDataSource, Select, RadioButtonGroup
from bokeh.layouts import row, column, gridplot, widgetbox
from bokeh.models.widgets import Tabs, Panel

import sqlite3 as sql
import numpy as np
import pandas as pd
#output file to HTML
#output_file('DBLvis1.html')

#read csv file
df_map = pd.read_csv('Uploads/fixation_data.csv', parse_dates=[0])

#create ColumnDataSource
source_city = ColumnDataSource(data = dict(x=[], y=[], timestamp=[], station=[], user=[], fixation_duration=[]))

#Global variables
stations = []
users = []

#create city select widget
for station in df_map['StimuliName']:
    stations.append(station)
#to remove duplicates
stations = list(dict.fromkeys(stations))

select_city = Select(
    title = 'Choose city', 
    value = '01_Antwerpen_S1.jpg', 
    options = stations
)

#create user select widget
for user in df_map['user']:
    users.append(user)
users = list(dict.fromkeys(users))

select_user = Select(
    title = 'Choose user',
    value = 'p1',
    options = users
)

#create figure and graph (scanpath)
def make_plot(src):
    fig = figure(
        title='Scanpath', 
        plot_width = 900, 
        plot_height = 600, 
        x_range = (0, 1900), 
        y_range = (0, 1200)
    )
    fig.line(x = 'x', y = 'y', source=source_city)
    fig.circle(
        x='x',
        y='y', 
        size = 'fixation_duration', 
        alpha = 0.5,
        source = source_city
    )
    return fig

def make_dataset():
    plot_data = df_map[(df_map['StimuliName'] == select_city.value) & (df_map['user'] == select_user.value)].copy()
    return plot_data

def update():
    new_src = make_dataset()
    source_city.data = dict(
        x=new_src['MappedFixationPointX'],
        y=new_src['MappedFixationPointY'],
        timestamp=new_src['Timestamp'],
        station=new_src['StimuliName'],
        user=new_src['user'],
        fixation_duration=(new_src['FixationDuration']/10)
    )

#update graph on selected changes
select_city.on_change('value', lambda attr, old, new: update())
select_user.on_change('value', lambda attr, old, new: update())

#make layout for the graph and selectors
choices = column(select_city, select_user)
city_map = make_plot(source_city)
layout = row(city_map, choices)

update()
curdoc().add_root(layout)