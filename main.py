import os
#import magic
import urllib.request
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
# from bokeh.plotting import figure, output_file, show
# from bokeh.embed import file_html
# from bokeh.resources import CDN
# import json
# from bokeh.embed import json_item
# from jinja2 import Template


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

# @app.route('/p1')
# def vis():
# 	# select the tools we want
# 	TOOLS="pan,wheel_zoom,box_zoom,reset,save"

# 	# prepare some data
# 	x = [1, 2, 3, 4, 5]
# 	y = [6, 7, 2, 4, 5]

# 	# output to static HTML file
# 	output_file("whatever.html")

# 	# create a new plot with a title and axis labels
# 	p = figure(title="simple line example", x_axis_label='x', y_axis_label='y' , tools=TOOLS, plot_width=300, plot_height=300)

# 	# add a line renderer with legend and line thickness
# 	p.line(x, y, line_width=2)

# 	# show the results
# 	return json.dumps(json_item(p, "myplot"))


if __name__ == "__main__":
	app.run(debug=True)