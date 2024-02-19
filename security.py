from ssl import AlertDescription
import bcrypt 

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
    print(result)

