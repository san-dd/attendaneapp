from flask import Flask

UPLOAD_FOLDER = 'C:/Users/santo/attendaneapp/static/uploads'
UPLOAD_FOLDER1 = 'C:/Users/santo/AppData/Local/Temp'
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER1'] = UPLOAD_FOLDER1
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024