#Import all the libraries needed
import os
import requests
import pandas as pd
import flask
import praw
import json
import ktrain
from ktrain import text
from flask import Flask, render_template, request

predictor=ktrain.load_predictor('flairdetector')
predictions=[]
urls=[]
mydict={}

#Create a reddit instance
r=praw.Reddit(client_id='XBKwye9TxZkelw', client_secret='pJPIYzpSWnx3BSMm8xuIQTohQxk', user_agent='Title Extractor')

#Creating an instance
app=Flask(__name__)

#Telling flask what url shoud trigger the function index()
@app.route('/')
@app.route('/flairdetectorfinal')
def index():
    return flask.render_template('flairdetectorfinal.html')

#Function that defines the flair detector
def FlairPredictor(x):
    predictor=ktrain.load_predictor('flairdetector')
    ans=predictor.predict(x)
    return ans

#Function to read url and predict flair
@app.route('/result',methods = ['GET','POST'])
def result():
    #Get url entered in textbox
    try:
            req=request.form['input']
            str=req
    except:
            print("Unable to get URL. Please make sure it's valid and try again.")
    #Getting post from url
    submission=r.submission(url=str)
    x=[]
    #Extracting title from post
    x.append(submission.title)
    #print(x)
    prediction=FlairPredictor(x)
    return flask.render_template("result.html",prediction=prediction)

@app.route('/automated_testing',methods=['POST','GET'])
def automated_testing():
    ffile=request.files['upload_file']
    df=pd.read_csv(ffile.stream)
    count=0
    for index, row in df.iterrows():
        count=count+1
        print("Working on line"+str(count))
        submission=r.submission(url=row[0])
        urls.append(row[0])
        x=[]
        x.append(submission.title)
        prediction=predictor.predict(x)
        #print(prediction)
        predictions.append(prediction)

    for prediction in predictions:
        mydict={urls[i]:predictions[i] for i in range(len(urls))}

    values=[{"key": k, "value": v} for k, v in mydict.items()]
    json_object=json.dumps(values, indent=3)
    print(json_object)
    with open("answer.json", "w") as outfile:
        outfile.write(json_object)
    return flask.send_file("answer.json")
