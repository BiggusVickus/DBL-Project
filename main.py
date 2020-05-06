import os
#import magic
import urllib.request
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './Uploads'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


ALLOWED_EXTENSIONS = set(['csv', 'pdf', 'png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash('File successfully uploaded')
			return redirect('/')
		else:
			flash('Allowed file types are csv, png, jpg, and jpeg')
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

@app.route('/vis1', methods=['GET', 'POST'])
def index_vis1():
	if request.method == 'POST':
		# do stuff when the form is submitted
		# redirect to end the POST handling
		# the redirect can be to the same route or somewhere else
		return redirect(url_for('vispage1'))
	# show the form, it wasn't submitted
	vis_page = 1
	vis_text = 'The concept of this graph is to show the user the difference between the scanpath of a colored graph and a noncolored graph. By default the colored image shows on screen and there are checkmarks that allow the user to select if they want to see just the colored scanpath, the black and white, both, or none, with a legend of course. The user can then change the maps as they please.'
	return render_template('vispage.html', vis_page = vis_page, vis_text=vis_text)

@app.route('/vis2', methods=['GET', 'POST'])
def index_vis2():
	if request.method == 'POST':
		# do stuff when the form is submitted
		# redirect to end the POST handling
		# the redirect can be to the same route or somewhere else
		return redirect(url_for('vispage'))
	# show the form, it wasn't submitted
	vis_page = 2
	vis_text = 'The goal of this visualization is to show the user how the x and y poition changes with respect to time. The user can see 3 individual graphs. The first graph shows the (x, y) position as the user scans the image. The second graph that the user can see is an (x, time) graph, where as time goes on, the x axis reflects the change in x position of the eyes, thile the y axis reflects the time spent. The thid graph is the opposite, ie the user sees the (time, y) graph. As time moves on the x-axis, the user sees how the y poition of the gazepath changes.'
	return render_template('vispage.html', vis_page = vis_page, vis_text = vis_text)

@app.route('/vis3', methods=['GET', 'POST'])
def index_vis3():
	if request.method == 'POST':
		# do stuff when the form is submitted
		# redirect to end the POST handling
		# the redirect can be to the same route or somewhere else
		return redirect(url_for('vispage'))
	# show the form, it wasn't submitted
	vis_page = 3
	vis_text = 'The idea behind this visualization is that the user can see a heatmap of a specific user, map, and map color. It helps  the user understand the density of where the majority of the data is using a fun interactive colorcoding.'
	return render_template('vispage.html', vis_page = vis_page, vis_text=vis_text)

@app.route('/vis4', methods=['GET', 'POST'])
def index_vis4():
	if request.method == 'POST':
		# do stuff when the form is submitted
		# redirect to end the POST handling
		# the redirect can be to the same route or somewhere else
		return redirect(url_for('vispage'))
	vis_page = 4
	vis_text = 'The idea behind this visualization is that you can see....'
	# show the form, it wasn't submitted

	return render_template('vispage.html', vis_page = vis_page, vis_text=vis_text)



if __name__ == "__main__":
	app.run(debug=True)