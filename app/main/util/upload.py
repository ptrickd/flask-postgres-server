import os
from flask import redirect, url_for

from werkzeug.utils import secure_filename
import shortuuid

# from app.main import app

ALLOWED_EXTENSIONS = { 'jpg', 'jpeg', 'png'}
UPLOAD_FOLDER = 'static/uploads/'
# UPLOAD_PATH = os.path.join(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(file):
    filename = 'no filename'
    print('type is', file.filename)
    
    # if user does not select file, browser also
    #submit an empty part without filename
    if file.filename == '':
        return('No selected file')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        split_filename = filename.rsplit('.',1)
        name = split_filename[0]
        extension = split_filename[1]
        old_filename = filename
        filename = name + '-' + shortuuid.uuid() + '.' + extension
        
        file.save(os.path.join('static/uploads/', filename))

        
    return filename
    # return redirect(url_for('upload_file', filename=filename))