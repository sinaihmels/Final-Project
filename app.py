from flask import Flask, render_template, request, session, redirect, url_for#we import the flask function, render_template, rewuest from the Flask library
from flask_session import Session
app = Flask(__name__) #we initiate the Flask application

@app.route('/') #the / is the decorator (what to put into the URL) the / stands for the index page
def index():
    return render_template('index.html')

@app.route("/login" methods="GET", "POST")
def login():
    session.clear()

    if request.method="GET":
        render_template('login.html')

    if request.method="POST":
        # check that input is not empty 
        if not request.form.get("username"):
            return apology("Must input a username.", 403)

        if not request.form.get("password"):
            return apology("Must input a password.", 403)
        
        # get the data from the matching username from the database and store this in the dictionary data
        data = db.execute(
            "SELECT * FROM users WHERE username=?", request.form.get("username")
        )
        if len(data) != 1:
            return apology("Invalid username.", 403)

        # put the hash password from the database and the password that was in the input into the check_password_hash function
        if not check_password_hash(data[0]["hash"], request.form.get("password")):
            return apology("Invalid password.", 403)
        else:
            # if true log the user in and redirect to index
            session["user_id"] = rows[0]["id"]
            return redirect("/")
        

@app.route("/logout")
def logout():
    return render_template('logout.html')
    # forget who was logged in
    # redirect to log in

@app.route("/settings")
def settings():
    return render_template('settings.html')
    #write the settings function

@app.route("/register")
def register():
    return render_template('register.html')
    # check that the iput is not empty
    # check that the password and the confirmation are identical
    # hash the password with the hash_password function
    # Input the username and the hashed password into the table users 
    # log the user in
    # redirect to index