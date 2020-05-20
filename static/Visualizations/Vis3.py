import numpy as np  # import auxiliary library, typical idiom
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, Select, Tabs, Panel, Button, ImageURL
from bokeh.layouts import column, row, WidgetBox, layout
from bokeh.models.callbacks import CustomJS
from PIL import Image
import csv
from bokeh.plotting import figure, output_file, show
from bokeh.models.widgets import Dropdown
from bokeh.io import output_file, show, curdoc
from bokeh.models import ColumnDataSource, Grid, ImageURL, LinearAxis, Plot, Range1d, ColorBar, LinearColorMapper, LogColorMapper
from bokeh.models import ColorBar, LogColorMapper, LogTicker
from bokeh.models import LinearColorMapper
from bokeh.transform import transform
sns.set()  # set Seaborn defaults

#load dataset
df_paths = pd.read_csv('fixation_data.csv', parse_dates=[0])
df_paths = df_paths.astype({'Timestamp': int, 'StimuliName': str, 'FixationIndex': float, 'FixationDuration': float, 'MappedFixationPointX': int, 'MappedFixationPointY' : int, 'user': str, 'description': str})

#Global Variables
users = []
stations = []

src = ColumnDataSource(data = dict(x=[], y=[], timestamp=[], station=[], user=[]))

#Choosing the data we want
def make_dataset():
    plot_data = df_paths[(df_paths['StimuliName'] == selectStation.value) & (df_paths['user'] == selectUser.value)].copy()
    length = len(df_copy.index) #number of rows in the dataframe is calculated
    list_closeness = [0] * length #A list is created such that: number of 0s = number of rows
    df_copy['closeness'] = list_closeness #the list is added to the dataframe as a new column named "closeness" and only contains 0s

    close = 15
    for index, row in df_copy.iterrows(): #Iterates every row one by one
        closeness_val = int(row['closeness'])
        xi_val = int(row['MappedFixationPointX'])
        yi_val = int(row['MappedFixationPointY'])
        for index2, OtherRow in df_copy.iterrows(): #Iterates every row. 
            if index != index2: #If the row found is not the same row, the distance between the two points is calculated.
                xi2_val = int(OtherRow['MappedFixationPointX'])
                yi2_val = int(OtherRow['MappedFixationPointY'])
                if ( (((xi2_val - xi_val)**2 + (yi2_val - yi_val)**2 )) < close**2 ) : #Checks if distance is 'close enough'.
                    closeness_val = closeness_val + 1 
                    df_copy.loc[index, 'closeness' ] = closeness_val #This line changes the actual row on the data frame
                else: closeness_val == closeness_val
    return plot_data

#making the plot
def make_plot(src):
    colors = ['#0000CD', '#4169E1', '#006400', '#00FF00', '#FFA500', '#FF4500', '#FF0000']
    
    p = figure(
        plot_width=990,
        plot_height=720,
        x_range=(0,1500), 
        y_range=(0,1500),
        title = 'Example (03_Bordeaux_S1.jpg)',
        x_axis_label = 'x coordinate',
        y_axis_label = 'y coordinate'
    )

    p.image_url(url = ['images/03_Bordeaux_S1.jpg'], x = 0 , y = 1500, w = 1500 , h = 1500)

    cmap = LinearColorMapper()
    #palette=colors[index]

    p.ellipse(x="MappedFixationPointX", y="MappedFixationPointY", source=src, line_color=None,
        fill_color=transform('closeness', cmap))
    #.ellipse(x=.., y=.., source=your_df, fill_color=transform('close_points', linear_color_mapper))
    return p

#Select
for station in df_paths['StimuliName']:
    stations.append(station)
for person in df_paths['user']:
    users.append(person)
#to remove duplicates
stations = list(dict.fromkeys(stations))
users = list(dict.fromkeys(users))

selectStation = Select(title="Station:", value = '03_Bordeaux_S1.jpg', options=stations)
selectUser = Select(title='User:', value='p1', options=users)

#Update
def update():
    new_src = make_dataset()
    src.data = dict(
        x=new_src['MappedFixationPointX'],
        y=new_src['MappedFixationPointY'],
        timestamp=new_src['Timestamp'],
        station=new_src['StimuliName'],
        user=new_src['user'],
    )

selectStation.on_change('value', lambda attr, old, new: update())
selectUser.on_change('value', lambda attr, old, new: update())
selections = [selectStation, selectUser]

plot = make_plot(src)

widgets = column(*selections, width = 320, height = 200)
layout = layout([
                [plot[2], plot[1], widgets],
                plot[0]])
update()

curdoc().add_root(layout)