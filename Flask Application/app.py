from email import message
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
from initalize import initalize
from fetch_data import fetch_all_data
import time



## path for upload folder
UPLOAD_FOLDER = 'static/uploads/'
PREDICTION_FOLDER= 'static\\preds\\'


# create and configure the app
app = Flask(__name__)
app.secret_key = "secret key"

## initalization
print("Fetching data")
if app.config.get('data',-1)==-1:
    app.config['data'] = fetch_all_data()
if app.config.get('l1',-1) == -1:
    app.config['l1'] =  initalize(app.config['data'])




def searcher(query_data):

    q_d = app.config['l1'].encodeQueryData(query_data)
    
    lnbr,lnval = app.config['l1'].findSimDocs(q_d)
    # t1 = time.time()
    # t2 = time.time()
    # nnbr,nnval = naiveSimDocs(fdata,query_data,wrds)
    # t3 = time.time()
    #return lnbr,lnval,nnbr,nnval,t1-t0,t3-t2
    return lnbr,lnval

@app.route('/')
def home():
    return render_template('index.html')

## upload image function
@app.route('/Search', methods=['POST'])
def upload_image():
    time.sleep(2)
    querry = request.form['querry']
    #print(querry)
    query_string ='"""' + querry + '"""'
    #print(query_string)
    output = searcher([query_string])
    index= output[0][0].tolist()
    res_data = []
    # print(index)
    for i in index:
        res_data.append(app.config['data'][int(i)][0])
    return render_template('index.html', res_dt = res_data)
    
if __name__ =="__main__":
    app.run(debug=True)