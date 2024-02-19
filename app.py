from flask import Flask, render_template, request, session, redirect, url_for#we import the flask function, render_template, rewuest from the Flask library
from flask_session import Session
app = Flask(__name__) #we initiate the Flask application

@app.route('/') #the / is the decorator (what to put into the URL) the / stands for the index page
def index():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "GET":
        render_template('login.html')

    if request.method == "POST":
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

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check that the input is not empty
        if not request.form.get("username"):
            return apology("Must input a username", 403)
        
        # check that the input is not already used 
        if request.form.get("username") == db.execute ("SELECT username WHERE username = ?", request.form.get("username")):
            return apology("Must input a different username", 403)
        
        if not request.form.get("password"):
            return apology("Must input a password", 403)
        
        if not request.form.get("confirmation"):
            return apology("Must confirm the password", 403)
        

        # check that the password and the confirmation are identical
        if not request.form.get("password") == request.form.get("confirmation"):
            return apology("Must input a matchig password and confirmation", 403)
            

        # Input the username and the hashed password into the table users 
        db.execute (
            "INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), hash_password(request.form.get("password"))
                    )
        
        data = db.execute (
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # log the user in
        session["user_id"] = data[0]["id"]
        
        # redirect to index
        return redirect("/")
    else:
        return render_template("register.html")