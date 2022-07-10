import user_db, habit_db, task_detail_db
import math
from colorama import Fore, Back, Style
from datetime import date, datetime
import re, os, sys


''' 
4) RUN TO SEE IF STILL ERROR (CHECKED TWICE ALREADY)
6) STUDY UNITTEST AND WATCH YOUTUBE
'''

# PART 0) CLASS FOR USERS, HABITS, TASK RECORD
# ------------------------------
class UserCreate:
    def __init__(self, email, password, last_login_date):
        self.email = email
        self.password = password
        self.last_login_date = last_login_date


class HabitCreate:
    def __init__(self, taskname, description, operator, target_quantity, unit, frequency, days_to_success, login_id):
        self.taskname = taskname
        self.description = description
        self.operator = operator
        self.target_quantity = target_quantity  # FLOAT
        self.unit = unit
        self.frequency = frequency
        self.days_to_success = days_to_success  # INTEGER
        self.login_id = login_id


class RecordCreate:
    def __init__(self, date, week, quantity, habit_id):
        self.date = date
        self.week = week
        self.quantity = quantity
        self.habit_id = habit_id


# PART 1) SET MESSAGE COLOR
# ------------------------------
def ErrorMsg(msg):  # TESTED
    print(f'{Fore.RED}{msg}\n{Style.RESET_ALL}')


def InfoMsg(msg):  # TESTED
    print(f'{Fore.BLUE}{msg}{Style.RESET_ALL}')


def EnquiryMsg(msg):  # TESTED
    return f'{Fore.CYAN}{msg}{Style.RESET_ALL}'


def AnalysisMsgS(msg):  # TESTED
    print(f'{Fore.GREEN}{msg}{Style.RESET_ALL}')


def AnalysisMsgF(msg):  # TESTED
    print(f'{Fore.LIGHTRED_EX}{msg}{Style.RESET_ALL}')


# PART 2) LOGIN PANEL
# ------------------------------
def LoginOption():  # TESTED
    input_lo = input(EnquiryMsg('Welcome to the habit tracking app!\nPlease pick your action, "R" for Register, "L" for Login: ')).upper()
    # print(input_lo)
    global vl
    if input_lo == 'R':
        InfoMsg("Register panel starts.")
        ve = VerifyEmail()
        vp = VerifyPassword()
        vd = VerifyDuplicate()
        vl = user_db.SearchUser(ve)
        # print(vl)  # [(6, 'test6@gmail.com', 'TEST6789', '2022-07-07')]
        EmailRegisterUserPanel()

    elif input_lo == 'L':
        InfoMsg("Login panel starts.")
        vl = VerifyLogin()
        # print(vl)  # [(1, 'test1@gmail.com', 'TEST1234', '2022-01-04')]
        EmailLoginUserPanel()

    else:
        ErrorMsg('Invalid selection. Please try again!')
        return LoginOption()


# PART 3) REGISTER / LOGIN RELATED
# ------------------------------
# # FOR USER REGISTRATION # #
def EmailRegister():  # TESTED
    input_er = input(EnquiryMsg('Please enter a valid email: '))  # jamjamgmail.com
    return input_er


def PasswordRegister():  # TESTED
    InfoMsg('*Password requirements:\n1)8-20 characters long\n2)in 1 word\n3)at least 1 uppercase letter & 1 number\n')
    input_pr = input(EnquiryMsg('Please enter a valid password: '))  # 123 444
    return input_pr


# CHECK IF EMAIL FORMAT IS VALID
def VerifyEmail():  # TESTED
    global email_register
    email_register = EmailRegister()
    # print(email_register)
    if '@' not in email_register or not email_register.endswith('.com'):
        ErrorMsg(f'"{email_register}" is an invalid email account. Please try again.')
        return VerifyEmail()
    return email_register


# CHECK IF PASSWORD FORMAT IS VALID
def VerifyPassword():  # TESTED
    global password_register
    password_register = PasswordRegister()
    # print(password_input)
    # 1) 8-20 CHARACTERS LONG
    if len(password_register) < 8 or 20 < len(password_register):
        ErrorMsg('Password needs to be within 8 to 20 characters. Please try again.')
        return VerifyPassword()
    # 2) IN 1 WORD
    if " " in password_register:
        ErrorMsg('Password is not in 1 word. Please try again.')
        return VerifyPassword()
    # 3) AT LEAST 1 UPPERCASE LETTER & 1 INTEGER
    is_uppercase = re.search(r'[A-Z]', password_register)
    if not is_uppercase:
        ErrorMsg('Password needs at least 1 uppercase letter. Please try again.')
        return VerifyPassword()
    is_integer = re.search(r'[0-9]', password_register)
    if not is_integer:
        ErrorMsg('Password needs at least 1 integer. Please try again.')
        return VerifyPassword()


