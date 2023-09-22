import os
from datetime import datetime
from pymongo.mongo_client import MongoClient
from werkzeug.utils import secure_filename
from flask import Flask, render_template,redirect, request, jsonify

app = Flask(__name__)
UPLOAD_FOLDER = '/Users/samasakethreddy/Downloads/pythonProject/pinacaLabs_Assignment/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
MONGO_URI ='mongodb+srv://19e11a0541:nPWOlzxduLwtCVLV@cluster0.mfhmxwg.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp'

def connect():
    mongo = MongoClient(MONGO_URI)
    print('connected to db')
    return mongo

@app.route('/upload', methods=['GET', 'POST'])
def uploader():
    if request.method == 'GET':
        return render_template('Home.html')
    else:
        data = request.files['file']
        mongo = connect()
        filename = secure_filename(data.filename)
        if mongo.flaskdb.filePaths.find_one({"file":filename}):
                return '''<p style="color:red">File exists !!!</p>
                <a href = "/upload">try again</a>'''
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        data.save(path)
        mongo.flaskdb.filePaths.insert_one({'file':filename, 'path':path,'uploaded_on':datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
        return f'uploaded succesfully'
        

@app.route('/get', methods=['GET','POST'])
def get_info():
    if request.method == 'GET':
        return render_template('get.html')
    else:
        filename = str(request.form['file'])
        mongo = connect()
        data = mongo.flaskdb.filePaths.find_one({"file":filename})
        if data:
            path = data['path']
            info = os.stat(path)
            extension = filename.split('.')[-1]
            dict = {
                "file":filename,
                "format":extension,
                "filesize":f'{info.st_size} bytes',
                "path":path,
                "uploaded_on":data['uploaded_on']
            }
            return jsonify(dict)
        else:
            return '''<p style="color:red">Please enter a valid file name !!!</p>
            <a href = "/get">try again</a>'''


if __name__ == '__main__':
    app.run(debug=True, port=5001)
