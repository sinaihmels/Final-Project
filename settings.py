import sqlite3

def getuserdata_settings(user_id):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT user_habits.habits_id, habits.name, user_habits.goal, habits.unit, user_habits.position FROM user_habits JOIN habits ON user_habits.habits_id=habits.id WHERE user_id = ?", (user_id,))
        rows = cur.fetchall()
        user_data_settings = []

        for row in rows:
            data_dict = {
                "user_habits.habits_id": row[0],
                "habits.name": row[1],
                "user_habits.goal": row[2],
                "habits.unit": row[3],
                "user_habits.position": row[4]
            }
            user_data_settings.append(data_dict)
        return user_data_settings
 

