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

df_map = pd.read_csv('static/Uploads/fixation_data.csv', parse_dates=[0])