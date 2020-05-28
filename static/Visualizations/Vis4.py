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
from math import pi

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

df_map_S1_color_grouped_2 = df_map_S1_color.groupby(["StimuliName","user"])
df_map_S1_gray_grouped_2 = df_map_S1_gray.groupby(["StimuliName","user"])
df_map_S2_color_grouped_2 = df_map_S2_color.groupby(["StimuliName","user"])
df_map_S2_gray_grouped_2 = df_map_S2_gray.groupby(["StimuliName","user"])

S1_color = df_map_S1_color_grouped[['FixationDuration']].sum().reset_index()
S1_gray = df_map_S1_gray_grouped[['FixationDuration']].sum().reset_index()
S2_color = df_map_S2_color_grouped[['FixationDuration']].sum().reset_index()
S2_gray = df_map_S2_gray_grouped[['FixationDuration']].sum().reset_index()

S1_color_2 = df_map_S1_color_grouped_2[['FixationDuration']].sum().reset_index()
S1_gray_2 = df_map_S1_gray_grouped_2[['FixationDuration']].sum().reset_index()
S2_color_2 = df_map_S2_color_grouped_2[['FixationDuration']].sum().reset_index()
S2_gray_2 = df_map_S2_gray_grouped_2[['FixationDuration']].sum().reset_index()

list_1 = S1_color['StimuliName'].tolist()
list_2 = S1_gray['StimuliName'].tolist()
list_3 = S2_color['StimuliName'].tolist()
list_4 = S2_gray['StimuliName'].tolist()

#Make ColumnDataSource
source_city_1 = ColumnDataSource(data = dict(x=[], station=[], fixation_duration=[]))
source_city_2 = ColumnDataSource(data = dict(x=[], station=[], fixation_duration=[]))
source_city_3 = ColumnDataSource(data = dict(x=[], station=[], fixation_duration=[]))
source_city_4 = ColumnDataSource(data = dict(x=[], station=[], fixation_duration=[]))

#Global variables
Stations_S1_Color = []
Stations_S1_Gray = []
Stations_S2_Color = []
Stations_S2_Gray = []

#Create city select widget
for station in df_map_S1_color['StimuliName']:
    Stations_S1_Color.append(station)

for station in df_map_S1_gray['StimuliName']:
    Stations_S1_Gray.append(station)

for station in df_map_S2_color['StimuliName']:
    Stations_S2_Color.append(station)

for station in df_map_S2_gray['StimuliName']:
    Stations_S2_Gray.append(station)


#Remove duplicates
Stations_S1_Color = list(dict.fromkeys(Stations_S1_Color))
Stations_S1_Gray = list(dict.fromkeys(Stations_S1_Gray))
Stations_S2_Color = list(dict.fromkeys(Stations_S2_Color))
Stations_S2_Gray = list(dict.fromkeys(Stations_S2_Gray))

#Sort Lists
Stations_S1_Gray.sort()
Stations_S2_Color.sort()

#Make widget 
select_city_1 = Select(
    title = 'Choose city S1 Color',
    value = '01_Antwerpen_S1.jpg',
    options = Stations_S1_Color
)

select_city_2 = Select(
    title = 'Choose city S1 Gray',
    value = '01b_Antwerpen_S1.jpg',
    options = Stations_S1_Gray
)

select_city_3 = Select(
    title = 'Choose city S2 Color',
    value = '01_Antwerpen_S2.jpg',
    options = Stations_S2_Color
)

select_city_4 = Select(
    title = 'Choose city S2 Gray',
    value = '01b_Antwerpen_S2.jpg',
    options = Stations_S2_Gray
)

def make_dataset_1():
    plot_data_S1_color = S1_color[(S1_color['StimuliName'] == select_city_1.value)].copy()
    return plot_data_S1_color

def make_dataset_2():
    plot_data_S1_gray = S1_gray[(S1_gray['StimuliName'] == select_city_2.value)].copy()
    return plot_data_S1_gray

def make_dataset_3():
    plot_data_S2_color = S2_color[(S2_color['StimuliName'] == select_city_3.value)].copy()
    return plot_data_S2_color

def make_dataset_4():
    plot_data_S2_gray = S2_gray[(S2_gray['StimuliName'] == select_city_4.value)].copy()
    return plot_data_S2_gray


