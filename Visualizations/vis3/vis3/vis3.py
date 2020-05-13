import pandas as pd
import csv
from bokeh.plotting import figure, output_file, show
from bokeh.models.widgets import Dropdown
from bokeh.io import output_file, show, curdoc
import numpy as np
from bokeh.models import ColumnDataSource, Grid, ImageURL, LinearAxis, Plot, Range1d

#C:\Users\20190756\source\repos\vis3\vis3





#####################################
#####################################
#####   DATASET MANIPULATION    #####
#####################################
#####################################


#Read the csv file
df = pd.read_csv('upload file', parse_dates=[0])
#C:\Users\20190756\Documents\GitHub\DBL-Project\Visualizations\vis3\vis3\fixation_data_edited.csv
stimulus = '01_Antwerpen_S1.jpg'
df_copy = df[df['StimuliName'] == stimulus].reset_index().copy()

df_copy['closeness'] = 0

close = 15

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







######################################
######################################
########   GRAPHING STARTS    ########
######################################
######################################
###################################################


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
    plot_width=1100,
    plot_height=800,
    x_range=(0,1100), 
    y_range=(0,800),
    title = 'Example (01_Antwerpen_S1.jpg)',
    x_axis_label = 'x-axis',
    y_axis_label = 'y-axis'
    )
# 1650 x 1200
# 11:8
p.image_url(url = ['images/01_Antwerpen_S1.jpg'], x = 0 , y = 800, w = 1100 , h = 800)

#Plot different colored graphs on top of each other
p.circle(df2['MappedFixationPointX'], df2['MappedFixationPointY'], size=10, color="MediumBlue", alpha=0.3)
p.circle(df3['MappedFixationPointX'], df2['MappedFixationPointY'], size=10, color="RoyalBlue", alpha=0.3)
p.circle(df4['MappedFixationPointX'], df2['MappedFixationPointY'], size=10, color="DarkGreen", alpha=0.3)
p.circle(df5['MappedFixationPointX'], df3['MappedFixationPointY'], size=10, color="Lime", alpha=0.3)
p.circle(df6['MappedFixationPointX'], df4['MappedFixationPointY'], size=10, color="Orange", alpha=0.3)
p.circle(df7['MappedFixationPointX'], df4['MappedFixationPointY'], size=10, color="OrangeRed", alpha=0.3)
p.circle(df8['MappedFixationPointX'], df4['MappedFixationPointY'], size=10, color="Red", alpha=0.3)

#Show results
show(p)




#DON'T DELETE - Notes to program the dropdown menu:

#dropwdown = ['hello', 'goodbye', ...]
#x = select.dropwdown
#image name = str(images/) + str(x)
#p.image_url(url = [image_name], x = 0 , y = 1500, w = 1500 , h = 1500)