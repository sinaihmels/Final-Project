import bcrypt 
from functools import wraps
from flask import session, request, redirect, url_for

def hash_password(password: str):
    password = password 
    # converting password to array of bytes 
    bytes = password.encode('utf-8') 
    # generating the salt 
    salt = bcrypt.gensalt() 
    # Hashing the password 
    hash = bcrypt.hashpw(bytes, salt) 
    return hash


# The function check_password_hash takes the hashed password from a specific username from the sql database and compares it with the hashed password given
def check_password_hash(hashuser: str, passwordgiven: str) -> bool:
    hash = hashuser
    # Taking user entered password 
    userPassword = passwordgiven
    # encoding user password 
    userBytes = userPassword.encode('utf-8') 
    # checking password 
    result = bcrypt.checkpw(userBytes, hash) 
    return result

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