# CHECK IF EMAIL & PASSWORD MATCHED DATABASE
def VerifyDuplicate():  # TESTED
    today = date.today()
    # print(email_register, password_register)
    duplicated_user = user_db.SearchUser(email_register)
    if len(duplicated_user) == 1:
        ErrorMsg(f'"{duplicated_user[0][1]}" has already been registered. Please try a new one.')  # PRINT ONLY THE EMAIL (1ST ROW 1ST ITEM)
        return LoginOption()
    else:
        today_conversion = TodayConversion(today)
        # print(today_conversion)
        user_new = UserCreate(email_register, password_register, today_conversion)
        insert_user = user_db.InsertUser(user_new)


# ------------------------------
# # FOR USER LOGIN # #
def EmailLogin():  # TESTED
    input_el = input(EnquiryMsg('Please enter the login email: '))  # test6@gmail.com, test7@gmail.com, test8@gmail.com
    return input_el


def PasswordLogin():  # TESTED
    input_3 = input(EnquiryMsg('Please enter the login password: '))  # TEST6789, TEST7890, TEST8901
    return input_3


# CHECK IF EMAIL & PASSWORD MATCHED THE DATABASE SYSTEM
def VerifyLogin():  # TESTED
    email_login = EmailLogin()
    password_login = PasswordLogin()
    users = user_db.SearchUser(email_login)
    # print(users[0][1], users[0][2], users[0][3])  # [('test1@gmail.com', 'TEST1234', '2022-01-04')]
    # CHECK IF EMAIL FOUND IN DATABASE
    if len(users) == 0:
        ErrorMsg('Login not found, please try again!')
        return LoginOption()
    if password_login == users[0][2]:
        InfoMsg('Login Successful!\n')
    else:
        ErrorMsg('Password incorrect, please try again!')
        return LoginOption()
    return users


# ------------------------------
# # FOR LOGIN DATE # #
def TodayConversion(new_login_date):  # TESTED
    today = date.today()
    new_login_date = today.strftime('%Y-%m-%d')
    # print(type(new_login_date), new_login_date)
    return new_login_date


# PART 0) CHECK DATE DIFF
def DateDiff():  # TESTED
    today = date.today()
    record_date = datetime.strptime(vl[0][3], '%Y-%m-%d').date()

    if today == record_date:
        date_diff = 0
    else:
        date_diff = int(str(today - record_date).split(" ")[0])
    if date_diff != 0:
        InfoMsg(f'It has been {date_diff} days since your last login.')
    if date_diff > 7:
        InfoMsg(f'It is important for you to login regularly to build up good habit!')
    print('')


# PART 4) EMAIL LOGIN USER PANEL
# ------------------------------
def EmailLoginUserPanel():
    today = date.today()
    InfoMsg('Welcome back! Please wait for a moment, data is loading...')
    date_diff = DateDiff()

    today_conversion = TodayConversion(today)
    # print(today_conversion)

    update_login_date = user_db.UpdatePassword(vl[0][0], today_conversion)

    while True:
        action_to_take = ActionToTake()


