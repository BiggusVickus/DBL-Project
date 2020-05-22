import os
import glob
import random
import urllib.request
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from flask.helpers import url_for

#DON'T TOUCH, app settings
UPLOAD_FOLDER = 'static/Uploads'
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

#Remove pdf later
ALLOWED_EXTENSIONS = set(['csv', 'pdf', 'png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
#randomly selects a colored image from /static/Stimuli then passes it onto the html page
@app.route('/')
def upload_form():
	image_list = [name for name in glob.glob('static/Stimuli/*[0-9]_*')]
	image_for_background = str(image_list[random.randint(0, len(image_list)-1)])
	return render_template('index.html', image_for_background = image_for_background)

	#does the upload function, absolutely dont touch or else it breaks

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
		

#part of the homepage
@app.route('/', methods=['GET', 'POST'])
def index_home():
	if request.method == 'POST':
		# do stuff when the form is submitted
		# redirect to end the POST handling
		# the redirect can be to the same route or somewhere else
		return redirect(url_for('index'))
	# show the form, it wasn't submitted
	return render_template('index.html')

#first visualization, returns the visualization number and a summary. Repeat for below. 
@app.route('/Scan-Path', methods=['GET', 'POST'])
def index_vis1():
	if request.method == 'POST':
		return redirect(url_for('vispage1'))
	vis_page = 'Scan-Path'
	vis_text = 'The concept of Scan-Path is to show the user the difference between the scanpath of a colored graph and a noncolored graph. By default the colored image shows on screen and there are checkmarks that allow the user to select if they want to see just the colored scanpath, the black and white, both, or none, with a legend of course. The user can then change the maps as they please.'
	return render_template('vispage.html', vis_page = vis_page, vis_text=vis_text)

@app.route('/Time-Graph', methods=['GET', 'POST'])
def index_vis2():
	if request.method == 'POST':
		return redirect(url_for('vispage'))
	vis_page = 'Time Graph'
	vis_text = 'The goal for Time Graph is to show the user how the x and y poition changes with respect to time. The user can see 3 individual graphs. The first graph shows the (x, y) position as the user scans the image. The second graph that the user can see is an (x, time) graph, where as time goes on, the x axis reflects the change in x position of the eyes, thile the y axis reflects the time spent. The thid graph is the opposite, ie the user sees the (time, y) graph. As time moves on the x-axis, the user sees how the y poition of the gazepath changes.'
	return render_template('vispage.html', vis_page = vis_page, vis_text = vis_text)

@app.route('/Heat-Map', methods=['GET', 'POST'])
def index_vis3():
	if request.method == 'POST':
		return redirect(url_for('vispage'))
	vis_page = 'Heat Map'
	vis_text = 'The idea behind Heat Map is that the user can see a heatmap of a specific user, map, and map color. It helps  the user understand the density of where the majority of the data is using a fun interactive colorcoding. All fixation points from each user fo a specific stimuli are added to the map. Depending on how many other dots are close to a dot, the dot\'s color changes from blue to red. The denser the dots, the redder the dots will appear. The user can select the image they want to analyse as well as a constant value \(p\). The closeness of a dot is calculated by taking a dot on the screen and making a virtual circle around it. If another dot is in that circle, the closeness value is increased by 1 for both dots. The dots are put onto the graph with an evenly distributed color coding. The radius of the circle is dynamically changed with the input size of the width and height of the image, and a proportion of the image size constant. The user can self select the value of \(p\). The mathematical formula for the radius of the circle is \(\sqrt{w*h*p \over \pi}\), where \(w=width, h=height, p=\)\(wanted\;area\;of\;circle \over area\;of\;image\). If \(p=0.05\), then the area of the circle is \(5\%\) the area of the rectangle.'
	return render_template('vispage.html', vis_page = vis_page, vis_text=vis_text)

@app.route('/Bar-Chart', methods=['GET', 'POST'])
def index_vis4():
	if request.method == 'POST':
		return redirect(url_for('vispage'))
	vis_page = 'Bar Chart'
	vis_text = 'The idea behind Bar Chart is that you can see....'
	return render_template('vispage.html', vis_page = vis_page, vis_text=vis_text)



#starts the app in debug mode, hit refresh to see an updated page, all without restarting the server. If changing CSS stuff, do a hrd refresh with cmd+shift+r.
if __name__ == "__main__":
	app.run(debug=True)