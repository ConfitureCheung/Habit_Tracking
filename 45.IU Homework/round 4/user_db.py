import sqlite3


# 1) CREATE USER TABLE
def CreateUserTable():
    try:
        # SAVE IN MEMORY, EVERYTIME ALL DATA CREATED IS RESTARTED FROM NOTHING
        # db = sqlite3.connect(':memory:')
        db = sqlite3.connect('users.db')
        cur = db.cursor()
    except sqlite3.Error as e:
        print("Error, please restart the application again.")
        exit(1)

    cur.execute("""CREATE TABLE IF NOT EXISTS users (
                login_id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT,
                password TEXT,
                last_login_date TEXT 
                )""")

    db.close()

# 2) INSERT ROW IN TABLE
def InsertUser(user):
    db = sqlite3.connect('users.db')
    cur = db.cursor()

    # THIS METHOD DON'T NEED db.commit()
    with db:
        cur.execute("INSERT INTO users VALUES (null, :email, :password, :last_login_date)", {'email': user.email, 'password': user.password, 'last_login_date': user.last_login_date})

    db.close()

# 3) SEARCH IF ALREADY CREATED PRESET USERS
def SearchFirstInput(login_id):
    db = sqlite3.connect('users.db')
    cur = db.cursor()

    cur.execute("SELECT login_id FROM users WHERE login_id=:login_id", {'login_id': login_id})
    return cur.fetchall()

    db.close()

# 4) SEARCH INFO
def SearchUser(email):
    db = sqlite3.connect('users.db')
    cur = db.cursor()

    cur.execute("SELECT * FROM users WHERE email=:email", {'email': email})
    return cur.fetchall()

    db.close()

# 5) SHOW LATEST ROW INFO
def FirstRegLoginID():
    db = sqlite3.connect('users.db')
    cur = db.cursor()

    cur.execute("""SELECT login_id FROM users 
                    WHERE login_id=
                    (SELECT login_id FROM users ORDER BY login_id DESC LIMIT 1)""")

    return cur.fetchall()[0]

    db.close()

# 6) UPDATE INFO
def UpdatePassword(login_id, last_login_date):
    db = sqlite3.connect('users.db')
    cur = db.cursor()

    with db:
        cur.execute("""UPDATE users SET last_login_date = :last_login_date
                    WHERE login_id = :login_id""",
                    {'login_id': login_id, 'last_login_date': last_login_date})

    db.close()

# # 7) REMOVE RECORD
# def RemoveUser(user):
#     db = sqlite3.connect('users.db')
#     cur = db.cursor()
#
#     with db:
#         cur.execute("DELETE FROM users WHERE email = :email AND password = :password",
#                     {'email': user.email, 'password': user.password})
#
#     db.close()

# 8) CHECK DATABASE
def CheckDB():
    db = sqlite3.connect('users.db')
    cur = db.cursor()

    cur.execute("SELECT * FROM users")
    return cur.fetchall()

    db.close()

# print(CheckDB())

