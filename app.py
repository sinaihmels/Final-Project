from flask import Flask, flash, render_template, request, session, redirect, url_for, Response #we import the flask function, render_template, rewuest from the Flask library
from flask_session import Session
from ssl import AlertDescription
from security import hash_password, check_password_hash, login_required
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
                return Response ("Must input a username", status= 400)

            if not request.form.get("password"):
                return Response ("Must input a password", status = 400)

            username = request.form.get("username")
            
            # get the data from the matching username from the database and store this in the dictionary data
            data = cur.execute("SELECT * FROM users WHERE username=?", (username,))
            user_data = data.fetchone()

            if user_data is None:
                return Response ("Invalid username", status = 400)
            # I still need to check if the username is in the username 

            # put the hash password from the database and the password that was in the input into the check_password_hash function
            if check_password_hash(user_data[2], request.form.get("password")) is False:
                return Response ("Invalid password", status = 400)
            

            # if true log the user in and redirect to index
            session.clear()
            session["user_id"] = user_data[0]
            print(f"logged in {user_data[1]}")
            return redirect("/")

    else:
        return render_template("login.html") 

@app.route("/logout")
@login_required
def logout():
    session.clear()
    print("logged out")
    return render_template("index.html")

    # give the user feedback that they are logged out

    # forget who was logged in
    # redirect to log in

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    return render_template('settings.html')
    #write the settings function



@app.route("/settingsuser", methods= ["GET", "POST"])
@login_required
def settingsuser():
    if request.method == "GET":
        username=session["user_id"]
        return render_template("settingsuser.html", username=username)
    
    if request.method == "POST":
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            # Find out which button was pressed and handle the input accordingly
            one = request.form.get("option1")
            two = request.form.get("option2")
            if one is not None: 
                # the update username button was pressed 
                # validate the input
                if not request.form.get("username"):
                    return Response("Must input a new username", status=400)
                
                # update the username within the database
                new_username = request.form.get("username")
                cur.execute("UPDATE users SET username = ? WHERE id = ?", new_username, session["user_id"])
                con.commit()
                # Tell the user that the name is updated!!

            elif two is not None:
                # the update password button was pressed
                # validate the input 
                if not request.form.get("password"):
                    return Response("Must input password", status=400)
                # check that the old password is correct

                # get the data from the matching username from the database and store this in the dictionary data
                data = cur.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
                user_data = data.fetchone()

                # put the hash password from the database and the password that was in the input into the check_password_hash function
                if check_password_hash(user_data[2], request.form.get("password")) is False:
                    return Response ("Invalid password", status = 400)
            
                if not request.form.get("new_password"):
                    return Response("Must input new password", status=400)
                if not request.form.get("confirmation"):
                    return Response("Must input the new password a second time", status=400)
                if not request.form.get("new_password") == request.form.get("confirmation"):
                    return Response("Must input a matching password and confirmation", status=400)
                
                # hash the new password and update the password within the database
                hashnew = hash_password(request.form.get("new_password"))
                cur.execute("UPDATE users SET hash = ? WHERE id = ?", hashnew, session["user_id"])
                con.commit()
                # Tell the user that the password was updated!!
                

@app.route("/settingsmh")
@login_required
def settingsmh():
    return render_template("settingsmh.html")

@app.route("/settingsdesign")
@login_required
def settingsdesign():
    return render_template("settingsdesign.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            # check that the input is not empty
            if not request.form.get("username"):
                return Response ("Must input a username", status=403)

            username = request.form.get("username")

            # I'm missing checking if the username is already used
            
            if not request.form.get("password"):
                return Response("Must input a password", status=403)
            
            if not request.form.get("confirmation"):
                return Response("Must confirm the password", status=403)
            

            # check that the password and the confirmation are identical
            if not request.form.get("password") == request.form.get("confirmation"):
                return Response("Must input a matching password and confirmation", status=403)
            
            hash = hash_password(request.form.get("password"))

            data = (
                {"username": username, "hash": hash}
            )
            # Input the username and the hashed password into the table users 
            cur.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", data)

            user = cur.execute("SELECT id FROM users WHERE username = ?", (username,))
    
            # log the user in
            session["user_id"] = user.fetchone()[0]
            con.commit()
            
            # redirect to index
            return redirect("/")
    else:
        return render_template("register.html")
    
