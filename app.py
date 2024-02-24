from flask import Flask, flash, render_template, request, session, redirect, url_for, Response, redirect #we import the flask function, render_template, rewuest from the Flask library
from flask_session import Session
from ssl import AlertDescription
from security import hash_password, check_password_hash, login_required
from habits import setdefault, getdefaultdata, getuserdata, setuser_habits
from settings import getuserdata_settings
import sqlite3

app = Flask(__name__) #we initiate the Flask application
# Secret Key 
# Note It’s essential to store the secret key in a secure environment, rather than hardcoding it directly within the application.
# TODO store the secret key in a secure environment
app.secret_key = b'91e7fb421e04cdb4d42f16860b24000a0018fe6da614105bf088cbd775c06f52'
# Initialize the Database

# Set the default user in the database 
# setdefault() This didn't work but I only have to set it once so its best that it didn't work

@app.route('/') #the / is the decorator (what to put into the URL) the / stands for the index page
def index():
    # if the session is not empty
        # implement the habits found in the habits table 
        # render_template with the data 
    
    if session.get("user_id") is None:
    # if session is empty (no one is logged in)
        # render_template with the data of the default user 
        rows = getdefaultdata()
        return render_template('index.html', rows=rows)
    
    else:
        # if there is a user logged in (there is a user_id in session)
        # render_template with the data from the user
        user_id = session["user_id"]
        rows = getuserdata(user_id)
        return render_template('index.html', rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            # check that input is not empty 
            if not request.form.get("username"):
                flash("Must input a valid username", "error")
                return render_template("login.html") 

            if not request.form.get("password"):
                #error = 'Must input a valid password'
                flash("Must input a valid password.", "error")
                return render_template("login.html")

            username = request.form.get("username")
            
            # get the data from the matching username from the database and store this in the dictionary data
            data = cur.execute("SELECT * FROM users WHERE username=?", (username,))
            user_data = data.fetchone()

            if user_data is None:
                flash("Must input a valid username", "error")
                return render_template("login.html") 
            # I still need to check if the username is in the username 

            # put the hash password from the database and the password that was in the input into the check_password_hash function
            if check_password_hash(user_data[2], request.form.get("password")) is False:
                flash("Must input a valid password", "error")
                return render_template("login.html") 
   
            # if true log the user in and redirect to index
            session.clear()
            session["user_id"] = user_data[0]
            flash("You were successfully logged in.", "success")
            return redirect("/")
        
    return render_template("login.html") 

@app.route("/logout")
@login_required
def logout():
    # forget who was logged in
    session.clear()
    # give the user feedback that they are logged out
    flash("You were successfully logged out.", "success")
    # redirect to index
    return render_template("index.html")

    



@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    return render_template('settings.html')
    #write the settings function



@app.route("/settingsuser", methods= ["GET", "POST"])
@login_required
def settingsuser():
    if request.method == "GET":
        return render_template("settingsuser.html")
    
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
                    flash("403: Must input a new username", "error")
                    return render_template("settingsuser.html")
                
                # update the username within the database
                new_username = request.form.get("username")
                user_id = session["user_id"]
                cur.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user_id,))
                con.commit()
                flash("The username was successfully updated", "success")
                return render_template("settingsuser.html")
                # TODO Tell the user that the name is updated!!

            elif two is not None:
                # the update password button was pressed
                # validate the input 
                if not request.form.get("password"):
                    flash("403: Must input a password", "error")
                    return render_template("settingsuser.html")
            

                user_id = session["user_id"]
                # get the data from the matching username from the database and store this in the dictionary data
                data = cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
                user_data = data.fetchone()

                # put the hash password from the database and the password that was in the input into the check_password_hash function
                if check_password_hash(user_data[2], request.form.get("password")) is False:
                    flash("403: Must input a valid password", "error")
                    return render_template("settingsuser.html")

            
                if not request.form.get("new_password"):
                    flash("403: Must input the new password", "error")
                    return render_template("settingsuser.html")
                if not request.form.get("confirmation"):
                    flash("403: Must input the new password a second time", "error")
                    return render_template("settingsuser.html")
                if not request.form.get("new_password") == request.form.get("confirmation"):
                    flash("403: Must input a matching new password and confirmation", "error")
                    return render_template("settingsuser.html")
                
                # hash the new password and update the password within the database
                hashnew = hash_password(request.form.get("new_password"))
                cur.execute("UPDATE users SET hash = ? WHERE id = ?", (hashnew, user_id,))
                con.commit()
                # Tell the user that the password was updated!
                flash("The password was successfully updated", "success")
                return render_template("settingsuser.html")
                
    return redirect("/settingsuser")
                

@app.route("/settingsmh", methods= ["GET", "POST"])
@login_required
def settingsmh():
    if request.method == "GET":
        user_id = session["user_id"]
        rows = getuserdata_settings(user_id=user_id)
        return render_template("settingsmh.html", rows=rows)
    
    if request.method == "POST":
        # if the submit button to select the habbits is submitted 
        if request.form.get("habit"):
            # get a list of the checked checkboxes from the form
            checked_habits = request.form.getlist('habit')
            print(checked_habits)
            
            # iterate over the list and validate the input
            if len(checked_habits) is None:
                flash("403: Must check at least one habit", "error")
                user_id = session["user_id"]
                rows = getuserdata_settings(user_id=user_id)
                return render_template("settingsmh.html", rows=rows)
            

            # if not 6 habits are checked return flash 
             # check that 6 habits are checked 
                # update user_settings so that when the page reloads the correct habits are displayed 

        user_id = session["user_id"]
        rows = getuserdata_settings(user_id=user_id)
        return render_template("settingsmh.html", rows=rows)


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
                flash("403: Must input a username", "error")
                return render_template("register.html")

            username = request.form.get("username")

            # I'm missing checking if the username is already used

            existing_user = cur.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
            if existing_user:
                flash("403: Username already exists. Please choose another one.", "error")
                return render_template("register.html")
            
            if not request.form.get("password"):
                flash("403: Must input a password", "error")
                return render_template("register.html")
            
            if not request.form.get("confirmation"):
                flash("403: Must confirm the password", "error")
                return render_template("register.html")
            

            # check that the password and the confirmation are identical
            if not request.form.get("password") == request.form.get("confirmation"):
                flash("403: Must input a matching password and confirmation", "error")
                return render_template("register.html")
            
            hash = hash_password(request.form.get("password"))

            data = (
                {"username": username, "hash": hash}
            )
            # Input the username and the hashed password into the table users 
            cur.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", data)
            con.commit()

            user = cur.execute("SELECT id FROM users WHERE username = ?", (username,))
            user_id = user.fetchone()[0]
            # log the user in
            session["user_id"] = user_id
            

            # set the user_habits to the default habits settings 
            setuser_habits(con, cur, user_id)
     
            # redirect to index
            flash("You were successfully logged in.", "success")
            return redirect("/")
    else:
        return render_template("register.html")
    
