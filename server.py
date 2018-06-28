#!/usr/bin/env python3

__author__ = "Kittisak Phomsri"
__copyright__ = "Copyright 2018, VAMStack Co.,Ltd."
# __license__ = ""
__version__ = "0.0.2"
__maintainer__ = "Kittisak Phomsri"
__email__ = "thekitp@gmail.com"
__status__ = "Development"

# Instant a server
import os
from flask import Flask, request, Response, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = '/tmp/recognition_server/'
ALLOWED_EXTENSIONS = {'png', 'jpg'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Check allowed file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# root path
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Image Uploader</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


# Do display uploaded file
@app.route('/result', methods=['GET'])
def uploaded_file():
    return send_file(UPLOAD_FOLDER + request.args.get('filename'))
