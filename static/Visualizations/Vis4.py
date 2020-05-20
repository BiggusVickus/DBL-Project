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
list_2 = S1_gray['StimuliName'].tolist()
list_3 = S2_color['StimuliName'].tolist()
list_4 = S2_gray['StimuliName'].tolist()

#Make ColumnDataSource
source_city = ColumnDataSource(data = dict(x=[], station=[], fixation_duration=[]))

#Global variables
stations = []

#Create city select widget
for station in df_map['StimuliName']:
    stations.append(station)

#Remove duplicates
stations = list(dict.fromkeys(stations))

select_city_1 = Select(
    title = 'Choose city',
    value = '01_Antwerpen_S1.jpg',
    options = stations
)

select_city_2 = Select(
    title = 'Choose city',
    value = '01_Antwerpen_S1.jpg',
    options = stations
)

def make_dataset():
    #if(df_map[df_map['StimuliName'].str.contains("S1")]): #& df_map_S1[df_map_S1['description'] == 'color']):
        plot_data_S1_color = S1_color[(S1_color['StimuliName'] == select_city_1.value)].copy()
        return plot_data_S1_color
    #elif(df_map[df_map['StimuliName'].str.contains("S2")]):# & df_map_S1[df_map_S1['description'] == 'gray']):
    #    plot_data_S1_gray = S1_gray[(S1_gray['StimuliName'] == select_city_2.value)].copy()
    #    return plot_data_S1_gray
    #elif(df_map[df_map['StimuliName'].str.contains("S2")] & df_map_S1[df_map_S1['description'] == 'color']):
    #    plot_data_S2_color = S2_color[(S2_color['StimuliName'] == select_city.value)].copy()
    #    return plot_data_S2_color
    #elif(df_map[df_map['StimuliName'].str.contains("S2")] & df_map_S1[df_map_S1['description'] == 'gray']):
    #    plot_data_S2_gray = S2_gray[(S2_gray['StimuliName'] == select_city.value)].copy()
    #    return plot_data_S2_gray

def make_plot(src):
    fig1 = figure(
        x_range = list_1,
        y_range = (0,750000),
        title = 'Barcharts',
        plot_width = 400,
        plot_height = 400
    )
    fig1.vbar(x='x', top = 'fixation_duration', width = 0.45, source = source_city, color = "red", legend_label = "color")
    fig1.xaxis.axis_label = 'City'
    fig1.yaxis.axis_label = 'Time'
    fig1.xgrid.grid_line_color = None
    
    fig2 = figure(
        x_range = list_2,
        y_range = (0,750000),
        title = 'Barcharts',
        plot_width = 400,
        plot_height = 400
    )
    fig2.vbar(x='x', top = 'fixation_duration', width = 0.45, source = source_city, color = "red", legend_label = "gray")
    fig2.xaxis.axis_label = 'City'
    fig2.yaxis.axis_label = 'Time'
    fig2.xgrid.grid_line_color = None

    fig3 = figure(
        x_range = list_3,
        y_range = (0,750000),
        title = 'Barcharts',
        plot_width = 400,
        plot_height = 400
    )
    fig3.vbar(x='x', top = 'fixation_duration', width = 0.45, source = source_city, color = "red", legend_label = "color")
    fig3.xaxis.axis_label = 'City'
    fig3.yaxis.axis_label = 'Time'
    fig3.xgrid.grid_line_color = None

    fig4 = figure(
        x_range = list_4,
        y_range = (0,750000),
        title = 'Barcharts',
        plot_width = 400,
        plot_height = 400
    )
    fig4.vbar(x='x', top = 'fixation_duration', width = 0.45, source = source_city, color = "red", legend_label = "gray")
    fig4.xaxis.axis_label = 'City'
    fig4.yaxis.axis_label = 'Time'
    fig4.xgrid.grid_line_color = None

    return [fig1,fig2,fig3,fig4]
    
#Update
def update():
    new_src = make_dataset()
    source_city.data = dict(
        x=new_src['StimuliName'],
        station=new_src['StimuliName'],
        fixation_duration=new_src['FixationDuration']
    )

select_city_1.on_change('value', lambda attr, old, new: update())
select_city_2.on_change('value', lambda attr, old, new: update())

selection_1 = [select_city_1]
selection_2 = [select_city_2]

plot = make_plot(source_city)

widget_1 = column(*selection_1, width = 320, height = 200)
widget_2 = column(*selection_2, width = 320, height = 200)

layout = layout([
                [plot[0], plot[1], widget_1],
                [plot[2], plot[3], widget_2]
])

update()
curdoc().add_root(layout)