# PART 5) EMAIL REGISTER USER PANEL
# ------------------------------
def EmailRegisterUserPanel():
    InfoMsg('Please wait for a moment, data is loading...\n')
    # CREATE HABIT TABLE WITH 5 TASKS CREATED (1 WEEKLY, 1 DAILY) WITH 4 WEEKS DATA
    create_table = habit_db.CreateHabitTable()
    create_table2 = task_detail_db.CreateTaskDetailTable()

    # GET LATEST USER ID
    last_login_id = user_db.FirstRegLoginID()
    # print(f'Last login id is: {last_login_id[0]}')

    # CHECK IF ALREADY HAVE CREATED PRESET HABITS
    search_first_habit = habit_db.SearchFirstHabit(last_login_id[0])
    # print(len(search_first_habit), search_first_habit)

    # ADD ONLY ONCE
    if len(search_first_habit) == 0:
        InfoMsg('Loading in 5 preset habits...\n')
        # HabitCreate(taskname, description, event, operator, target_quantity, unit, frequency, days_to_Success, login_id)
        habit_1 = HabitCreate('Listen To Music', 'Enjoy relax time', 'at least', 10, 'songs', 'daily', 30, last_login_id[0])
        habit_2 = HabitCreate('Play An Instrument', 'Build up the art sense', 'at least', 12, 'hours', 'weekly', 28, last_login_id[0])
        habit_3 = HabitCreate('Sleep', 'Recover the energy', 'at least', 6.5, 'hours', 'daily', 40, last_login_id[0])
        habit_4 = HabitCreate('Run', 'Build up strength', 'at least', 3, 'times', 'weekly', 28, last_login_id[0])
        habit_5 = HabitCreate('Swim', 'Build up strength', 'at least', 0.75, 'hours', 'weekly', 35, last_login_id[0])
        preset_habits_list = [habit_1, habit_2, habit_3, habit_4, habit_5]
        for preset_habit in preset_habits_list:
            insert_habit = habit_db.InsertHabit(preset_habit)

            # EXTRACT DAYS OF SUCCESS INFO FROM HABIT DB AND CREATE ROWS IN TASK DETAIL DB
            auto_create = task_detail_db.AutoCreateTaskDetail()

    # # CHECK CREATED ROWS FOR THE 4 WEEKS DATA
    # for i in range(5):
    #     search_check = task_detail_db.SearchTaskDetail(i + 1)
    #     print(search_check)

    InfoMsg('We have 5 preset habits for your reference on how to store and review the habit.\n')

    while True:
        action_to_take = ActionToTake()


