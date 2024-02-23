import sqlite3

# Set the habit settings of the default user
def setdefault():
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()


        cur.execute("INSERT INTO habits", (new_username, user_id,))
        con.commit()