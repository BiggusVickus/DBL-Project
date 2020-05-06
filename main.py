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
	return render_template('index.html', )

@app.route('/vis1', methods=['GET', 'POST'])
def index_vis1():
	if request.method == 'POST':
		# do stuff when the form is submitted
		# redirect to end the POST handling
		# the redirect can be to the same route or somewhere else
		return redirect(url_for('vispage1'))
	# show the form, it wasn't submitted
	visualization = 1
	return render_template('vispage.html', vis_page = visualization)

@app.route('/vis2', methods=['GET', 'POST'])
def index_vis2():
	if request.method == 'POST':
		# do stuff when the form is submitted
		# redirect to end the POST handling
		# the redirect can be to the same route or somewhere else
		return redirect(url_for('vispage'))
	# show the form, it wasn't submitted
	visualization = 2
	return render_template('vispage.html', vis_page = visualization)

@app.route('/vis3', methods=['GET', 'POST'])
def index_vis3():
	if request.method == 'POST':
		# do stuff when the form is submitted
		# redirect to end the POST handling
		# the redirect can be to the same route or somewhere else
		return redirect(url_for('vispage'))
	# show the form, it wasn't submitted
	visualization = 3
	return render_template('vispage.html', vis_page = visualization)

@app.route('/vis4', methods=['GET', 'POST'])
def index_vis4():
	if request.method == 'POST':
		# do stuff when the form is submitted
		# redirect to end the POST handling
		# the redirect can be to the same route or somewhere else
		return redirect(url_for('vispage'))
	visualization = 4
	# show the form, it wasn't submitted

	return render_template('vispage.html', vis_page = visualization)



if __name__ == "__main__":
	app.run(debug=True)