# PART 6)
# ------------------------------
# DIFFERENT ACTIONS SELECTED BY USER
def ActionToTake():
    input_atk = input(EnquiryMsg('Please advise what you want to do: \n"A" for "VIEW all habits",\n"B" for "VIEW records of a selected habit",\n'
                                 '"C" for "ADD a new habit",\n"D" for "ADD a record for a habit",\n"E" for "EDIT a habit",\n'
                                 '"F" for "EDIT record for a specific habit",\n"G" for "DELETE a habit",\n'
                                 '"H" for "DELETE record for a specific habit" or\n"I" for "EXIT the app": \n')).upper()

    # VIEW ALL HABITS
    if input_atk == "A":
        show_all_habits_only = ShowAllHabitOnly()

    # VIEW RECORDS OF A SELECTED HABIT
    elif input_atk == "B":
        show_all_habits = ShowAllHabits()
        # SELECT TO DISPLAY INDIVIDUAL HABIT
        # KEEP THIS FOR EASIER UNDERSTANDING
        habit_infos = habit_db.SearchHabit(show_all_habits)
        habit_name = habit_infos[0][0]
        habit_operator = habit_infos[0][1]
        habit_target_qty = habit_infos[0][2]
        habit_unit = habit_infos[0][3]
        habit_frequency = habit_infos[0][4]
        habit_strike_day = habit_infos[0][5]
        InfoMsg('## Habit Selection ##')
        InfoMsg(f'{habit_name} for {habit_operator} {habit_target_qty} {habit_unit} {habit_frequency} in {habit_strike_day} days\n')

        if habit_frequency == 'daily':
            task_details = task_detail_db.SearchTaskDetail(show_all_habits)
            # ANALYSIS SESSION
            strike_success_list, strike_fail_list, strike_count_list = [], [], []
            for task_detail in task_details:
                days_info = task_detail[1]
                weeks_info = task_detail[2]
                actual_qty_info = task_detail[3]
                # print(days_info, weeks_info, actual_qty_info)

                if habit_operator == "at least":
                    strike_result = actual_qty_info >= habit_target_qty
                elif habit_operator == "less than":
                    strike_result = actual_qty_info <= habit_target_qty
                strike_count_list.append(strike_result)
                if strike_result == True:
                    AnalysisMsgS(f'{days_info} record: {actual_qty_info} {habit_unit} meets the target!')
                    strike_success_list.append(1)
                elif strike_result == False:
                    AnalysisMsgF(f'{days_info} record: {actual_qty_info} {habit_unit} fails to meet the target.')
                    strike_fail_list.append(1)

            InfoMsg('####################')
            longest_strike = LongestStrike(strike_count_list)
            AnalysisMsgS(f'Your longest strike for this habit is: {longest_strike}!')

            AnalysisMsgS(f'Strike completion: {len(strike_success_list)}/{habit_strike_day}')
            if len(strike_fail_list) > 0:
                AnalysisMsgF('Sorry, consecutive strike fail!\n')
            else:
                AnalysisMsgS('Congratulation! Consecutive strike succeed!\n')
            pct = len(strike_success_list) / habit_strike_day * 100
            AnalysisMsgS(f'You completion percentage is: {pct:.2f}%')
            completion_performance = CompletionPerformance(pct, len(strike_success_list) + len(strike_fail_list))

            strike_success_list, strike_fail_list, strike_count_list = [], [], []

        elif habit_frequency == "weekly":
            # SUM QTY INFO BY WEEK
            weekly_temp = task_detail_db.SumQuantity(show_all_habits)  # show_all_habits
            # print(weekly_temp)  # [(12.0,), (10.0,), (13.0,), (11.0,)]
            weekly_act_qtys = [x[0] for x in weekly_temp]
            # print(weekly_act_qtys)  # [12.0, 10.0, 13.0, 11.0]

            # ANALYSIS SESSION
            week_num = 1
            strike_success_list, strike_fail_list, strike_count_list = [], [], []
            for weekly_act_qty in weekly_act_qtys:
                if habit_operator == "at least":
                    strike_result = weekly_act_qty >= habit_target_qty
                elif habit_operator == "less than":
                    strike_result = weekly_act_qty <= habit_target_qty
                strike_count_list.append(strike_result)
                if strike_result == True:
                    AnalysisMsgS(f'Week {week_num} record: {weekly_act_qty} {habit_unit} meets the target!')
                    strike_success_list.append(1)
                elif strike_result == False:
                    AnalysisMsgF(f'Week {week_num} record: {weekly_act_qty} {habit_unit} fails to meet the target.')
                    strike_fail_list.append(1)
                week_num += 1

            InfoMsg('####################')
            longest_strike = LongestStrike(strike_count_list)
            AnalysisMsgS(f'Your longest strike for this habit is: {longest_strike}!')

            try:
                AnalysisMsgS(f'Strike completion: {len(strike_success_list)}/{len(weekly_act_qtys)}')
            except ZeroDivisionError:
                AnalysisMsgS('Strike completion: 0')
            if len(strike_fail_list) > 0 or len(weekly_act_qtys) == 0:
                AnalysisMsgF('Sorry, consecutive strike fail!\n')
            else:
                AnalysisMsgS('Congratulation! Consecutive strike succeed!\n')
            try:
                pct = len(strike_success_list) / len(weekly_act_qtys) * 100
            except ZeroDivisionError:
                pct = 0
            AnalysisMsgS(f'You completion percentage is: {pct:.2f}%')
            completion_performance = CompletionPerformance(pct, len(strike_success_list) + len(strike_fail_list))

            week_num = 1
            strike_success_list, strike_fail_list, strike_count_list = [], [], []

    # CREATE/ADD A NEW HABIT
    elif input_atk == "C":
        add_habit_name = AddHabitName()
        add_description = AddDescription()
        add_operator = AddOperator()
        add_target_quantity = AddEditTargetQuantity()
        add_unit = AddUnit()
        add_frequency = AddFrequency()
        add_days_to_success = AddDaysToSuccess()

        new_habit = HabitCreate(add_habit_name, add_description, add_operator, add_target_quantity, add_unit, add_frequency, add_days_to_success, vl[0][0])
        insert_habit = habit_db.InsertHabit(new_habit)
        print("")

        show_all_habits_only = ShowAllHabitOnly()

    # ADD A RECORD FOR A HABIT
    elif input_atk == "D":
        show_all_habits = ShowAllHabits()
        # SELECT TO DISPLAY INDIVIDUAL HABIT
        habit_infos = habit_db.SearchHabit(show_all_habits)
        InfoMsg('## Habit Selection ##')
        InfoMsg(f'{habit_infos[0][0]} for {habit_infos[0][1]} {habit_infos[0][2]} {habit_infos[0][3]} {habit_infos[0][4]} in {habit_infos[0][5]} days\n')

        # GET NEW RECORD INFO
        record_day_n_week = RecordDayAndWeek()
        record_day = record_day_n_week[0]
        record_week = record_day_n_week[1]
        # print(record_day, record_week)
        add_record_quanity = AddEditRecordQuantity()

        # ADD NEW RECORD
        # new_record = RecordCreate('Day 2', 1, 2.0, show_all_habits)  # WEEK IN INT OR STR ALSO OKAY
        new_record = RecordCreate(record_day, record_week, add_record_quanity, show_all_habits)
        insert_task_detail = task_detail_db.InsertTaskDetail(new_record)

    # EDIT A HABIT
    elif input_atk == "E":
        edit_a_habit = EditAHabit()
        # SELECT TO DISPLAY INDIVIDUAL HABIT
        habit_infos = habit_db.SearchHabit(edit_a_habit)
        InfoMsg(f'{habit_infos[0][0]} for {habit_infos[0][1]} {habit_infos[0][2]} {habit_infos[0][3]} {habit_infos[0][4]} in {habit_infos[0][5]} days\n')

        # EDIT INFO
        edit_target_quantity = AddEditTargetQuantity()

        # update_habit = habit_db.UpdateHabit(show_all_habits, 'Build up the art sense', 'at least', '11', 'hours', 'weekly', 28)
        update_habit = habit_db.UpdateHabit(edit_a_habit, habit_infos[0][1], edit_target_quantity, habit_infos[0][3], habit_infos[0][4], habit_infos[0][5])
        InfoMsg(f'UPDATED: {habit_infos[0][0]} for {habit_infos[0][1]} {habit_infos[0][2]} {habit_infos[0][3]} {habit_infos[0][4]} in {habit_infos[0][5]} days\n')

    # EDIT RECORD FOR A SPECIFIC HABIT
    elif input_atk == "F":
        global edit_days_list
        edit_a_habit = EditAHabit()
        # SELECT TO DISPLAY INDIVIDUAL HABIT
        habit_infos = habit_db.SearchHabit(edit_a_habit)
        InfoMsg(f'{habit_infos[0][0]} for {habit_infos[0][1]} {habit_infos[0][2]} {habit_infos[0][3]} {habit_infos[0][4]} in {habit_infos[0][5]} days\n')

        task_details = task_detail_db.SearchTaskDetail(edit_a_habit)
        # print(task_details)
        edit_days_list = []
        for task_detail in task_details:
            days_info = task_detail[1]
            days_num = int(days_info.split(" ")[1])
            edit_days_list.append(days_num)
            weeks_info = task_detail[2]
            actual_qty_info = task_detail[3]
            habit_id_info = task_detail[4]
            InfoMsg(f'{days_info} (Week {weeks_info}) the inputted quantity is {actual_qty_info} {habit_infos[0][3]}')

        # EDIT INFO BY RETRIEVING THE UNIQUE TASK_ID
        edit_record_day = EditRecordDay()
        edit_day = edit_record_day[0]
        edit_week = edit_record_day[1]
        edit_record_quantity = AddEditRecordQuantity()
        # print(edit_day, edit_week, edit_record_quantity, habit_id_info)

        task_id_info = task_detail_db.SearchTaskID(edit_day, habit_id_info)
        # print(task_id_info[0][0], type(task_id_info[0][0]))
        insert_task_detail = task_detail_db.UpdateTaskDetail(task_id_info[0][0], edit_day, edit_week, edit_record_quantity)
        edit_days_list = []

    # DELETE A HABIT
    elif input_atk == "G":
        delete_a_habit = DeleteAHabit()
        # print(delete_a_habit, type(delete_a_habit))
        remove_a_habit = habit_db.RemoveHabit(delete_a_habit)
        # REMOVE IND TASK RECORD DUE TO CASCADE NOT WORK
        remove_task_details = task_detail_db.RemoveTaskDetailTwo(delete_a_habit)

    # DELETE RECORD FOR A SPECIFIC HABIT
    elif input_atk == "H":
        global delete_days_list
        delete_a_habit = DeleteAHabit()
        # SELECT TO DISPLAY INDIVIDUAL HABIT
        habit_infos = habit_db.SearchHabit(delete_a_habit)
        InfoMsg(f'{habit_infos[0][0]} for {habit_infos[0][1]} {habit_infos[0][2]} {habit_infos[0][3]} {habit_infos[0][4]} in {habit_infos[0][5]} days\n')

        task_details = task_detail_db.SearchTaskDetail(delete_a_habit)
        # print(task_details)
        delete_days_list = []
        for task_detail in task_details:
            days_info = task_detail[1]
            days_num = int(days_info.split(" ")[1])
            delete_days_list.append(days_num)
            weeks_info = task_detail[2]
            actual_qty_info = task_detail[3]
            habit_id_info = task_detail[4]
            InfoMsg(f'{days_info} (Week {weeks_info}) the inputted quantity is {actual_qty_info} {habit_infos[0][3]}')

        # DELETE A SPECIFIC ROW OF RECORD
        delete_record_day = DeleteRecordDay()
        # print(delete_record_day)

        task_id_info = task_detail_db.SearchTaskID(delete_record_day, habit_id_info)
        # print(task_id_info)
        remove_task_detail = task_detail_db.RemoveTaskDetail(task_id_info[0][0])
        delete_days_list = []

    # EXIT THE APP
    elif input_atk == "I":
        InfoMsg('See you next time!')
        sys.exit(0)
    else:
        ErrorMsg('Wrong input. Please try again. (ATT)')
        return ActionToTake()
    return input_atk


