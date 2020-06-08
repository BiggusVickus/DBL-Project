import bokeh as bk 
from bokeh.plotting import figure, show, curdoc
from bokeh.io import output_file, output_notebook, show 
from bokeh.models import ColumnDataSource, Select, RadioButtonGroup, Plot, ImageURL, Slider, ColorPicker, HoverTool
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
#df_ok = pd.DataFrame({'color':[], 'url':[], 'x':[], 'y':[], 'timestamp':[], 'station':[], 'user':[], 'fixation_duration':[]})
src = ColumnDataSource(#df_ok
    data = dict(opacity_l=[], opacity_c=[], color=[], url=[], x=[], y=[], timestamp=[], station=[], user=[], fixation_duration=[])
    )

#Global variables
stations = []
users = ["all"]

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

select_color = Select(
    title = 'Choose color of graph',
    options = ['steelblue', 'darkgreen', 'gold', 'darkorange', 'red'],
    value = 'darkgreen'
)

line_opacity = Slider(
    title = 'Opacity of line',
    value = 0.7, step = 0.1,
    start = 0, end = 1
)

circle_opacity = Slider(
    title = 'Opacity of circles',
    value = 0.5, step = 0.1,
    start = 0, end = 1
)

#create figure with background and graph (scanpath)
def make_plot(src):
    fig = figure(
        title='Scanpath', 
        plot_width = print_width, 
        plot_height = print_height, 
        x_range = (0, width), 
        y_range = (height, 0)
    )
    image = ImageURL(url = "url", x=0, y=0, w=width, h=height)
    fig.add_glyph(src, image)
    #the color should already be in '' thus it sees 'color' as the color instead of the CDS color
    fig.line(x = 'x', y = 'y', width = 3, alpha = 1, source = src) 
    fig.circle(
        x='x', y='y', 
        size = 'fixation_duration', 
        alpha = 0.5,
        source = src, line_width = 3,
        #color = 'color'
    )
    tooltips = [
        ('Time', '@FixationDuration'),
        ('Coordinates', '($x, $y)')
    ]
    fig.add_tools(HoverTool(tooltips = tooltips))
    return fig

def make_dataset():
    if select_user.value == 'all':
        plot_data = df_map[(df_map['StimuliName'] == select_city.value)].copy()
        #plot_data = plot_data.groupby('user')
    else:
        plot_data = df_map[(df_map['StimuliName'] == select_city.value) & (df_map['user'] == select_user.value)].copy()
    plot_data['opacity_l'] = line_opacity.value
    plot_data['opacity_c'] = circle_opacity.value
    plot_data['color'] = select_color.value
    return plot_data

#update data with new dataframe for new input (selection)
def update():
    new_src = make_dataset()
    N = len(new_src.index) #IMPORTANT
    src.data = dict(
        opacity_l = new_src['opacity_l'],
        opacity_c = new_src['opacity_c'],
        #color = select_color.value,
        url = ["https://www.jelter.net/stimuli/"+select_city.value]*N,
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
select_color.on_change('value', lambda attr, old, new: update())
line_opacity.on_change('value', lambda attr, old, new: update())
circle_opacity.on_change('value', lambda attr, old, new: update())

#get image and its properties
image = PIL.Image.open('Stimuli/'+select_city.value)
width, height = image.size
ratio = width/height

print_width = int(ratio * 720)
print_height = int(720)

#make layout for the graph and selectors
choices = column(select_city, select_user, select_color, line_opacity, circle_opacity)
city_map = make_plot(src)
layout = row(city_map, choices)

update()
curdoc().add_root(layout)