import sqlite3

# Set the habit settings of the default user
def setdefault():
    with sqlite3.connect("database.db") as con:
        #Set the first habit as water with the default goal 2
        cur = con.cursor()
        cur.execute("INSERT INTO user_habits (user_id, habits_id, progress, goal, position) VALUES (1, 1, 0, 2, 1)")

        #Set the second habit as workout with the default goal 20
        cur.execute("INSERT INTO user_habits (user_id, habits_id, progress, goal, position) VALUES (1, 2, 0, 20, 2)")

        # Set the third habit as reading with the default goal 10
        cur.execute("INSERT INTO user_habits (user_id, habits_id, progress, goal, position) VALUES (1, 3, 0, 10, 3)")

        # Set the fourth habit as meditating with the default goal 10
        cur.execute("INSERT INTO user_habits (user_id, habits_id, progress, goal, position) VALUES (1, 4, 0, 10, 4)")

        # Set the fifth habit as sleeping with the default goal as 6
        cur.execute("INSERT INTO user_habits (user_id, habits_id, progress, goal, position) VALUES (1, 5, 0, 6, 5)")

        # Set the sixth habit as time outside with default goal as 30
        cur.execute("INSERT INTO user_habits (user_id, habits_id, progress, goal, position) VALUES (1, 6, 0, 30, 6)")
        con.commit()


def setuser_habits(con, cur, user_id):
        #Set the first habit as water with the default goal 2
        cur.execute("INSERT INTO user_habits (user_id, habits_id, progress, goal, position) VALUES (?, 1, 0, 2, 1)", (user_id,))

        #Set the second habit as workout with the default goal 20
        cur.execute("INSERT INTO user_habits (user_id, habits_id, progress, goal, position) VALUES (?, 2, 0, 20, 2)", (user_id,))

        # Set the third habit as reading with the default goal 10
        cur.execute("INSERT INTO user_habits (user_id, habits_id, progress, goal, position) VALUES (?, 3, 0, 10, 3)", (user_id,))

        # Set the fourth habit as meditating with the default goal 10
        cur.execute("INSERT INTO user_habits (user_id, habits_id, progress, goal, position) VALUES (?, 4, 0, 10, 4)", (user_id,))


        # Set the fifth habit as sleeping with the default goal as 6
        cur.execute("INSERT INTO user_habits (user_id, habits_id, progress, goal, position) VALUES (?, 5, 0, 6, 5)", (user_id,))


        # Set the sixth habit as time outside with default goal as 30
        cur.execute("INSERT INTO user_habits (user_id, habits_id, progress, goal, position) VALUES (?, 6, 0, 30, 6)", (user_id,))
        con.commit()

def getdefaultdata():
    with sqlite3.connect("database.db") as con:
        # Get the data from the default user and store them within data
        cur = con.cursor()
        cur.execute("SELECT user_habits.position, habits.name, habits.descriptionheader1, user_habits.goal, habits.descriptionheader2, habits.icon_path, habits.descriptionprogress1, user_habits.progress, habits.descriptionprogress2, habits.descriptionlogmore, habits.unit, habits.id FROM user_habits JOIN habits ON user_habits.habits_id=habits.id WHERE user_id = 1;")
        rows = cur.fetchall()
        # Define a list to store the dicionaries 
        default_data = []

        # iterate over the rows and create a dictionary for each row 
        for row in rows:
            data_dict = {
                "user_habits.position": row[0], 
                "habits.name": row[1], 
                "habits.descriptionheader1": row[2], 
                "user_habits.goal": row[3], 
                "habits.descriptionheader2": row[4], 
                "habits.icon_path": row[5], 
                "habits.descriptionprogress1": row[6], 
                "user_habits.progress": row[7],
                "habits.descriptionprogress2": row[8],
                "habits.descriptionlogmore": row[9],
                "habits.unit": row[10],
                "habits.id": row[11]
            }
            default_data.append(data_dict)
        return default_data
        

        

def getuserdata(user_id):
    with sqlite3.connect("database.db") as con:
        # Get the data from the default user and store them within data
        cur = con.cursor()
        cur.execute("SELECT user_habits.position, habits.name, habits.descriptionheader1, user_habits.goal, habits.descriptionheader2, habits.icon_path, habits.descriptionprogress1, user_habits.progress, habits.descriptionprogress2, habits.descriptionlogmore, habits.unit, habits.id FROM user_habits JOIN habits ON user_habits.habits_id=habits.id WHERE user_id = ?", (user_id,))
        rows = cur.fetchall()
        # Define a list to store the dicionaries 
        user_data = []

        # iterate over the rows and create a dictionary for each row 
        for row in rows:
            data_dict = {
                "user_habits.position": row[0], 
                "habits.name": row[1], 
                "habits.descriptionheader1": row[2], 
                "user_habits.goal": row[3], 
                "habits.descriptionheader2": row[4], 
                "habits.icon_path": row[5], 
                "habits.descriptionprogress1": row[6], 
                "user_habits.progress": row[7],
                "habits.descriptionprogress2": row[8],
                "habits.descriptionlogmore": row[9],
                "habits.unit": row[10],
                "habits.id": row[11]
            }
            user_data.append(data_dict)
        return user_data
    
def update_progress(user_id, habits_id, newprogress):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        # Get current progress
        cur.execute("SELECT progress FROM user_habits WHERE user_id = ? AND habits_id = ?", (user_id, habits_id))
        currentprogress = cur.fetchone()
        if currentprogress is None: 
            currentprogress = 0
        currentprogress = int(currentprogress[0])
        newprogress = int(newprogress)
        # Add the former progress to the newprogress
        newprogress = currentprogress + newprogress
        print(f"newprogress with current: %", newprogress)
        # Update the data
        cur.execute("UPDATE user_habits SET progress = ? WHERE user_id = ? AND habits_id = ?", (newprogress, user_id, habits_id))
        return True