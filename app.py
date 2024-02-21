from flask import Flask, flash, render_template, request, session, redirect, url_for #we import the flask function, render_template, rewuest from the Flask library
from flask_session import Session
from ssl import AlertDescription
from security import hash_password, check_password_hash
import sqlite3

app = Flask(__name__) #we initiate the Flask application
# Secret Key 
app.secret_key = b'91e7fb421e04cdb4d42f16860b24000a0018fe6da614105bf088cbd775c06f52'
# Initialize the Database




@app.route('/') #the / is the decorator (what to put into the URL) the / stands for the index page
def index():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            # check that input is not empty 
            if not request.form.get("username"):
                flash("Must input a username, 403")

            if not request.form.get("password"):
                flash("Must input a password., 403")
            
            # get the data from the matching username from the database and store this in the dictionary data
            data = cur.execute(
                "SELECT * FROM users WHERE username=?", request.form.get("username")
            )

            if len(data) != 1:
                flash("Invalid username.", 403)

            # put the hash password from the database and the password that was in the input into the check_password_hash function
            if not check_password_hash(data.fetchone()[2], request.form.get("password")):
                flash("Invalid password.", 403)
            
            # if true log the user in and redirect to index
            session.clear()
            session["user_id"] = data.fetchone()[0]
            return redirect("/")

    else:
        return render_template("login.html") 

@app.route("/logout")
def logout():
    return render_template('logout.html')
    # forget who was logged in
    # redirect to log in

@app.route("/settings")
def settings():
    return render_template('settings.html')
    #write the settings function

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            # check that the input is not empty
            if not request.form.get("username"):
                flash("Must input a username", 403)

            username = request.form.get("username")

            # I'm missing checking if the username is already used
            
            if not request.form.get("password"):
                flash("Must input a password", 403)
            
            if not request.form.get("confirmation"):
                flash("Must confirm the password", 403)
            

            # check that the password and the confirmation are identical
            if not request.form.get("password") == request.form.get("confirmation"):
                flash("Must input a matching password and confirmation", 403)
            
            hash = hash_password(request.form.get("password"))

            data = (
                {"username": username, "hash": hash}
            )
            # Input the username and the hashed password into the table users 
            cur.execute ("INSERT INTO users (username, hash) VALUES(:username, :hash)", data)

    
            user = cur.execute ("SELECT id FROM users WHERE username = ?", (username,))
    

            # log the user in
            session["user_id"] = user.fetchone()[0]
            con.commit()
            
            # redirect to index
            return redirect("/")
    else:
        return render_template("register.html")