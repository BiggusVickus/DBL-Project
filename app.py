#Dont touch anything here, otherwise everything breaks, especially the first 2 lines. 
from flask import Flask
UPLOAD_FOLDER = '/Upload_Folder'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024