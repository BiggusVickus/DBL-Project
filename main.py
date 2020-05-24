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
from bokeh.models import ColumnDataSource, Select, Tabs, Panel, Button, ImageURL, Slider
from bokeh.layouts import column, row, WidgetBox, layout
from bokeh.models.callbacks import CustomJS
from PIL import Image
from bokeh.server.server import Server
from bokeh.themes import Theme
from bokeh.client import pull_session
from bokeh.embed import server_session
from flask.helpers import url_for
import random
import glob

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
    df_map = pd.read_csv('Visualizations/fixation_data.csv', parse_dates=[0])

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
		#script = server_document('http://127.0.0.1:5006/vis2')
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
		# do stuff when the form is submitted
		# redirect to end the POST handling
		# the redirect can be to the same route or somewhere else
		return redirect(url_for('vispage'))
	# show the form, it wasn't submitted
	vis_page = 'Heat Map'
	vis_text = 'The idea behind Heat Map is that the user can see a heatmap of a specific user, map, and map color. It helps  the user understand the density of where the majority of the data is using a fun interactive colorcoding. All fixation points from each user fo a specific stimuli are added to the map. Depending on how many other dots are close to a dot, the dot\'s color changes from blue to red. The denser the dots, the redder the dots will appear. The user can select the image they want to analyse as well as a constant value \(p\). The closeness of a dot is calculated by taking a dot on the screen and making a virtual circle around it. If another dot is in that circle, the closeness value is increased by 1 for both dots. The dots are put onto the graph with an evenly distributed color coding. The radius of the circle is dynamically changed with the input size of the width and height of the image, and a proportion of the image size constant. The user can self select the value of \(p\). The mathematical formula for the radius of the circle is \(\sqrt{w*h*p \over \pi}\), where \(w=width, h=height, p=\)\(wanted\;area\;of\;circle \over area\;of\;image\). If \(p=0.05\), then the area of the circle is \(5\%\) the area of the rectangle.'
	return render_template('vispage.html', vis_page = vis_page, vis_text=vis_text)

@app.route('/vis4', methods=['GET', 'POST'])
def index_vis4():
	if request.method == 'POST':
		# do stuff when the form is submitted
		# redirect to end the POST handling
		# the redirect can be to the same route or somewhere else
		return redirect(url_for('vispage'))
	vis_page = 'Bar Chart'
	vis_text = 'The idea behind this visualization is that you can see....'
	# show the form, it wasn't submitted

	return render_template('vispage.html', vis_page = vis_page, vis_text=vis_text)



if __name__ == "__main__":
	app.run(port=8080, debug=True)