# ------------------------------
# 6A, 6C) SHOW HABITS
def ShowAllHabitOnly():
    all_habits = habit_db.AllHabit(vl[0][0])
    InfoMsg('Below are all the available habits: ')
    for all_habit in all_habits:
        InfoMsg(f'{all_habit}')
    print('')


# 6B, 6D) SHOW HABIT & ANALYSIS
def ShowAllHabits():
    all_habits = habit_db.AllHabit(vl[0][0])
    InfoMsg('Below are all the available habits: ')
    habit_num_list = []
    for all_habit in all_habits:
        InfoMsg(f'{all_habit}')
        habit_num_list.append(all_habit[0])
    print('')

    input_habit = input(EnquiryMsg('Please select a habit by number to view the detail: '))
    # FILTER OUT NON INTEGER INPUT
    try:
        input_habit = int(input_habit)
    except ValueError:
        ErrorMsg('Wrong input. Please try again. (SAH)')
        return ShowAllHabits()
    # FILTER OUT INPUT NOT IN THE TABLE
    if input_habit not in habit_num_list:
        ErrorMsg('Wrong input. Please try again. (SAH2)')
        return ShowAllHabits()
    else:
        return input_habit
    habit_num_list = []


# 6C) ADD NEW HABIT NAME
def AddHabitName():
    global input_hn, word
    input_hn = input(EnquiryMsg('Please name your habit: ')).title()
    # print(input_hn)

    # BLOCK DUPLICATE INPUT
    duplicated_habit = habit_db.DuplicateHabitCheck(input_hn)
    # print(duplicated_habit)
    if len(duplicated_habit) > 0:
        ErrorMsg('Duplicated Input, please try again. (AHN)')
        return AddHabitName()
    return input_hn


