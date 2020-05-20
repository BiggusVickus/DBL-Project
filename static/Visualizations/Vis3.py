import pandas as pd
import numpy as np
import csv
from bokeh.layouts import gridplot, column, row, WidgetBox, layout
from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.models.widgets import Dropdown
from bokeh.io import output_file, show, curdoc
from bokeh.models import ColumnDataSource, Select, Tabs, Panel, Button, ImageURL, Grid, LinearAxis, Plot, Range1d
import matplotlib.pyplot as plt
import seaborn as sns
from bokeh.models.callbacks import CustomJS
from PIL import Image


#####################################
#####################################
#####   DATASET MANIPULATION    #####
#####################################
#####################################


#Read the csv file
df = pd.read_csv('DBL-Project/static/Visualizations/Uploads/fixation_data.csv', parse_dates=[0]) #read the input data into a dataframe
#stimulus = '01_Antwerpen_S1.jpg'
#df_copy = df[df['StimuliName'] == stimulus].reset_index().copy() #only the rows containing the stimuli map is copied into a new dataframe

#Choosing the data we want
def make_dataset():
    df_copy = df[df['StimuliName'] == stimulus].reset_index().copy() #only the rows containing the stimuli map is copied into a new dataframe
    return df_copy

length = len(df_copy.index) #number of rows in the dataframe is calculated
list_closeness = [0] * length #A list is created such that: number of 0s = number of rows
df_copy['closeness'] = list_closeness #the list is added to the dataframe as a new column named "closeness" and only contains 0s

#Global Variable
stations = []

src = ColumnDataSource(data = dict(x=[], y=[], timestamp=[], station=[], user=[]))


close = 15 #If two point are closer than 15 pixels we consider them close

for index, row in df_copy.iterrows(): #Iterates every row one by one
    closeness_val = int(row['closeness'])
    xi_val = int(row['MappedFixationPointX'])
    yi_val = int(row['MappedFixationPointY'])
    for index2, OtherRow in df_copy.iterrows(): #Iterates every row. 
        if index != index2: #If the row found is not the same row, the distance between the two points is calculated.
            xi2_val = int(OtherRow['MappedFixationPointX'])
            yi2_val = int(OtherRow['MappedFixationPointY'])
            if ( (((xi2_val - xi_val)**2 + (yi2_val - yi_val)**2 )**0.5) < close ) : #Checks if distance is 'close enough'.
                closeness_val = closeness_val + 1 
                #df_copy.replace(to_replace = closeness_val, value = new_closeness_val)
                df_copy.loc[index, 'closeness' ] = closeness_val #This line changes the actual row on the data frame
            else: closeness_val == closeness_val
#df_copy.to_csv('fixation_data.csv')

#After these for loops we have a dataset with different values on its "closeness" column. Now the data is ready to be plotted.


######################################
######################################
########   GRAPHING STARTS    ########
######################################
######################################


#Group points with certain closeness rates in different data frames

df2 = df_copy.loc[(0 <= df_copy['closeness']) & (df_copy['closeness']  <= 2)] #dark blue
df3 = df_copy.loc[(3 <= df_copy['closeness']) & (df_copy['closeness'] <= 5)] #light blue
df4 = df_copy.loc[(6 <= df_copy['closeness']) & (df_copy['closeness'] <= 8)] #dark green
df5 = df_copy.loc[(9 <= df_copy['closeness']) & (df_copy['closeness'] <= 11)] #light green
df6 = df_copy.loc[(12 <= df_copy['closeness']) & (df_copy['closeness'] <= 14)] #orange
df7 = df_copy.loc[(15 <= df_copy['closeness']) & (df_copy['closeness'] <= 17)] #dark orange
df8 = df_copy.loc[18 <= df_copy['closeness']] #red


output_file('line.html')

#Add plot 
def df_copy(src):
    p = figure(
        plot_width=1100,
        plot_height=800,
        x_range=(0,1500), 
        y_range=(0,1500),
        title = 'Example (01_Antwerpen_S1.jpg)',
        x_axis_label = 'x-axis',
        y_axis_label = 'y-axis'
    )
# 1650 x 1200
# 11:8
    p.image_url(url = ['images/01_Antwerpen_S1.jpg'], x = 0 , y = 1500, w = 1500 , h = 1500)

#Plot different colored graphs on top of each other
    p.circle(df2['MappedFixationPointX'], df2['MappedFixationPointY'], size=10, color="MediumBlue", alpha=0.3)
    p.circle(df3['MappedFixationPointX'], df2['MappedFixationPointY'], size=10, color="RoyalBlue", alpha=0.3)
    p.circle(df4['MappedFixationPointX'], df2['MappedFixationPointY'], size=10, color="DarkGreen", alpha=0.3)
    p.circle(df5['MappedFixationPointX'], df3['MappedFixationPointY'], size=10, color="Lime", alpha=0.3)
    p.circle(df6['MappedFixationPointX'], df4['MappedFixationPointY'], size=10, color="Orange", alpha=0.3)
    p.circle(df7['MappedFixationPointX'], df4['MappedFixationPointY'], size=10, color="OrangeRed", alpha=0.3)
    p.circle(df8['MappedFixationPointX'], df4['MappedFixationPointY'], size=10, color="Red", alpha=0.3)



#Select
for station in df_paths['StimuliName']:
    stations.append(station)

#to remove duplicates
stations = list(dict.fromkeys(stations))

selectStation = Select(title="Station:", value = '03_Bordeaux_S1.jpg', options=stations)

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

#update graph on selected changes
selectStation.on_change('value', lambda attr, old, new: update())
selections = [selectStation]

plot = make_plot(src)

widgets = column(*selections, width = 320, height = 200)



#make layout for the graph and selectors
choices = column(selectStation)
#city_map = make_plot(source_city)
layout = row(choices) #city_map, 

update()
curdoc().add_root(layout)

#Show results
#show(p)

#dropwdown = ['hello', 'goodbye', ...]
#x = select.dropwdown
#image name = str(images/) + str(x)
#p.image_url(url = [image_name], x = 0 , y = 1500, w = 1500 , h = 1500)