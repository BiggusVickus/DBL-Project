import pandas as pd
import csv
from bokeh.plotting import figure, output_file, show
from bokeh.models.widgets import Dropdown
from bokeh.io import output_file, show

#Read the csv file
df = pd.read_csv('fixation_data_edited.csv', parse_dates=[0])
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

df_copy.to_csv('fixation_data.csv')

