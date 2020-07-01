import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template,jsonify
from werkzeug.utils import secure_filename

from src import saveuser,searchuser

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'file1' not in request.files and 'file2' not in request.files and 'file3' not in request.files:
		flash('No file part')
		return redirect(request.url)

	file1,file2,file3 = request.files['file1'],request.files['file2'],request.files['file3']
	if file1.filename == '' and file2.filename == '' and file3.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)

	if file1 and allowed_file(file1.filename) and file2 and allowed_file(file2.filename) and file3 and allowed_file(file3.filename):
		filename1 = secure_filename(file1.filename)
		filename2 = secure_filename(file2.filename)
		filename3 = secure_filename(file3.filename)
		file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
		file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
		file3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename3))
		#print('upload_image filename: ' + filename)
		print(request.form['fname'])
		#data=jsonify({"fname":request.form['fname'],"lname":request.form['lname'],"emaiid":request.form['emaiid'],"mobno":request.form['mobno']})
		#print("ASAA",data)
		data={}
		data["fname"]=request.form['fname']
		data["lname"]=request.form['lname']
		data["emailid"]=request.form['emailid']
		data["mobno"]=request.form['mobno']
		data["files"]=[filename1,filename2,filename3]
		saveuser.saveuser(data)
		flash('Image successfully uploaded and displayed')
		return render_template('upload.html', filename=[filename1,filename2,filename3])
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/userlist')
def display_user():
	#print('display_image filename: ' + filename)
	userlist=saveuser.listuser()
	print(userlist)
	flash('Image successfully uploaded and displayed')

	return render_template('userlist.html', userlist=userlist)

@app.route('/searchuser', methods=['POST','GET'])
def index():
    print(os.path)
    if (request.method== "POST"):
        if 'file1' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file1= request.files['file1']
        if file1.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file1 and allowed_file(file1.filename):
            filename1 = secure_filename(file1.filename)
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            result=searchuser.searchImages(filename1)
            return render_template('searchuser.html',userdata=result)
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return render_template('searchuser.html')
    else:
        return render_template('searchuser.html')
if __name__ == "__main__":
    app.run()