import math
import sqlite3
import habit_db
import random


# 1) CREATE HABIT TABLE
def CreateTaskDetailTable():
    try:
        # SAVE IN MEMORY, EVERYTIME ALL DATA CREATED IS RESTARTED FROM NOTHING
        # db = sqlite3.connect(':memory:')
        db = sqlite3.connect('task_detail.db')
        # db.execute("PRAGMA foreign_keys = 1")  # NOT WORKING: TO ACTIVATE CASCADE FUNC IN SQLITE3
        cur = db.cursor()
    except sqlite3.Error as e:
        print("Error, please try again.")
        exit(1)

    cur.execute("""CREATE TABLE IF NOT EXISTS task_detail (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                week TEXT NOT NULL,
                quantity REAL NOT NULL,
                habit_id INTEGER NOT NULL, 
                FOREIGN KEY (habit_id) REFERENCES habits (habit_id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
                )""")

    db.close()

# 2) AUTO CREATE ROWS IN TABLE WITH DAYS_TO_SUCCESS INFO IN HABITS TABLE
def AutoCreateTaskDetail():
    db = sqlite3.connect('task_detail.db')
    cur = db.cursor()

    # CONNECT TO HABIT DB FOR 'DAYS TO SUCCESS' INFO, FOR CREATE NO. OF ROWS IN TASK DETAIL TABLE
    infos = habit_db.SearchLatestHabit()
    strike_days = infos[0]
    habit_id = infos[1]
    taskname = infos[2]

    # print(f"No of strike days set: {strike_days}")
    for strike_day in range(strike_days):
        week_info = math.ceil((strike_day+1)/7)
        # print(f'{habit_id}: {strike_days} - {week_info}')
        # THIS METHOD DON'T NEED db.commit()
        with db:
            if taskname == 'Listen To Music':
                cur.execute("INSERT INTO task_detail VALUES (null, ?, ?, ?, ?)", (f"Day {strike_day + 1}",  week_info, random.randint(8, 14), habit_id))
            if taskname == 'Play An Instrument':
                cur.execute("INSERT INTO task_detail VALUES (null, ?, ?, ?, ?)", (f"Day {strike_day + 1}", week_info, random.randint(0, 3), habit_id))
            if taskname == 'Sleep':
                cur.execute("INSERT INTO task_detail VALUES (null, ?, ?, ?, ?)", (f"Day {strike_day + 1}", week_info, random.randint(5, 12), habit_id))
            if taskname == 'Run':
                cur.execute("INSERT INTO task_detail VALUES (null, ?, ?, ?, ?)", (f"Day {strike_day + 1}", week_info, random.randint(2, 7), habit_id))
            if taskname == 'Swim':
                cur.execute("INSERT INTO task_detail VALUES (null, ?, ?, ?, ?)", (f"Day {strike_day + 1}", week_info, random.randint(1, 3), habit_id))

    db.close()

# 3) INSERT ROW IN TABLE
def InsertTaskDetail(task):
    db = sqlite3.connect('task_detail.db')
    cur = db.cursor()

    # THIS METHOD DON'T NEED db.commit()
    with db:
        cur.execute("INSERT INTO task_detail VALUES (null, ?, ?, ?, ?)", (task.date, task.week, task.quantity, task.habit_id))
    db.close()

# 4) SEARCH INFO
def SearchTaskDetail(habit_id):
    db = sqlite3.connect('task_detail.db')
    cur = db.cursor()

    cur.execute("SELECT * FROM task_detail WHERE habit_id=:habit_id", {'habit_id': habit_id})
    return cur.fetchall()

    db.close()

# 5) SUM INFO
def SumQuantity(habit_id):
    db = sqlite3.connect('task_detail.db')
    cur = db.cursor()

    cur.execute("SELECT SUM(quantity) FROM task_detail WHERE habit_id=:habit_id GROUP BY week", {'habit_id': habit_id})

    return cur.fetchall()

    db.close()

# 6) SEARCH INFO
def SearchTaskID(date, habit_id):
    db = sqlite3.connect('task_detail.db')
    cur = db.cursor()

    cur.execute("SELECT task_id FROM task_detail WHERE date=:date AND habit_id=:habit_id", {'date': date, 'habit_id': habit_id})
    return cur.fetchall()

    db.close()

# 7) UPDATE INFO
def UpdateTaskDetail(task_id, date, week, quantity):
    db = sqlite3.connect('task_detail.db')
    cur = db.cursor()

    with db:
        cur.execute("""UPDATE task_detail SET date = :date, week = :week, quantity = :quantity
                    WHERE task_id=:task_id""",
                    {'task_id': task_id, 'date': date, 'week': week, 'quantity': quantity})

    db.close()

# 8) REMOVE RECORD
def RemoveTaskDetail(task_id):
    db = sqlite3.connect('task_detail.db')
    cur = db.cursor()

    with db:
        cur.execute("DELETE FROM task_detail WHERE task_id=:task_id", {'task_id': task_id})

    db.close()

# 9) REMOVE RECORD
def RemoveTaskDetailTwo(habit_id):
    db = sqlite3.connect('task_detail.db')
    cur = db.cursor()

    with db:
        cur.execute("DELETE FROM task_detail WHERE habit_id=:habit_id", {'habit_id': habit_id})

    db.close()

# 10) CHECK DATABASE
def CheckDB():
    db = sqlite3.connect('task_detail.db')
    cur = db.cursor()

    cur.execute("SELECT * FROM task_detail")
    return cur.fetchall()

    db.close()

# print(CheckDB())