# 6C) ADD NEW  DESCRIPTION (THIS PART SHOWS THAT THE INPUT CAN BE OPTIONAL)
def AddDescription():
    input_de = input(EnquiryMsg('Please describe your habit within 50 characters. Or you can skip this by press "Enter": '))
    if len(input_de) > 50:
        ErrorMsg('Description has to be within 50 characters. Please try again.')
        return AddDescription()
    return input_de


# 6C) ADD NEW OPERATOR
def AddOperator():
    input_op = input(EnquiryMsg('Please input "A" for "at least" or "B" for "less than": ')).upper()
    if input_op == "A":
        input_op = "at least"
    elif input_op == "B":
        input_op = "less than"
    else:
        ErrorMsg('Wrong input. Please try again. (AO)')
        return AddOperator()
    return input_op


# 6C, 6E) ADD NEW TARGET QUANTITY
def AddEditTargetQuantity():
    input_tq = input(EnquiryMsg('How many in number you want to achieve?: '))
    try:
        float(input_tq)
        return input_tq
    except ValueError:
        ErrorMsg('Wrong input. Please try again. (AETQ)')
        return AddEditTargetQuantity()


# 6C) ADD NEW UNIT
def AddUnit():
    input_un = input(EnquiryMsg('Please input a suitable unit to describe the target quantity set. e.g. songs, hours, times, miles: '))
    return input_un


# 6C) ADD NEW FREQUENCY
def AddFrequency():
    input_fr = input(EnquiryMsg('Please input "A" for "daily" or "B" for "weekly": ')).upper()
    if input_fr == "A":
        input_fr = "daily"
    elif input_fr == "B":
        input_fr = "weekly"
    else:
        ErrorMsg('Wrong input. Please try again. (AF)')
        return AddFrequency()
    return input_fr


