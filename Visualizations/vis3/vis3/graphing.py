import pandas as pd
import csv
from bokeh.plotting import figure, output_file, show
from bokeh.models.widgets import Dropdown
from bokeh.io import output_file, show, curdoc
import numpy as np
from bokeh.models import ColumnDataSource, Grid, ImageURL, LinearAxis, Plot, Range1d

df_copy = pd.read_csv('fixation_data.csv', parse_dates=[0])

#Group points with certain closeness rates in different data frames
df2 = df_copy[(df_copy['closeness'].isin([0,1,2]))] #dark blue
df3 = df_copy[(df_copy['closeness'].isin([3,4,5]))] #light blue
df4 = df_copy[(df_copy['closeness'].isin([6,7,8]))] #dark green
df5 = df_copy[(df_copy['closeness'].isin([9,10,11]))] #light green
df6 = df_copy[(df_copy['closeness'].isin([11,12,13]))] #orange
df7 = df_copy[(df_copy['closeness'].isin([14,15,16]))] #dark orange
df8 = df_copy[(df_copy['closeness'].isin([17,18,19]))] #red
#print(df4)

output_file('line.html')

#Add plot 
p = figure(
    plot_width=400,
    plot_height=400,
    x_range=(0,1600), 
    y_range=(0,1600),
    title = 'Example (01_Antwerpen_S2)',
    x_axis_label = 'x-axis',
    y_axis_label = 'y-axis'
    )
p.image_url(url = ['images/01_Antwerpen_S1.jpg'], x = 0 , y = 0, w = 1600 , h = 1600) 
#C:\Users\20190756\source\repos\vis3\vis3\01_Antwerpen_S1.jpg

#Plot different colored graphs on top of each other
p.circle(df2['MappedFixationPointX'], df2['MappedFixationPointY'], size=7, color="MediumBlue", alpha=0.3)
p.circle(df3['MappedFixationPointX'], df2['MappedFixationPointY'], size=7, color="RoyalBlue", alpha=0.3)
p.circle(df4['MappedFixationPointX'], df2['MappedFixationPointY'], size=7, color="DarkGreen", alpha=0.3)
p.circle(df5['MappedFixationPointX'], df3['MappedFixationPointY'], size=7, color="Lime", alpha=0.3)
p.circle(df6['MappedFixationPointX'], df4['MappedFixationPointY'], size=7, color="Orange", alpha=0.3)
p.circle(df7['MappedFixationPointX'], df4['MappedFixationPointY'], size=7, color="OrangeRed", alpha=0.3)
p.circle(df8['MappedFixationPointX'], df4['MappedFixationPointY'], size=7, color="Red", alpha=0.3)

#Show results
show(p)