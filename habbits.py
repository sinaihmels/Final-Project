import sqlite3

# Set the habit settings of the default user
def setdefault():
    with sqlite3.connect("database.db") as con:
        #Set the first habit as water with the default goal 2
        cur = con.cursor()
        cur.execute("INSERT INTO user_habits (user_id, habits_id, progress, goal, position) VALUES (1, 1, 0, 2, 1)")
        con.commit()

        #Set the second habit as workout with the default goal 20
        cur = con.cursor()
        cur.execute("INSERT INTO user_habits (user_id, habits_id, progress, goal, position) VALUES (1, 2, 0, 20, 2)")
        con.commit()

        # Set the third habit as reading with the default goal 10
        cur = con.cursor()
        cur.execute("INSERT INTO user_habits (user_id, habits_id, progress, goal, position) VALUES (1, 3, 0, 10, 3)")
        con.commit()

        # Set the fourth habit as meditating with the default goal 10
        cur = con.cursor()
        cur.execute("INSERT INTO user_habits (user_id, habits_id, progress, goal, position) VALUES (1, 4, 0, 10, 4)")
        con.commit()

        # Set the fifth habit as sleeping with the default goal as 6
        cur = con.cursor()
        cur.execute("INSERT INTO user_habits (user_id, habits_id, progress, goal, position) VALUES (1, 5, 0, 6, 5)")
        con.commit()

        # Set the sixth habit as time outside with default goal as 30
        cur = con.cursor()
        cur.execute("INSERT INTO user_habits (user_id, habits_id, progress, goal, position) VALUES (1, 6, 0, 30, 6)")
        con.commit()


def getdefaultdata():
    with sqlite3.connect("database.db") as con:
        # Get the data from the default user and store them within data
        cur = con.cursor()
        cur.execute("SELECT user_habits.position, habits.name, habits.descriptionheader1, user_habits.goal, habits.descriptionheader2, habits.icon_path, habits.descriptionprogress1, user_habits.progress, habits.descriptionprogress2, habits.descriptionlogmore, habits.unit FROM user_habits JOIN habits ON user_habits.habits_id=habits.id WHERE user_id = 1;")
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
                "habts.unit": row[10]
            }
            default_data.append(data_dict)
        return default_data
        

        

def getuserdata(user_id):
    with sqlite3.connect("database.db") as con:
        # Get the data from the default user and store them within data
        cur = con.cursor()
        cur.execute("SELECT user_habits.position, habits.name, habits.descriptionheader1, user_habits.goal, habits.descriptionheader2, habits.icon_path, habits.descriptionprogress1, user_habits.progress, habits.descriptionprogress2, habits.descriptionlogmore, habits.unit FROM user_habits JOIN habits ON user_habits.habits_id=habits.id WHERE user_id = ?", user_id)
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
                "habts.unit": row[10]
            }
            user_data.append(data_dict)
        return user_data