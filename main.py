import os
import glob
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template,jsonify
from werkzeug.utils import secure_filename
import importlib

from src import saveuser,searchuser
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#indexpage
@app.route('/adduser')
def upload_form():
	return render_template('upload.html')
#save user details
@app.route('/adduser', methods=['POST'])
def upload_image():
	if 'file1' not in request.files and 'file2' not in request.files and 'file3' not in request.files:
		flash('No file part')
		return redirect(request.url)

	file1,file2,file3 = request.files['file1'],request.files['file2'],request.files['file3']
	if file1.filename == '' and file2.filename == '' and file3.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)

	if file1 and allowed_file(file1.filename) and file2 and allowed_file(file2.filename) and file3 and allowed_file(file3.filename):
		filename1 = secure_filename(request.form['mobno']+"_1."+file1.filename.split(".")[-1])
		filename2 = secure_filename(request.form['mobno']+"_2."+file1.filename.split(".")[-1])
		filename3 = secure_filename(request.form['mobno']+"_3."+file1.filename.split(".")[-1])
  
		file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
		file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
		file3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename3))
  
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

#static image display from folder uploads
@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

#show all register user list
@app.route('/userlist')
def display_user():
	#print('display_image filename: ' + filename)
	userlist=saveuser.listuser()
	if(userlist["success"]):
		print(userlist)
		#flash('Image successfully uploaded and displayed')
		return render_template('userlist.html', userlist=userlist["userlist"])
	else:
		flash('mongodb error')
		return render_template('userlist.html')

#search user using image
@app.route('/', methods=['POST','GET'])
def index():
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
            file1.save(os.path.join(app.config['UPLOAD_FOLDER1'], filename1))
            result=searchuser.searchImages(filename1)
            if(result["success"]):
                userdetails=saveuser.searchuserdetails(list(result["userclass"]))
                if(userdetails["success"]):
                    if len(userdetails["userlist"])==0:flash("user not found")
                    return render_template('searchuser.html',userlist=userdetails["userlist"])
                else:
                    flash("mongodb error")
                    return render_template('searchuser.html')
            else:
                flash('error in recognition module')
                return render_template('searchuser.html')
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return render_template('searchuser.html')
    else:
        return render_template('searchuser.html')
    
#delete user from record
@app.route('/deleteuser/<mobno>',methods=['GET'])
def delete(mobno):
    result=saveuser.deleteuser(mobno)
    if(result["success"]):
        fileList=glob.glob(f'{searchuser.path}/{mobno}*', recursive=True)
        print(f'{searchuser.path}/{mobno}*')
        print(fileList)
        for file in fileList:
            try:
                os.remove(file)
            except OSError:
                print("oserror")
            finally:
                pass
        flash("user deleted successfully")
        return redirect(url_for('display_user'))
    else:
        flash("mongodb error")
        return redirect(request.url)

#refresh model:
@app.route('/modelupdate')
def modelupdate():
    importlib.reload(searchuser)
    flash("model updated successfully")
    return render_template('upload.html')

if __name__ == "__main__":
    app.run()