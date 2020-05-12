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

#Reading csv file
df_map = pd.read_csv('static/Uploads/fixation_data.csv', parse_dates=[0])

#Make ColumnDataSource
source_city = ColumnDataSource(data = dict(x=[], y=[], timestamp=[], station=[], user=[], fixation_duration=[]))

#Global variables
stations = []

#Create city select widget
for station in df_map['Stimuliname']:
    stations.append(station)

#Remove duplicates
stations = list(dict.fromkeys(stations))

select_city = Select(
    title = 'Choose city'
    value = '01_Antwerpen_S1.jpg'
    options = stations
)

#grouped_city = df_map.groupby('StimuliName')
#grouped_city['FixationDuration'].sum().plot(kind='bar')

def make_plot(src):
    fig1 = figure(
        title = 'Barcharts',
        plot_width = 400,
        plot_height = 400,
        
    )
    fig1.plot(kind = 'bar')