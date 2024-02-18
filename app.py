from flask import Flask, render_template, request, session, redirect, url_for#we import the flask function, render_template, rewuest from the Flask library
from flask_session import Session
app = Flask(__name__) #we initiate the Flask application

@app.route('/') #the / is the decorator (what to put into the URL) the / stands for the index page
def index():

    return render_template('index.html')
