import os
#import magic
import urllib.request
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from threading import Thread
from tornado.ioloop import IOLoop
from bokeh.embed import server_document
import numpy as np  # import auxiliary library, typical idiom
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, Select, Tabs, Panel, Button, ImageURL, Slider, Grid, LinearAxis, Plot
from bokeh.models import Range1d, ColorBar, LinearColorMapper, LogColorMapper, LogTicker, Div, Select, Slider, TextInput
from bokeh.layouts import column, row, WidgetBox, layout
from bokeh.models.callbacks import CustomJS
from PIL import Image
from bokeh.server.server import Server
from bokeh.themes import Theme
from bokeh.client import pull_session
from bokeh.embed import server_session
from flask.helpers import url_for
from bokeh.models.callbacks import CustomJS
from PIL import Image
import PIL
from bokeh.models.widgets import Dropdown
from bokeh.transform import transform
import sqlite3 as sql
from os.path import dirname, join
import pandas.io.sql as psql
import random
import glob
from bokeh.transform import dodge
from math import pi

UPLOAD_FOLDER = './static/Visualizations/Uploads'
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


ALLOWED_EXTENSIONS = set(['csv', 'png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	image_list = [name for name in glob.glob('static/Visualizations/Stimuli/*[0-9]_*')]
	image_for_background = str(image_list[random.randint(0, len(image_list)-1)])
	return render_template('index.html', image_for_background = image_for_background)

@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the files part
		if 'files[]' not in request.files:
			flash('No file part')
			return redirect(request.url)
		files = request.files.getlist('files[]')
		for file in files:
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			else:
				flash('Allowed file types are csv, png, jpg, and jpeg')
		flash('File(s) successfully uploaded')
		return redirect(request.url)
		

@app.route('/home', methods=['GET', 'POST'])
def index_home():
	if request.method == 'POST':
		# do stuff when the form is submitted
		# redirect to end the POST handling
		# the redirect can be to the same route or somewhere else
		return redirect(url_for('index'))
	# show the form, it wasn't submitted
	return render_template('index.html')

def Vis1(doc):
    #read csv file
    df_map = pd.read_csv('static/Visualizations/Uploads/fixation_data.csv', parse_dates=[0])

    #create ColumnDataSource
    source_city = ColumnDataSource(data = dict(x=[], y=[], timestamp=[], station=[], user=[], fixation_duration=[]))

    #Global variables
    stations = []
    users = []

    #create city select widget
    for station in df_map['StimuliName']:
        stations.append(station)
    #to remove duplicates
    stations = list(dict.fromkeys(stations))

    select_city = Select(
        title = 'Choose city', 
        value = '01_Antwerpen_S1.jpg', 
        options = stations
    )

    #create user select widget
    for user in df_map['user']:
        users.append(user)
    users = list(dict.fromkeys(users))

    select_user = Select(
        title = 'Choose user',
        value = 'p1',
        options = users
    )

    #create figure and graph (scanpath)
    def make_plot(src):
        fig = figure(
            title='Scanpath', 
            plot_width = 900, 
            plot_height = 600, 
            x_range = (0, 1900), 
            y_range = (0, 1200)
        )
        fig.line(x = 'x', y = 'y', source=source_city)
        fig.circle(
            x='x',
            y='y', 
            size = 'fixation_duration', 
            alpha = 0.5,
            source = source_city
        )
        return fig

    def make_dataset():
        plot_data = df_map[(df_map['StimuliName'] == select_city.value) & (df_map['user'] == select_user.value)].copy()
        return plot_data

    def update():
        new_src = make_dataset()
        source_city.data = dict(
            x=new_src['MappedFixationPointX'],
            y=new_src['MappedFixationPointY'],
            timestamp=new_src['Timestamp'],
            station=new_src['StimuliName'],
            user=new_src['user'],
            fixation_duration=(new_src['FixationDuration']/10)
        )

    #update graph on selected changes
    select_city.on_change('value', lambda attr, old, new: update())
    select_user.on_change('value', lambda attr, old, new: update())

    #make layout for the graph and selectors
    choices = column(select_city, select_user)
    city_map = make_plot(source_city)
    overlay = row(city_map, choices)

    update()
    doc.add_root(overlay)



@app.route('/vis1', methods=['GET', 'POST'])
def index_vis1():
	if request.method == 'POST':
		# do stuff when the form is submitted
		# redirect to end the POST handling
		# the redirect can be to the same route or somewhere else
		return redirect(url_for('vispage1'))
	# show the form, it wasn't submitted
	with pull_session(url="http://localhost:5007/vis1") as session:
	    vis_page = 'Scan Path'
	    vis_text = 'The concept of this graph is to show the user the difference between the scanpath of a colored graph and a noncolored graph. By default the colored image shows on screen and there are checkmarks that allow the user to select if they want to see just the colored scanpath, the black and white, both, or none, with a legend of course. The user can then change the maps as they please.'
	    script = server_session(session_id=session.id, url='http://localhost:5007/vis1')
	    return render_template('vispage.html', script=script, vis_page = vis_page, vis_text=vis_text)

def bk_worker_1():
    server = Server({'/vis1': Vis1}, io_loop=IOLoop(), allow_websocket_origin=["127.0.0.1:8080"], port=5007)
    server.start()
    server.io_loop.start()

Thread(target=bk_worker_1).start()

@app.route('/vis2', methods=['GET', 'POST'])
def index_vis2():
	if request.method == 'POST':
		# do stuff when the form is submitted
		# redirect to end the POST handling
		# the redirect can be to the same route or somewhere else
		return redirect(url_for('vispage'))
	# show the form, it wasn't submitted
	with pull_session(url="http://localhost:5006/vis2") as session:
		vis_page = 'Time Graph'
		vis_text = 'The goal of this visualization is to show the user how the x and y position changes with respect to time. The user can see 3 individual graphs. The first graph shows the (x, y) position as the user scans the image. The second graph that the user can see is an (x, time) graph, where as time goes on, the x axis reflects the change in x position of the eyes, thile the y axis reflects the time spent. The thid graph is the opposite, ie the user sees the (time, y) graph. As time moves on the x-axis, the user sees how the y poition of the gazepath changes.'
		script = server_session(session_id=session.id, url='http://localhost:5006/vis2')
		return render_template('vispage.html', script=script, vis_page = vis_page, vis_text = vis_text)



def Vis2(doc):
    #load dataset
    df_paths = pd.read_csv('static/Visualizations/Uploads/fixation_data.csv', parse_dates=[0])
    df_paths = df_paths.astype({'Timestamp': int, 'StimuliName': str, 'FixationIndex': float, 'FixationDuration': float, 'MappedFixationPointX': int, 'MappedFixationPointY' : int, 'user': str, 'description': str})

    #Global Variables
    users = []
    stations = []

    src = ColumnDataSource(data = dict(x=[], y=[], timestamp=[], station=[], user=[]))

    #Choosing the data we want
    def make_dataset():
        plot_data = df_paths[(df_paths['StimuliName'] == selectStation.value) & (df_paths['user'] == selectUser.value)].copy()
        return plot_data

    #making the plot
    def make_plot(src):
        #Writing X-path
        p1 = figure(title="X path", plot_width = 400, plot_height = 400)
        p1.grid.grid_line_alpha=0.3
        p1.xaxis.axis_label = 'X'
        p1.yaxis.axis_label = 'Time'
        p1.y_range.flipped = True
        p1.line(x='x', y='timestamp', source = src)

        #Writing Y-path
        p2 = figure(title= "Y path", plot_width = 400, plot_height = 400)
        p2.grid.grid_line_alpha=0.3
        p2.xaxis.axis_label = 'Time'
        p2.yaxis.axis_label = 'Y'
        p2.line(x='timestamp', y='y', source = src)
        
        #writing general path
        p3 = figure(title="General Path", plot_width = 400, plot_height = 400)
        p3.grid.grid_line_alpha=0.3
        p3.xaxis.axis_label = 'X'
        p3.yaxis.axis_label = 'Y'
        p3.line(x='x', y='y', source = src)
        return [p1, p2, p3]

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
    overlay = layout([
                    [plot[2], plot[1], widgets],
                    plot[0]])
    update()

    doc.add_root(overlay)

def bk_worker_2():
    server = Server({'/vis2': Vis2}, io_loop=IOLoop(), allow_websocket_origin=["127.0.0.1:8080"], port=5006)
    server.start()
    server.io_loop.start()

Thread(target=bk_worker_2).start()

@app.route('/vis3', methods=['GET', 'POST'])
def index_vis3():
    if request.method == 'POST':
        return redirect(url_for('vispage'))
    with pull_session(url="http://localhost:5008/vis3") as session:
        vis_page='Heat Map'
        vis_text='The idea behind Heat Map is that the user can see a heatmap of a specific user, map, and map color. It helps  the user understand the density of where the majority of the data is using a fun interactive colorcoding. All fixation points from each user fo a specific stimuli are added to the map.'# Depending on how many other dots are close to a dot, the dot\'s color changes from blue to red. The denser the dots, the redder the dots will appear. The user can select the image they want to analyse as well as a constant value \(p\). The closeness of a dot is calculated by taking a dot on the screen and making a virtual circle around it. If another dot is in that circle, the closeness value is increased by 1 for both dots. The dots are put onto the graph with an evenly distributed color coding. The radius of the circle is dynamically changed with the input size of the width and height of the image, and a proportion of the image size constant. The user can self select the value of \(p\). The mathematical formula for the radius of the circle is \(\sqrt{w*h*p \over \pi}\), where \(w=width, h=height, p=\)\(wanted\;area\;of\;circle \over area\;of\;image\). If \(p=0.05\), then the area of the circle is \(5\%\) the area of the rectangle.'
        script = server_session(session_id=session.id, url="http://localhost:5008/vis3")
        return render_template('vispage.html', script=script, vis_page = vis_page, vis_text=vis_text)

def Vis3(doc):
    #load dataset
    df_paths = pd.read_csv('static/Visualizations/Uploads/fixation_data.csv', parse_dates=[0])

    #Global Variables
    stations = []

    src = ColumnDataSource(data = dict(url = [], x=[], y=[], timestamp=[], station=[], user=[], closeness=[]))

    df_paths = df_paths.astype({'Timestamp': int, 'StimuliName': str, 'FixationIndex': float, 'FixationDuration': float, 
                                'MappedFixationPointX': int, 'MappedFixationPointY' : int, 'user': str, 'description': str})

    alp = 0.5 #transparency
    dia = 15 #size of circles
    #p_val = 0.1
    #dia = (p_val * width * height) / (math.Pi)
    dia2 = dia**2

    #Choosing the data we want
    def make_dataset():
        plot_data = df_paths[(df_paths['StimuliName'] == selectStation.value)].copy() # & (df_paths['user'] == selectUser.value)

        plot_data = plot_data.sort_values(by=['MappedFixationPointX']).reset_index().drop('index', axis=1)#sort by x coordinate
    
        plot_data['closeness'] = 0 #the list is added to the dataframe as a new column named "closeness" and only contains 0s

        for index, row in plot_data.iterrows(): #Iterates every row one by one
            xi_val = int(row['MappedFixationPointX'])
            yi_val = int(row['MappedFixationPointY'])
            closeness_val = 0
            for index2, OtherRow in plot_data.iterrows(): #Iterates every row. 
                    if index != index2: #If the row found is not the same row, the distance between the two points is calculated.
                            xi2_val = int(OtherRow['MappedFixationPointX'])
                            yi2_val = int(OtherRow['MappedFixationPointY'])
                            if (xi2_val - xi_val > dia):
                                break
                            if ( (((xi2_val - xi_val)**2 + (yi2_val - yi_val)**2 )) < dia2 ) : #Checks if distance is 'close enough'.
                                closeness_val = closeness_val + 1 
            plot_data.loc[index, 'closeness' ] = closeness_val #This line changes the actual row on the data frame  
        return plot_data

    #making the plot
    def make_plot(src):
        p = figure(
            plot_width = print_width,
            plot_height = print_height,
            x_range = (0, width), 
            y_range = (height, 0), #y value is manipulated to have the correct coordinates.
                                    #in the dataset origin is treated to be the upper left corner. While graphing it is lower left. 
                                    #Therefore we "flip" the y axis in the dataset.           
            title = 'Heatmap',
            x_axis_label = 'x coordinate',
            y_axis_label = 'y coordinate'
        )
        image = ImageURL(url="url", x = 0 , y = 0, w = width, h = height)
        #p.image_url(url = ["https://www.jelter.net/stimuli/" + selectStation.value], 
        #            x = 0 , y = 0, w = width, h = height) #'../../' + 
        p.add_glyph(src, image)
        colors = ["#0000FF", "#0072FF", "#00FF00", "#D1FF00", "#FFC500", "#FF6C00", "#FF0000"]
        cmap = LinearColorMapper(palette=colors)
        p.ellipse(x="x", y="y", source=src, line_color=None, 
                fill_color=transform('closeness', cmap), width=dia, height=dia, alpha=alp)
        color_bar = ColorBar(color_mapper=cmap, ticker=LogTicker(),
                        label_standoff=12, border_line_color=None, location=(0,0))
        p.add_layout(color_bar, 'right')
        return p

    #Select
    for station in df_paths['StimuliName']:
        stations.append(station)
    stations = list(dict.fromkeys(stations))

    selectStation = Select(title="Station:", value = '01_Antwerpen_S1.jpg', options=stations)
    selectAlpha = Slider(title="Select the transparancy of the plotting", start=0, end=1, value=0.05, step=0.01)
    selectSize = Slider(title="Select the size of the dots", start=0, end=50, value=0.1, step=1) 
    selectClose = Slider(title="Select the closeness value", start=0, end=1, value=0.1, step=0.01) #p-value in the equation

    callback = CustomJS(args=dict(source=src, alpha=selectAlpha, size=selectSize, close=selectClose),
                        code="""
        const data = source.data;
        const alp_= alpha.value;
        const dia = size.value;
        const p_val = close.value;

        source.change.emit();
    """)

    selectAlpha.js_on_change('value', callback)
    selectSize.js_on_change('value', callback)
    selectClose.js_on_change('value', callback)

    #Update
    def update():
        new_src = make_dataset()
        N = new_src.size//9
        src.data = dict(
            url = ["https://www.jelter.net/stimuli/" + selectStation.value]*N,
            x=new_src['MappedFixationPointX'],
            y=new_src['MappedFixationPointY'],
            timestamp=new_src['Timestamp'],
            station=new_src['StimuliName'],
            user=new_src['user'],
            closeness=new_src['closeness']
        )

    selectStation.on_change('value', lambda attr, old, new: update())
    #selections = [selectStation]

    image = PIL.Image.open('static/Visualizations/Stimuli/' + selectStation.value)
    width, height = image.size

    ratio = width/height

    print_width = int(ratio * 720)
    print_height = int(720)

    widgets = column(selectStation)
    plot = make_plot(src)
    layout = row(plot, 
                column( widgets, selectAlpha, selectSize, selectClose))
    update()
    doc.add_root(layout)

def bk_worker_3():
    server = Server({'/vis3': Vis3}, io_loop=IOLoop(), allow_websocket_origin=["127.0.0.1:8080"], port=5008)
    server.start()
    server.io_loop.start()

Thread(target=bk_worker_3).start()


@app.route('/vis4', methods=['GET', 'POST'])
def index_vis4():
    if request.method == 'POST':
        return redirect(url_for('vispage'))
    with pull_session(url="http://localhost:5009/vis4") as session:
        vis_page='Bar Chart'
        vis_text='The idea behind this visualization is that you can see...'
        script = server_session(session_id=session.id, url='http://localhost:5009/vis4')
        return render_template('vispage.html', script=script, vis_page = vis_page, vis_text = vis_text)


def Vis4(doc):
    #Reading csv file
    df_map = pd.read_csv('static/Visualizations/Uploads/fixation_data.csv', parse_dates=[0])
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

    overlay = layout([
                    [plot_1[0], plot_2[0], widget_1_2],
                    [plot_3[0], plot_4[0], widget_3_4]
    ])

    update_1(), update_2(), update_3(), update_4()
    doc.add_root(overlay)

def bk_worker_4():
    server = Server({'/vis4': Vis4}, io_loop=IOLoop(), allow_websocket_origin=["127.0.0.1:8080"], port=5009)
    server.start()
    server.io_loop.start()

Thread(target=bk_worker_4).start()


if __name__ == "__main__":
	app.run(port=8080, debug=True)