import bokeh as bk 
from bokeh.plotting import figure, show, curdoc
from bokeh.io import output_file, output_notebook, show 
from bokeh.models import ColumnDataSource, Select, RadioButtonGroup, Plot, ImageURL
from bokeh.layouts import row, column, gridplot, widgetbox
from bokeh.models.widgets import Tabs, Panel
import seaborn as sns
import PIL
from PIL import Image

import sqlite3 as sql
import pandas as pd 
import numpy as np
#output file to HTML
#output_file('DBLvis1.html')

#read csv file
df_map = pd.read_csv('Uploads/fixation_data.csv', parse_dates=[0])

#create ColumnDataSource
src = ColumnDataSource(data = dict(url=[], x=[], y=[], w=[], h=[], print_w=[], print_h=[], 
    timestamp=[], station=[], user=[], fixation_duration=[]))

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

#city = select_city.value

#create figure and graph (scanpath)
def make_plot(src):
    fig = figure(
        title='Scanpath', 
        plot_width = print_width, 
        plot_height = print_height, 
        x_range = (0, 1900), 
        y_range = (height, 0),
		x_axis_label = 'x-coordinate of fixation',
		y_axis_label = 'y-coordinate of fixation',
    )
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None
    image = ImageURL(url = "url", x=0, y=0, w='w', h='h')
    fig.add_glyph(src, image)
    fig.line(x = 'x', y = 'y', source=src, width = 3, color = 'navy', 
        muted_alpha = 0.1, legend_label = 'Disable/Enable graph')
    fig.circle(
        x='x', y='y', size = 'fixation_duration', color = 'navy', 
        muted_alpha = 0.1, legend_label = 'Disable/Enable graph',
        alpha = 0.5, source = src
    )
    fig.legend.click_policy = 'mute'
    return fig

def make_dataset():
    plot_data = df_map[(df_map['StimuliName'] == select_city.value) & (df_map['user'] == select_user.value)].copy()

    image = PIL.Image.open('Stimuli/'+select_city.value)
    width, height = image.size
    ratio = width/height
    print_width = int(ratio * 720)
    print_height = int(720)

    plot_data['width'] = width
    plot_data['height'] = height
    plot_data['print_width'] = print_width
    plot_data['print_height'] = print_height
    return plot_data

def update():
    new_src = make_dataset()
    N = len(new_src.index)
    src.data = dict(
        url = ["https://www.jelter.net/stimuli/"+select_city.value]*N,
        x=new_src['MappedFixationPointX'],
        y=new_src['MappedFixationPointY'],
        w=new_src['width'],
        h=new_src['height'],
        print_w=new_src['print_width'],
        print_h=new_src['print_height'],
        timestamp=new_src['Timestamp'],
        station=new_src['StimuliName'],
        user=new_src['user'],
        fixation_duration=(new_src['FixationDuration']/10)
    )

image = PIL.Image.open('Stimuli/'+select_city.value)
width, height = image.size
ratio = width/height

print_width = int(ratio * 720)
print_height = int(720)

#update graph on selected changes
select_city.on_change('value', lambda attr, old, new: update())
select_user.on_change('value', lambda attr, old, new: update())

#make layout for the graph and selectors
choices = column(select_city, select_user)
city_map = make_plot(src)
layout = row(city_map, choices)

update()
curdoc().add_root(layout)