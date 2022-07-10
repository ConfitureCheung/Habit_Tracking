import sqlite3


# 1) CREATE HABIT TABLE
def CreateHabitTable():
    try:
        # SAVE IN MEMORY, EVERYTIME ALL DATA CREATED IS RESTARTED FROM NOTHING
        # db = sqlite3.connect(':memory:')
        db = sqlite3.connect('habits.db')
        # db.execute("PRAGMA foreign_keys = 1")  # NOT WORKING: TO ACTIVATE CASCADE FUNC IN SQLITE3
        cur = db.cursor()
    except sqlite3.Error as e:
        print("Error, please restart the application again.")
        exit(1)

    cur.execute("""CREATE TABLE IF NOT EXISTS habits (
                habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                taskname TEXT NOT NULL,
                description TEXT,
                operator TEXT NOT NULL,
                target_quantity REAL NOT NULL,
                unit TEXT NOT NULL,
                frequency TEXT NOT NULL,
                days_to_success INTEGER NOT NULL,
                login_id INTEGER NOT NULL, 
                FOREIGN KEY (login_id) REFERENCES users (login_id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
                )""")

    db.close()

# 2) INSERT ROW IN TABLE
def InsertHabit(task):
    db = sqlite3.connect('habits.db')
    cur = db.cursor()

    # THIS METHOD DON'T NEED db.commit()
    with db:
        # cur.execute("INSERT INTO habits VALUES (null, :taskname, :description, :event, :operator, :target_quantity, :unit, :frequency, :days_to_success)",
        #             {'taskname': task.taskname, 'description': task.description, 'event': task.event, 'operator': task.operator, 'target_quantity': task.target_quantity, 'unit': task.unit, 'frequency': task.frequency, 'days_to_success': task.days_to_success})
        cur.execute("INSERT INTO habits VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (task.taskname, task.description, task.operator, task.target_quantity, task.unit, task.frequency, task.days_to_success, task.login_id))
    db.close()

# 3) SEARCH IF ALREADY CREATED PRESET USERS
def SearchFirstHabit(login_id):
    db = sqlite3.connect('habits.db')
    cur = db.cursor()

    cur.execute("SELECT login_id FROM habits WHERE login_id=:login_id", {'login_id': login_id})
    return cur.fetchall()

    db.close()

# 4) SHOW INFO
def AllHabit(login_id):
    db = sqlite3.connect('habits.db')
    cur = db.cursor()

    cur.execute("SELECT habit_id, taskname FROM habits WHERE login_id=:login_id", {'login_id': login_id})
    return cur.fetchall()

    db.close()

# 5) SHOW LATEST ROW INFO
def SearchLatestHabit():
    db = sqlite3.connect('habits.db')
    cur = db.cursor()

    cur.execute("""SELECT days_to_success, habit_id, taskname FROM habits 
                    WHERE habit_id=
                    (SELECT habit_id FROM habits ORDER BY habit_id DESC LIMIT 1)""")

    return cur.fetchall()[0]

    db.close()

# 6) SEARCH INFO
def SearchHabit(habit_id):
    db = sqlite3.connect('habits.db')
    cur = db.cursor()

    cur.execute("SELECT taskname, operator, target_quantity, unit, frequency, days_to_success FROM habits WHERE habit_id=:habit_id", {'habit_id': habit_id})
    return cur.fetchall()

    db.close()

# 7) SEARCH INFO
def DuplicateHabitCheck(taskname):
    db = sqlite3.connect('habits.db')
    cur = db.cursor()

    cur.execute("SELECT * FROM habits WHERE taskname=:taskname", {'taskname': taskname})
    return cur.fetchall()

    db.close()

# 8) UPDATE INFO
def UpdateHabit(habit_id, operator, target_quantity, unit, frequency, days_to_success):
    db = sqlite3.connect('habits.db')
    cur = db.cursor()

    with db:
        cur.execute("""UPDATE habits SET operator = :operator, target_quantity = :target_quantity, unit = :unit, frequency = :frequency, days_to_success = :days_to_success
                    WHERE habit_id=:habit_id""", {'operator': operator, 'target_quantity': target_quantity, 'unit': unit, 'frequency': frequency, 'days_to_success': days_to_success, 'habit_id': habit_id})

    db.close()

# 9) REMOVE RECORD
def RemoveHabit(habit_id):
    db = sqlite3.connect('habits.db')
    cur = db.cursor()

    with db:
        cur.execute("DELETE FROM habits WHERE habit_id = :habit_id", {'habit_id': habit_id})

    db.close()

# 10) CHECK DATABASE
def CheckDB():
    db = sqlite3.connect('habits.db')
    cur = db.cursor()

    cur.execute("SELECT * FROM habits")
    return cur.fetchall()

    db.close()

# print(CheckDB())


