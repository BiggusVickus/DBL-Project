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
from bokeh.transform import dodge

#Reading csv file
df_map = pd.read_csv('Datasets/fixation_data.csv', parse_dates=[0])
df_map = df_map.astype({'Timestamp': int, 'StimuliName': str, 'FixationIndex': float, 'FixationDuration': float, 'MappedFixationPointX': int, 'MappedFixationPointY' : int, 'user': str, 'description': str})

#Making data frames
df_map_S1 = df_map[df_map['StimuliName'].str.contains("S1")]
df_map_S2 = df_map[df_map['StimuliName'].str.contains("S2")]

df_map_S1_color = df_map_S1[df_map_S1['description'] == 'color']
df_map_S1_gray = df_map_S1[df_map_S1['description'] == 'gray']
df_map_S2_color = df_map_S2[df_map_S2['description'] == 'color']
df_map_S2_gray = df_map_S2[df_map_S2['description'] == 'gray']

df_map_S1_color_grouped = df_map_S1_color.groupby("StimuliName")
df_map_S1_gray_grouped = df_map_S1_gray.groupby("StimuliName")
df_map_S2_color_grouped = df_map_S2_color.groupby("StimuliName")
df_map_S2_gray_grouped = df_map_S2_gray.groupby("StimuliName")

S1_color = df_map_S1_color_grouped[['FixationDuration']].sum().reset_index()
S1_gray = df_map_S1_gray_grouped[['FixationDuration']].sum().reset_index()
S2_color = df_map_S2_color_grouped[['FixationDuration']].sum().reset_index()
S2_gray = df_map_S2_gray_grouped[['FixationDuration']].sum().reset_index()

list_1 = S1_color['StimuliName'].tolist()

#StimuliNames_S1_color = ['01_Antwerpen_S1.jpg', '02_Berlin_S1.jpg', '03_Bordeaux_S1.jpg', '04_Köln_S1.jpg', '05_Frankfurt_S1.jpg', '06_Hamburg_S1.jpg', 
#'07_Moskau_S1.jpg', '08_Riga_S1.jpg', '09_Tokyo_S1.jpg', '10_Barcelona_S1.jpg', '11_Bologna_S1.jpg', '12_Brussel_S1.jpg', '13_Budapest_S1.jpg',
#'14_Düsseldorf_S1.jpg', '15_Göteborg_S1.jpg', '16_Hong_Kong_S1.jpg', '17_Krakau_S1.jpg', '18_Ljubljana_S1.jpg', '19_New_York_S1.jpg', '20_Paris_S1.jpg',
#'21_Pisa_S1.jpg', '22_Venedig_S1.jpg', '23_Warschau_S1.jpg', '24_Zürich_S1.jpg']

#Make ColumnDataSource
source_city = ColumnDataSource(data = dict(x=[], y=[], timestamp=[], station=[], fixation_duration=[]))

#Global variables
stations = []

#Create city select widget
for station in df_map['StimuliName']:
    stations.append(station)

#Remove duplicates
stations = list(dict.fromkeys(stations))

select_city = Select(
    title = 'Choose city',
    value = '01_Antwerpen_S1.jpg',
    options = stations
)

def make_dataset():
    plot_data_S1_color = S1_color[(S1_color['StimuliName'] == select_city.value)].copy()
    #plot_data_S1_gray = df_map_S1_gray_grouped[(df_map_S1_gray_grouped['StimuliName'] == select_city.value)].copy()
    #plot_data_S2_color = df_map_S2_color_grouped[(df_map_S2_color_grouped['StimuliName'] == select_city.value)].copy()
    #plot_data_S2_gray = df_map_S2_gray_grouped[(df_map_S2_gray_grouped['StimuliName'] == select_city.value)].copy()
    return plot_data_S1_color, #plot_data_S1_gray, plot_data_S2_color, plot_data_S2_gray

def make_plot(src):
    fig1 = figure(
        x_range = list_1,
        y_range = (0,750000),
        title = 'Barcharts',
        plot_width = 400,
        plot_height = 400
    )
    fig1.vbar(x='StimuliName', top = 'FixationDuration', width = 0.45, source = source_city, color = "red", legend_label = "color")
    #fig1.vbar(x='StimuliName', top = S1_gray, width = 0.45, source = source_city, color = "blue", legend_label = "gray")
    fig1.xaxis.axis_label = 'City'
    fig1.yaxis.axis_label = 'Time'
    fig1.xgrid.grid_line_color = None
    return fig1
    
#Update
def update():
    new_src = make_dataset()
    source_city.data = dict(
        x=new_src['MappedFixationPointX'],
        y=new_src['MappedFixationPointY'],
        timestamp=new_src['Timestamp'],
        station=new_src['StimuliName'],
        fixation_duration=new_src['Fixation']
    )

select_city.on_change('value', lambda attr, old, new: update())
selections = [select_city]

plot = make_plot(source_city)

widgets = column(*selections, width = 320, height = 200)

layout = row(plot, widgets)

update()
curdoc().add_root(layout)