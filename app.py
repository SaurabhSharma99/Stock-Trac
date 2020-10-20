from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
import json
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime

authent_key="013EI0MDSY4HVSIJ"
base_url= "https://www.alphavantage.co/query?"


Prestige_comp=['goog','msft','amzn','aapl','fb']
list_of_dict=[]
for x in Prestige_comp:
    URL= base_url+"function=GLOBAL_QUOTE&symbol={}&apikey={}".format(x,authent_key)
    response= requests.get(URL)
    ans=response.json()
    list_of_dict.append(ans.copy())





local_server = True

with open('config.json','r') as c:
    params=json.load(c)["params"]


app = Flask(__name__)
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

# sno,name,email,mobileno,message
#table for adding comments in the users section of stocktrack database
class Addcomments(db.Model):
    sno= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(20), nullable=False)
    mobile_no= db.Column(db.String(12), nullable=False)
    message=db.Column(db.String(120), nullable=False)




# API calls for liststock html page




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/data')
def domain():
    return render_template('data.html')

@app.route('/invest')
def hosting():
    return render_template('invest.html')

@app.route('/liststock')
def blog():
    return render_template('liststock.html',final_list=list_of_dict)

@app.route('/contact')
def contact():
    return render_template('contact.html')

#Plot test in python
@app.route("/test")
def chartText():
    arr = []
    for i in range(5):
        arr.append(float(list_of_dict[i]['Global Quote']['02. open']))
    plt.plot(arr)
    plt.title('Plot of five companies with opening price')
    plt.savefig('static/images/new_plot.png')
    return render_template('plot.html', name = 'Sample Plot', url = 'static/images/new_plot.png')

# sno,name,email,mobileno,message

@app.route('/users', methods=['GET','POST'])
def users():    
    if(request.method=='POST'):
        #add entry to the database
        name=request.form.get('name')
        email=request.form.get('email')
        mno=request.form.get('mobileno')
        message=request.form.get('message')
        entry=Addcomments(name=name,email=email, mobile_no=mno, message=message)
        db.session.add(entry)
        db.session.commit()
    return render_template('users.html')
app.run(debug=True)