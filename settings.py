import sqlite3

def getuserdata_settings(user_id):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT user_habits.habits_id, habits.name, user_habits.goal, habits.unit, user_habits.position, habits.descriptionheader1, habits.descriptionheader2 FROM user_habits JOIN habits ON user_habits.habits_id=habits.id WHERE user_id = ?", (user_id,))
        rows = cur.fetchall()
        user_data_settings = []

        for row in rows:
            data_dict = {
                "user_habits.habits_id": row[0],
                "habits.name": row[1],
                "user_habits.goal": row[2],
                "habits.unit": row[3],
                "user_habits.position": row[4],
                "habits.descriptionheader1": row[5],
                "habits.descriptionheader2": row[6]
            }
            user_data_settings.append(data_dict)
        return user_data_settings
 

def changehabits(user_id, checked_habits):
     with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        # get the names of the habits linked to the user_id within the database
        cur.execute("SELECT habits.name FROM habits JOIN user_habits ON habits.id = user_habits.habits_id WHERE user_habits.user_id = ?", (user_id,))
        # create a list with the names of the habits linked to the user_id
        old_habits = set([row[0] for row in cur.fetchall()])
        
        # Habits to be linked (checked_habits - old_habits)
        habits_to_link = set(checked_habits) - old_habits

        # Habits to be unlinked (old_habits - checked_habits)
        habits_to_unlink = old_habits - set(checked_habits)

        # Link new habits
        for habit_name in habits_to_link:
            cur.execute("SELECT id FROM habits WHERE name = ?", (habit_name,))
            habit_id = cur.fetchone()[0]
            cur.execute("INSERT INTO user_habits (user_id, habits_id, progress, goal, position) VALUES (?, ?, 0, 1, 0)", (user_id, habit_id))

        # Unlink old habits
        for habit_name in habits_to_unlink:
            cur.execute("SELECT id FROM habits WHERE name = ?", (habit_name,))
            habit_id = cur.fetchone()[0]
            cur.execute("DELETE FROM user_habits WHERE user_id = ? AND habits_id = ?", (user_id, habit_id))

        con.commit()
        return True
     
def update_goal(habits_id, newgoal, user_id):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE user_habits SET goal = ? WHERE user_id = ? AND habits_id = ?",(newgoal, user_id, habits_id))
        con.commit()
        return True