def make_plot_1(src):
    fig1 = figure(
        x_range = list_1,
        y_range = (0,750000),
        title = 'S1 Color Barcharts',
        plot_width = 500,
        plot_height = 500
    )
    fig1.vbar(x='x', top = 'fixation_duration', width = 0.5, source = source_city_1, color = "red", legend_label = "color")
    fig1.xaxis.axis_label = 'City'
    fig1.yaxis.axis_label = 'Total Time'
    fig1.xaxis.major_label_orientation = pi/3
    fig1.xgrid.grid_line_color = None
    fig1.add_tools(HoverTool(
        tooltips=[
            ("Total Time", "@fixation_duration")
            #("p1","@dsfdf")
        ], renderers=[bar]
    ))
    return [fig1]

def make_plot_2(src):
    fig2 = figure(
        x_range = list_2,
        y_range = (0,750000),
        title = 'S1 Gray Barcharts',
        plot_width = 500,
        plot_height = 500
    )
    fig2.vbar(x='x', top = 'fixation_duration', width = 0.5, source = source_city_2, color = "blue", legend_label = "gray")
    fig2.xaxis.axis_label = 'City'
    fig2.yaxis.axis_label = 'Total Time'
    fig2.xaxis.major_label_orientation = pi/3
    fig2.xgrid.grid_line_color = None
    return [fig2]
    
def make_plot_3(src):
    fig3 = figure(
        x_range = list_3,
        y_range = (0,750000),
        title = 'S2 Color Barcharts',
        plot_width = 500,
        plot_height = 500
    )
    fig3.vbar(x='x', top = 'fixation_duration', width = 0.5, source = source_city_3, color = "red", legend_label = "color")
    fig3.xaxis.axis_label = 'City'
    fig3.yaxis.axis_label = 'Total Time'
    fig3.xaxis.major_label_orientation = pi/3
    fig3.xgrid.grid_line_color = None
    return [fig3]

def make_plot_4(src):
    fig4 = figure(
        x_range = list_4,
        y_range = (0,750000),
        title = 'S2 Gray Barcharts',
        plot_width = 500,
        plot_height = 500
    )
    fig4.vbar(x='x', top = 'fixation_duration', width = 0.5, source = source_city_4, color = "blue", legend_label = "gray")
    fig4.xaxis.axis_label = 'City'
    fig4.yaxis.axis_label = 'Total Time'
    fig4.xaxis.major_label_orientation = pi/3
    fig4.xgrid.grid_line_color = None
    return [fig4]

#Update
def update_1():
    new_src = make_dataset_1()
    source_city_1.data = dict(
        x=new_src['StimuliName'],
        station=new_src['StimuliName'],
        fixation_duration=new_src['FixationDuration']
    )

def update_2():
    new_src_2 = make_dataset_2()
    source_city_2.data = dict(
        x=new_src_2['StimuliName'],
        station=new_src_2['StimuliName'],
        fixation_duration=new_src_2['FixationDuration']
    )

def update_3():
    new_src_3 = make_dataset_3()
    source_city_3.data = dict(
        x=new_src_3['StimuliName'],
        station=new_src_3['StimuliName'],
        fixation_duration=new_src_3['FixationDuration']
    )

def update_4():
    new_src_4 = make_dataset_4()
    source_city_4.data = dict(
        x=new_src_4['StimuliName'],
        station=new_src_4['StimuliName'],
        fixation_duration=new_src_4['FixationDuration']
    )

select_city_1.on_change('value', lambda attr, old, new: update_1())
select_city_2.on_change('value', lambda attr, old, new: update_2())
select_city_3.on_change('value', lambda attr, old, new: update_3())
select_city_4.on_change('value', lambda attr, old, new: update_4())

selection_1 = [select_city_1]
selection_2 = [select_city_2]
selection_3 = [select_city_3]
selection_4 = [select_city_4]

plot_1 = make_plot_1(source_city_1)
plot_2 = make_plot_2(source_city_2)
plot_3 = make_plot_3(source_city_3)
plot_4 = make_plot_4(source_city_4)

widget_1_2 = column(*selection_1, *selection_2, width = 320, height = 200)
widget_3_4 = column(*selection_3, *selection_4, width = 320, height = 200)

layout = layout([
                [plot_1[0], plot_2[0], widget_1_2],
                [plot_3[0], plot_4[0], widget_3_4]
])

update_1(), update_2(), update_3(), update_4()
curdoc().add_root(layout)