# 6C) ADD NEW DAYS TO SUCCESS
def AddDaysToSuccess():
    input_dts = input(EnquiryMsg('How many in number you want to achieve?: '))
    if input_dts == '0' or input_dts == 0:
        ErrorMsg('Cannot be 0. Please try again. (ADTS)')
        return AddDaysToSuccess()
    try:
        int(input_dts)
        return input_dts
    except ValueError:
        ErrorMsg('Wrong input. Please try again. (ADTS2)')
        return AddDaysToSuccess()


# 6D) RECORD INFO
def RecordDayAndWeek():
    input_day = input(EnquiryMsg('Please input the day info: '))
    try:
        input_day = int(input_day)
    except ValueError:
        ErrorMsg('Wrong input. Please try again. (RDAW)')
        return RecordDayAndWeek()

    date_info = f'Day {input_day}'
    week_info = math.ceil(int(input_day)/7)
    return date_info, week_info


# 6D, 6F) RECORD QUANTITY
def AddEditRecordQuantity():
    input_rq = input(EnquiryMsg('Please input your achieved quantity: '))
    try:
        float(input_rq)
        return input_rq
    except ValueError:
        ErrorMsg('Wrong input. Please try again. (AERQ)')
        return AddEditRecordQuantity()


# 6E, 6F) EDIT A HABIT
def EditAHabit():
    all_habits = habit_db.AllHabit(vl[0][0])
    InfoMsg('Below are all the available habits: ')
    habit_num_list = []
    for all_habit in all_habits:
        InfoMsg(f'{all_habit}')
        habit_num_list.append(all_habit[0])

    edit_habit = input(EnquiryMsg('Please select a habit by number to edit: '))
    # FILTER OUT NON INTEGER INPUT
    try:
        edit_habit = int(edit_habit)
    except ValueError:
        ErrorMsg('Wrong input. Please try again. (EAH)')
        return EditAHabit()
    # FILTER OUT INPUT NOT IN THE TABLE
    if edit_habit not in habit_num_list:
        ErrorMsg('Wrong input. Please try again. (EAH2)')
        return EditAHabit()
    else:
        return edit_habit
    habit_num_list = []


# 6F) EDIT RECORD DAY SELECTION
def EditRecordDay():
    edit_day = input(EnquiryMsg('Which day you want to edit?: '))
    try:
        edit_day = int(edit_day)
    except ValueError:
        ErrorMsg('Wrong input. Please try again. (ERD)')
        return EditRecordDay()
    # FILTER OUT INPUT NOT IN THE TABLE
    if edit_day not in edit_days_list:
        ErrorMsg('No such day info. Please try again. (ERD2)')
        return EditRecordDay()

    date_info = f'Day {edit_day}'
    week_info = math.ceil(int(edit_day)/7)
    return date_info, week_info


# 6G, 6H) DELETE A HABIT
def DeleteAHabit():
    all_habits = habit_db.AllHabit(vl[0][0])
    InfoMsg('Below are all the available habits: ')
    habit_num_list = []
    for all_habit in all_habits:
        InfoMsg(f'{all_habit}')
        habit_num_list.append(all_habit[0])
    print("")

    delete_habit = input(EnquiryMsg('Please select a habit by number to delete: '))
    # FILTER OUT NON INTEGER INPUT
    try:
        delete_habit = int(delete_habit)
    except ValueError:
        ErrorMsg('Wrong input. Please try again. (DAH)')
        return DeleteAHabit()
    # FILTER OUT INPUT NOT IN THE TABLE
    if delete_habit not in habit_num_list:
        ErrorMsg('Wrong input. Please try again. (DAH2)')
        return DeleteAHabit()
    else:
        return delete_habit
    habit_num_list = []


# 6H) DELETE RECORD DAY SELECTION
def DeleteRecordDay():
    delete_day = input(EnquiryMsg('Which day you want to delete?: '))
    try:
        delete_day = int(delete_day)
    except ValueError:
        ErrorMsg('Wrong input. Please try again. (DRD)')
        return DeleteRecordDay()
    # FILTER OUT INPUT NOT IN THE TABLE
    if delete_day not in delete_days_list:
        ErrorMsg('No such day info. Please try again. (DRD2)')
        return DeleteRecordDay()

    date_info = f'Day {delete_day}'
    return date_info


