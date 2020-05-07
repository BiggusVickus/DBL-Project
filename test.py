# #THIS TO DO PYTHON SCRIPT TESTING BEFORE IMPLEMENTING A FEATURE
# import glob
# import random
# import time
# #This randomly selects an image from /static/images to be put on the homepage
# while True:
#     image_list = [name for name in glob.glob('static/images/*')]
#     random_number = random.randint(0, len(image_list)-1)
#     image_for_background = str(image_list[random_number])
#     print (str(random_number) + image_for_background)





# import glob
# import random
# import urllib.request
# from app import app
# from flask import Flask, flash, request, redirect, render_template
# from werkzeug.utils import secure_filename

# #DON"T TOUCH
# UPLOAD_FOLDER = './Uploads'
# app = Flask(__name__)
# app.secret_key = "secret key"
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# #only these files are allowed to be uploaded, will remove pdf compatability later (its convenient for me as when the file searcher pops up, I only see pdfs).
# ALLOWED_EXTENSIONS = set(['csv', 'pdf', 'png', 'jpg', 'jpeg'])

# def allowed_file(filename):
# 	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
# #randomly selects a colored image from Stimuli to be displayed on the front page
# @app.route('/')
# def upload_form():
# 	image_list = [name for name in glob.glob('static/Images/*')]
# 	random_number = random.randint(0, len(image_list)-1)
# 	image_for_background = str(image_list[random_number])
# 	return render_template('index.html', image_for_background=image_for_background)

# @app.route('/', methods=['POST'])
# def upload_file():
# 	if request.method == 'POST':
# 		# check if the post request has the file part
# 		if 'file' not in request.files:
# 			flash('No file part')
# 			return redirect(request.url)
# 		file = request.files['file']
# 		if file.filename == '':
# 			flash('No file selected for uploading')
# 			return redirect(request.url)
# 		if file and allowed_file(file.filename):
# 			filename = secure_filename(file.filename)
# 			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# 			flash('File successfully uploaded')
# 			return redirect('/')
# 		else:
# 			flash('Allowed file types are csv, png, jpg, and jpeg')
# 			return redirect(request.url)

# #creates webpage for the home page
# @app.route('/', methods=['GET', 'POST'])
# def index_home():
# 	if request.method == 'POST':
# 		# do stuff when the form is submitted
# 		# redirect to end the POST handling
# 		# the redirect can be to the same route or somewhere else
# 		return redirect(url_for('index'))
# 	# show the form, it wasn't submitted
# 	return render_template('index.html')

# #creates webpage for the 1st visualization. Also returns welcome to vis 1 and individual description of the visualization. Same comments apply to below, just chnage 1 to 2, 3, or 4. 
# @app.route('/vis1', methods=['GET', 'POST'])
# def index_vis1():
# 	if request.method == 'POST':
# 		return redirect(url_for('vispage1'))
# 	vis_page = 1
# 	vis_text = 'The concept of this graph is to show the user the difference between the scanpath of a colored graph and a noncolored graph. By default the colored image shows on screen and there are checkmarks that allow the user to select if they want to see just the colored scanpath, the black and white, both, or none, with a legend of course. The user can then change the maps as they please.'
# 	return render_template('vispage.html', vis_page = vis_page, vis_text=vis_text)

# @app.route('/vis2', methods=['GET', 'POST'])
# def index_vis2():
# 	if request.method == 'POST':
# 		return redirect(url_for('vispage'))
# 	vis_page = 2
# 	vis_text = 'The goal of this visualization is to show the user how the x and y poition changes with respect to time. The user can see 3 individual graphs. The first graph shows the (x, y) position as the user scans the image. The second graph that the user can see is an (x, time) graph, where as time goes on, the x axis reflects the change in x position of the eyes, thile the y axis reflects the time spent. The thid graph is the opposite, ie the user sees the (time, y) graph. As time moves on the x-axis, the user sees how the y poition of the gazepath changes.'
# 	return render_template('vispage.html', vis_page = vis_page, vis_text = vis_text)

# @app.route('/vis3', methods=['GET', 'POST'])
# def index_vis3():
# 	if request.method == 'POST':
# 		return redirect(url_for('vispage'))
# 	vis_page = 3
# 	vis_text = 'The idea behind this visualization is that the user can see a heatmap of a specific user, map, and map color. It helps  the user understand the density of where the majority of the data is using a fun interactive colorcoding.'
# 	return render_template('vispage.html', vis_page = vis_page, vis_text=vis_text)

# @app.route('/vis4', methods=['GET', 'POST'])
# def index_vis4():
# 	if request.method == 'POST':
# 		return redirect(url_for('vispage'))
# 	vis_page = 4
# 	vis_text = 'The idea behind this visualization is that you can see....'
# 	return render_template('vispage.html', vis_page = vis_page, vis_text=vis_text)

# #starts the app, runs in debug mode so that any changes in code are reflected in the web browser. To get there, cmd+click on 127.0.0.1.5000. If editing CSS, to refresh press cmd+shift+r (use ctrl for windows users)
# if __name__ == "__main__":
# 	app.run(debug=True)