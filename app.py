from flask import Flask, render_template, request, session, redirect, url_for#we import the flask function, render_template, rewuest from the Flask library
from flask_session import Session
app = Flask(__name__) #we initiate the Flask application

@app.route('/') #the / is the decorator (what to put into the URL) the / stands for the index page
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')
    #write the login function

@app.route("/logout")
def logout():
    return render_template('logout.html')
    #write the logout function

@app.route("/settings")
def settings():
    return render_template('settings.html')
    #write the settings function

@app.route("/register")
def register():
    return render_template('register.html')
    #write the register function