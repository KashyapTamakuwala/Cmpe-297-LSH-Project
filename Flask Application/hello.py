from email import message
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename


## path for upload folder
UPLOAD_FOLDER = 'static/uploads/'
PREDICTION_FOLDER= 'static\\preds\\'

## creating app
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PREDICTION_FOLDER'] = PREDICTION_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

## upload image function
@app.route('/upload', methods=['POST'])
def upload_image():
    #print("here")
    return render_template('index.html')
    
if __name__ =="__main__":
    app.run(debug=True)