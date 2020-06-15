import bokeh as bk 
from bokeh.plotting import figure, show, curdoc
from bokeh.io import output_file, output_notebook, show 
from bokeh.models import ColumnDataSource, Select, RadioButtonGroup, Plot, ImageURL, Slider, ColorPicker, HoverTool
from bokeh.layouts import row, column, gridplot, widgetbox
from bokeh.models.widgets import Tabs, Panel
from bokeh.palettes import Spectral10

import seaborn as sns
import PIL
from PIL import Image

import sqlite3 as sql
import pandas as pd 
import numpy as np

df_map = pd.read_csv('Uploads/fixation_data.csv', parse_dates=[0])
src = ColumnDataSource(
    data = dict(url=[], x=[], y=[], timestamp=[], station=[], user=[], fixation_duration=[])
)
#df_map.drop(columns = ['FixationIndex', 'Timestamp', 'description'])

stations = []
users = []

for station in df_map['StimuliName']:
    stations.append(station)
#to remove duplicates
stations = list(dict.fromkeys(stations))

select_city = Select(
    title = 'Choose city', 
    value = '01_Antwerpen_S1.jpg', 
    options = stations
)
new_src = df_map[df_map['StimuliName'] == select_city.value]

def make_plot(src, new_src):
    fig = figure(
        title='Scanpath', 
        plot_width = print_width, 
        plot_height = print_height, 
        x_range = (0, width), 
        y_range = (height, 0)
    )
    image = ImageURL(url = "url", x=0, y=0, w=width, h=height)
    fig.add_glyph(src, image)
    for index, row in new_src.iterrows():
        fig.line(
            x = row['MappedFixationPointX'],
            y = row['MappedFixationPointY'],
            width = 3, alpha = 1, muted_alpha = 0.1,
            legend_label = row['user'],
        )
        fig.circle(
            x = row['MappedFixationPointX'],
            y = row['MappedFixationPointY'],
            size = row['FixationDuration']/10,
            alpha = 0.7, muted_alpha = 0.1,
            legend_label = row['user'],
        )
    fig.legend.click_policy = 'mute'
    tooltips = [
        ('Time', '@FixationDuration'),
        ('Coordinates', '($x, $y)')
    ]
    fig.add_tools(HoverTool(tooltips = tooltips))
    return fig

def make_dataset():
    plot_data = df_map[(df_map['StimuliName'] == select_city.value)]
    return plot_data

def update():
    new_src = make_dataset()
    N = len(new_src.index)
    src.data = dict(
        url = ["https://www.jelter.net/stimuli/"+select_city.value]*N,
        x=new_src['MappedFixationPointX'],
        y=new_src['MappedFixationPointY'],
        timestamp=new_src['Timestamp'],
        station=new_src['StimuliName'],
        user=new_src['user'],
        fixation_duration=(new_src['FixationDuration']/10)
    )
    make_plot(src, new_src)

select_city.on_change('value', lambda attr, old, new: update())

image = PIL.Image.open('Stimuli/'+select_city.value)
width, height = image.size
ratio = width/height

print_width = int(ratio * 720)
print_height = int(720)

choices = column(select_city)
city_map = make_plot(src, new_src)
layout = row(city_map, choices)

update()
curdoc().add_root(layout)