# PART 7) ABOUT ANALYSIS
# ------------------------------
# COMMENTS VIA COMPLETION %
def CompletionPerformance(pct, succeed_rate):
    if succeed_rate == 0:
        AnalysisMsgF('Your problem might be forgetful! Key in some records for your habit.\n')
    elif pct == 0 and not succeed_rate == 0:
        AnalysisMsgF('If your have already tried your best. Maybe you should reset your habit target.\n')
    elif pct <= 20:
        AnalysisMsgF('Your performance is way behind. But no worry, things would get better, keep going!\n')
    elif 20 < pct <= 40:
        AnalysisMsgF('Be more aggressive to achieve your habit target or lower your target setting.\n')
    elif 40 < pct <= 60:
        AnalysisMsgS('I am sure you could do better!\n')
    elif 60 < pct <= 80:
        AnalysisMsgS('You are doing better and better!\n')
    elif 80 < pct < 100:
        AnalysisMsgS('You are about to be perfect\n')
    elif pct == 100:
        AnalysisMsgS('You are a (wo)man of word!\n')


# LONGEST STRIKE COUNT
def LongestStrike(strike_list):
    success_count_list, fail_count_list = [], []
    succeed, failed = 0, 0
    # print(len(strike_list), strike_list)

    for i in range(len(strike_list)):
        true_false = strike_list[i]
        if true_false:  # if true_false == True
            succeed += 1
            if failed != 0:
                fail_count_list.append(failed)
                failed = 0
            if i + 1 == len(strike_list):
                success_count_list.append(succeed)
        if not true_false:  # if true_false == False
            failed += 1
            if succeed != 0:
                success_count_list.append(succeed)
                succeed = 0
            if i + 1 == len(strike_list):
                fail_count_list.append(failed)

    # print(max(success_count_list), success_count_list)
    # print(max(fail_count_list), fail_count_list)
    return max(success_count_list)

    success_count_list, fail_count_list = [], []
    succeed, failed = 0, 0


# ------------------------------
if __name__ == "__main__":
    ''' TEMPORARY HIDE BELOW INFO AND DISTRIBUTE IT TO DIFF DEFS DUE TO UNITTEST '''
    # today = date.today()

    # CREATE USER TABLE WITH SOME USERS INFO CREATED
    create_table = user_db.CreateUserTable()

    # CHECK IF ALREADY HAVE CREATED PRESET USERS
    search_first_input = user_db.SearchFirstInput(1)
    # print(len(search_first_input))

    # ADD ONLY ONCE
    if len(search_first_input) == 0:
        user_1 = UserCreate('test1@gmail.com', 'TEST1234', '2022-01-04')
        user_2 = UserCreate('test2@gmail.com', 'TEST2345', '2022-02-05')
        user_3 = UserCreate('test3@gmail.com', 'TEST3456', '2022-03-06')
        user_4 = UserCreate('test4@gmail.com', 'TEST4567', '2022-04-07')
        user_5 = UserCreate('test5@gmail.com', 'TEST5678', '2022-05-08')
        preset_users = [user_1, user_2, user_3, user_4, user_5]
        for preset_user in preset_users:
            insert_user = user_db.InsertUser(preset_user)

        # CREATE HABIT TABLE WITH 5 TASKS CREATED (1 WEEKLY, 1 DAILY) WITH 4 WEEKS DATA
        create_table = habit_db.CreateHabitTable()
        create_table2 = task_detail_db.CreateTaskDetailTable()

        for i in range(5):
            # HabitCreate(taskname, description, event, operator, target_quantity, unit, frequency, days_to_Success, login_id)
            habit_1 = HabitCreate('Listen To Music', 'Enjoy relax time', 'at least', 10, 'songs', 'daily', 30, i + 1)
            habit_2 = HabitCreate('Play An Instrument', 'Build up the art sense', 'at least', 12, 'hours', 'weekly', 28, i + 1)
            habit_3 = HabitCreate('Sleep', 'Recover the energy', 'at least', 6.5, 'hours', 'daily', 40, i + 1)
            habit_4 = HabitCreate('Run', 'Build up strength', 'at least', 3, 'times', 'weekly', 28, i + 1)
            habit_5 = HabitCreate('Swim', 'Build up strength', 'at least', 0.75, 'hours', 'weekly', 35, i + 1)
            preset_habits_list = [habit_1, habit_2, habit_3, habit_4, habit_5]
            for preset_habit in preset_habits_list:
                insert_habit = habit_db.InsertHabit(preset_habit)

                # EXTRACT DAYS OF SUCCESS INFO FROM HABIT DB AND CREATE ROWS IN TASK DETAIL DB
                auto_create = task_detail_db.AutoCreateTaskDetail()

    login_option = LoginOption()


