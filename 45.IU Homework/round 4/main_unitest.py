import unittest
from unittest import mock
from unittest.mock import MagicMock
from mock import patch
from freezegun import freeze_time
import main, user_db, habit_db, task_detail_db
import math, random
from colorama import Fore, Back, Style
from datetime import date, datetime
import re, os, sys
import sqlite3

''' https://stackoverflow.com/questions/29987488/how-to-reuse-tests-written-using-unittest-testcase '''
''' https://stackoverflow.com/questions/28473781/test-whether-a-function-is-called-inside-another-function-in-unit-testing '''
''' https://a-n-rose.github.io/2018/11/07/unittest-sqlite3-classes/ '''

# MAIN INTERFACE
class TestMainApplication(unittest.TestCase):
    def setUp(self):
        self.msg = "Hello World"
        self.select_l = 'L'
        self.select_r = 'R'
        self.select_others = 'X'
        self.valid_email = "test1@gmail.com"
        self.valid_password = "TEST1234"
        self.invalid_email1 = 'test1gmail.com'
        self.invalid_email2 = 'test1@gmail'
        self.invalid_password1 = 'shortpw'
        self.invalid_password2 = 'white space'
        self.invalid_password3 = 'nouppercase'
        self.invalid_password4 = 'noInteger'
        self.today = '2022-07-09'
        self.record_day1 = '2022-07-05'
        self.record_day2 = '2022-06-15'
        self.qty_selection0 = '0'
        self.qty_selection2 = '2'
        self.qty_selection13 = '13'
        self.habit_name = 'drink coffee'
        self.habit_description = 'to wake myself'
        self.habit_description_long = 'to wake myself in the morning so that I can feel refresh and energetic'
        self.select_a = 'A'
        self.select_b = 'B'
        self.select_c = 'C'
        self.select_d = 'D'
        self.select_e = 'E'
        self.select_f = 'F'
        self.select_g = 'G'
        self.select_h = 'H'
        self.select_i = 'I'
        self.habit_unit = 'times'

    def tearDown(self):
        pass

    # ------------------------------
    # PART 1
    # -- PRINT -- #
    @patch('builtins.print')
    def test_error_msg(self, mock_print):
        main.errorMsg(f'{self.msg}')
        mock_print.assert_called_with(f'{Fore.RED}{self.msg}\n{Style.RESET_ALL}')

    @patch('builtins.print')
    def test_info_msg(self, mock_print):
        main.infoMsg(f'{self.msg}')
        mock_print.assert_called_with(f'{Fore.BLUE}{self.msg}{Style.RESET_ALL}')

    # -- RETURN  -- #
    def test_enquiry_msg(self):
        self.assertEqual(main.enquiryMsg(f'{self.msg}'), f'{Fore.CYAN}{self.msg}{Style.RESET_ALL}')

    @patch('builtins.print')
    def test_analysis_msg_s(self, mock_print):
        main.analysisMsgS(f'{self.msg}')
        mock_print.assert_called_with(f'{Fore.GREEN}{self.msg}{Style.RESET_ALL}')

    @patch('builtins.print')
    def test_analysis_msg_f(self, mock_print):
        main.analysisMsgF(f'{self.msg}')
        mock_print.assert_called_with(f'{Fore.LIGHTRED_EX}{self.msg}{Style.RESET_ALL}')

    # ------------------------------
    # PART 2
    @patch('main.LoginOption', return_value='R')
    def test_login_option_r(self, input):
        self.assertEqual(main.loginOption(), self.select_r)
        if self.select_r == 'R':
            main.infoMsg("Register panel starts.")
        elif self.select_r == 'L':
            main.infoMsg("Login panel starts.")
        else:
            main.errorMsg('Invalid selection. Please try again!')
            return self.test_login_option_r

    @patch('main.LoginOption', return_value='L')
    def test_login_option_l(self, input):
        self.assertEqual(main.loginOption(), self.select_l)
        if self.select_l == 'R':
            main.infoMsg("Register panel starts.")
        elif self.select_l == 'L':
            main.infoMsg("Login panel starts.")
        else:
            main.errorMsg('Invalid selection. Please try again!')
            return self.test_login_option_l

    @patch('main.LoginOption', return_value='X')
    def test_login_option_x(self, input):
        self.assertEqual(main.loginOption(), self.select_others)
        if self.select_others == 'R':
            main.infoMsg("Register panel starts.")
        elif self.select_others == 'L':
            main.infoMsg("Login panel starts.")
        else:
            main.errorMsg('Invalid selection. Please try again!')
            return self.test_login_option_x

    # PART 3
    # ------------------------------
    # # FOR USER REGISTRATION # #
    # -- INPUT WITH RETURN -- #
    @patch('main.EmailRegister', return_value='test1@gmail.com')
    def test_email_register_ok(self, input):
        self.assertEqual(main.emailRegister(), self.valid_email)

    @patch('main.PasswordRegister', return_value='TEST1234')
    def test_password_register(self, input):
        self.assertEqual(main.passwordRegister(), self.valid_password)

    @patch('main.EmailRegister', return_value='test1gmail.com')
    def test_verify_email_notok1(self, input):
        self.assertEqual(main.emailRegister(), self.invalid_email1)
        if '@' not in self.invalid_email1 or not self.invalid_email1.endswith('.com'):
            main.errorMsg(f'"{self.invalid_email1}" is an invalid email account. Please try again.')
            return self.test_verify_email_notok1
        return self.invalid_email1

    @patch('main.EmailRegister', return_value='test1@gmail')
    def test_verify_email_notok2(self, input):
        self.assertEqual(main.emailRegister(), self.invalid_email2)
        if '@' not in self.invalid_email2 or not self.invalid_email2.endswith('.com'):
            main.errorMsg(f'"{self.invalid_email2}" is an invalid email account. Please try again.')
            return self.test_verify_email_notok2
        return self.invalid_email2

    @patch('main.EmailRegister', return_value='test1@gmail.com')
    def test_verify_email_ok(self, input):
        self.assertEqual(main.emailRegister(), self.valid_email)
        if '@' not in self.valid_email or not self.valid_email.endswith('.com'):
            main.errorMsg(f'"{self.invalid_email1}" is an invalid email account. Please try again.')
            return self.test_verify_email_ok
        return self.valid_email

    @patch('main.PasswordRegister', return_value='shortpw')
    def test_verify_password_notok1(self, input):
        self.assertEqual(main.passwordRegister(), self.invalid_password1)
        if len(self.invalid_password1) < 8 or 20 < len(self.invalid_password1):
            main.errorMsg('Password needs to be within 8 to 20 characters. Please try again.')
            return self.test_verify_password_notok1
        if " " in self.invalid_password1:
            main.errorMsg('Password is not in 1 word. Please try again.')
            return self.test_verify_password_notok1
        is_uppercase = re.search(r'[A-Z]', self.invalid_password1)
        if not is_uppercase:
            main.errorMsg('Password needs at least 1 uppercase letter. Please try again.')
            return self.test_verify_password_notok1
        is_integer = re.search(r'[0-9]', self.invalid_password1)
        if not is_integer:
            main.errorMsg('Password needs at least 1 integer. Please try again.')
            return self.test_verify_password_notok1

    @patch('main.PasswordRegister', return_value='white space')
    def test_verify_password_notok2(self, input):
        self.assertEqual(main.passwordRegister(), self.invalid_password2)
        if len(self.invalid_password2) < 8 or 20 < len(self.invalid_password2):
            main.errorMsg('Password needs to be within 8 to 20 characters. Please try again.')
            return self.test_verify_password_notok2
        if " " in self.invalid_password2:
            main.errorMsg('Password is not in 1 word. Please try again.')
            return self.test_verify_password_notok2
        is_uppercase = re.search(r'[A-Z]', self.invalid_password2)
        if not is_uppercase:
            main.errorMsg('Password needs at least 1 uppercase letter. Please try again.')
            return self.test_verify_password_notok2
        is_integer = re.search(r'[0-9]', self.invalid_password2)
        if not is_integer:
            main.errorMsg('Password needs at least 1 integer. Please try again.')
            return self.test_verify_password_notok2

    @patch('main.PasswordRegister', return_value='nouppercase')
    def test_verify_password_notok3(self, input):
        self.assertEqual(main.passwordRegister(), self.invalid_password3)
        if len(self.invalid_password3) < 8 or 20 < len(self.invalid_password3):
            main.errorMsg('Password needs to be within 8 to 20 characters. Please try again.')
            return self.test_verify_password_notok3
        if " " in self.invalid_password3:
            main.errorMsg('Password is not in 1 word. Please try again.')
            return self.test_verify_password_notok3
        is_uppercase = re.search(r'[A-Z]', self.invalid_password3)
        if not is_uppercase:
            main.errorMsg('Password needs at least 1 uppercase letter. Please try again.')
            return self.test_verify_password_notok3
        is_integer = re.search(r'[0-9]', self.invalid_password3)
        if not is_integer:
            main.errorMsg('Password needs at least 1 integer. Please try again.')
            return self.test_verify_password_notok3

    @patch('main.PasswordRegister', return_value='noInteger')
    def test_verify_password_notok4(self, input):
        self.assertEqual(main.passwordRegister(), self.invalid_password4)
        if len(self.invalid_password4) < 8 or 20 < len(self.invalid_password4):
            main.errorMsg('Password needs to be within 8 to 20 characters. Please try again.')
            return self.test_verify_password_notok4
        if " " in self.invalid_password4:
            main.errorMsg('Password is not in 1 word. Please try again.')
            return self.test_verify_password_notok4
        is_uppercase = re.search(r'[A-Z]', self.invalid_password4)
        if not is_uppercase:
            main.errorMsg('Password needs at least 1 uppercase letter. Please try again.')
            return self.test_verify_password_notok4
        is_integer = re.search(r'[0-9]', self.invalid_password4)
        if not is_integer:
            main.errorMsg('Password needs at least 1 integer. Please try again.')
            return self.test_verify_password_notok4

    @patch('main.PasswordRegister', return_value='TEST1234')
    def test_verify_password_ok(self, input):
        self.assertEqual(main.passwordRegister(), self.valid_password)
        if len(self.valid_password) < 8 or 20 < len(self.valid_password):
            main.errorMsg('Password needs to be within 8 to 20 characters. Please try again.')
            return self.test_verify_password_ok
        if " " in self.valid_password:
            main.errorMsg('Password is not in 1 word. Please try again.')
            return self.test_verify_password_ok
        is_uppercase = re.search(r'[A-Z]', self.valid_password)
        if not is_uppercase:
            main.errorMsg('Password needs at least 1 uppercase letter. Please try again.')
            return self.test_verify_password_ok
        is_integer = re.search(r'[0-9]', self.valid_password)
        if not is_integer:
            main.errorMsg('Password needs at least 1 integer. Please try again.')
            return self.test_verify_password_ok

    @patch('main.VerifyDuplicate', return_value='test1@gmail.com')
    def test_verify_duplicate_notok(self, input):
        self.assertEqual(main.verifyDuplicate(), self.valid_email)
        duplicated_list = []
        if self.valid_email not in duplicated_list:
            duplicated_list.append(self.valid_email)
        else:
            duplicated_list.remove(self.valid_email)
        if len(duplicated_list) == 1:
            main.errorMsg(f'"{self.valid_email}" has already been registered. Please try a new one.')

    @patch('main.VerifyDuplicate', return_value='test1@gmail.com')
    def test_verify_duplicate_ok(self, input):
        self.assertEqual(main.verifyDuplicate(), self.valid_email)
        duplicated_list = ['test1@gmail.com']
        if self.valid_email not in duplicated_list:
            duplicated_list.append(self.valid_email)
        else:
            duplicated_list.remove(self.valid_email)
        if len(duplicated_list) == 1:
            main.errorMsg(f'"{self.valid_email}" has already been registered. Please try a new one.')

    # ------------------------------
    # # FOR USER LOGIN # #
    @patch('main.EmailLogin', return_value='test1@gmail.com')
    def test_email_login(self, input):
        self.assertEqual(main.emailLogin(), self.valid_email)

    @patch('main.PasswordLogin', return_value='TEST1234')
    def test_password_login(self, input):
        self.assertEqual(main.passwordLogin(), self.valid_password)

    def test_verify_login_email_nouser(self):
        users = []
        if len(users) == 0:
            main.errorMsg('Login not found, please try again!')
            return self.test_verify_login_email_nouser
        if self.test_password_login == users[0][2]:
            main.infoMsg('Login Successful!\n')
        else:
            main.errorMsg('Password incorrect, please try again!')
        return users

    def test_verify_login_email_ok(self):
        users = [(1, self.test_email_login, self.test_password_login, '2022-07-10')]
        if len(users) == 0:
            main.errorMsg('Login not found, please try again!')
            return self.test_verify_login_email_ok
        if self.test_password_login == users[0][2]:
            main.infoMsg('Login Successful!\n')
        else:
            main.errorMsg('Password incorrect, please try again!')
        return users

    def test_verify_login_email_notok(self):
        users = [(1, self.test_email_login, 'TEST12345', '2022-07-10')]
        if len(users) == 0:
            main.errorMsg('Login not found, please try again!')
            return self.test_verify_login_email_notok
        if self.test_password_login == users[0][2]:
            main.infoMsg('Login Successful!\n')
        else:
            main.errorMsg('Password incorrect, please try again!')
        return users

    # ------------------------------
    # # FOR LOGIN DATE # #
    @freeze_time("2022-07-09")
    def test_today_conversion(self):
        self.assertEqual(main.todayConversion(self.today), date.today().strftime('%Y-%m-%d'))


    @freeze_time("2022-07-09")
    def test_date_diff1(self):
        today = date.today()
        record_date = datetime.strptime(self.record_day1, '%Y-%m-%d').date()

        if today == record_date:
            date_diff = 0
        else:
            date_diff = int(str(today - record_date).split(" ")[0])
        if date_diff != 0:
            main.infoMsg(f'It has been {date_diff} days since your last login.')
        if date_diff > 7:
            main.infoMsg(f'It is important for you to login regularly to build up good habit!')
        print('')

    @freeze_time("2022-07-09")
    def test_date_diff2(self):
        today = date.today()
        record_date = datetime.strptime(self.record_day2, '%Y-%m-%d').date()

        if today == record_date:
            date_diff = 0
        else:
            date_diff = int(str(today - record_date).split(" ")[0])
        if date_diff != 0:
            main.infoMsg(f'It has been {date_diff} days since your last login.')
        if date_diff > 7:
            main.infoMsg(f'It is important for you to login regularly to build up good habit!')
        print('')

    @freeze_time("2022-07-09")
    def test_date_diff3(self):
        today = date.today()
        record_date = datetime.strptime(self.today, '%Y-%m-%d').date()

        if today == record_date:
            date_diff = 0
        else:
            date_diff = int(str(today - record_date).split(" ")[0])
        if date_diff != 0:
            main.infoMsg(f'It has been {date_diff} days since your last login.')
        if date_diff > 7:
            main.infoMsg(f'It is important for you to login regularly to build up good habit!')
        print('')

    # PART 6
    # ------------------------------
    @patch('main.ActionToTake', return_value='A')
    def test_action_to_take_a(self, input):
        self.assertEqual(main.actionToTake(), self.select_a)
        if self.select_a == "A":
            self.test_show_all_habit_only

    @patch('main.ActionToTake', return_value='B')
    def test_action_to_take_b_daily(self, input):
        self.assertEqual(main.actionToTake(), self.select_b)
        if self.select_b == "B":
            self.test_show_all_habits_print
            habit_infos = [('Listen To Music', 'at least', 10.0, 'songs', 'daily', 5), ('Play An Instrument', 'at least', 12.0, 'hours', 'weekly', 7)]
            habit_name = habit_infos[0][0]
            habit_operator = habit_infos[0][1]
            habit_target_qty = habit_infos[0][2]
            habit_unit = habit_infos[0][3]
            habit_frequency = habit_infos[0][4]
            habit_strike_day = habit_infos[0][5]
            main.infoMsg('## Habit Selection ##')
            main.infoMsg(f'{habit_name} for {habit_operator} {habit_target_qty} {habit_unit} {habit_frequency} in {habit_strike_day} days\n')

            if habit_frequency == 'daily':
                task_details = [(1, 'Day 1', '1', 8.0, 1), (2, 'Day 2', '1', 12.0, 1), (3, 'Day 3', '1', 13.0, 1), (4, 'Day 4', '1', 14.0, 1), (5, 'Day 5', '1', 8.0, 1)]

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
                        main.analysisMsgS(f'{days_info} record: {actual_qty_info} {habit_unit} meets the target!')
                        strike_success_list.append(1)
                    elif strike_result == False:
                        main.analysisMsgF(f'{days_info} record: {actual_qty_info} {habit_unit} fails to meet the target.')
                        strike_fail_list.append(1)

                main.infoMsg('####################')
                longest_strike = main.longestStrike(strike_count_list)
                main.analysisMsgS(f'Your longest strike for this habit is: {longest_strike}!')

                main.analysisMsgS(f'Strike completion: {len(strike_success_list)}/{habit_strike_day}')
                if len(strike_fail_list) > 0:
                    main.analysisMsgF('Sorry, consecutive strike fail!\n')
                elif len(task_details) == 0:
                    pass
                elif len(strike_success_list) == habit_strike_day:
                    main.analysisMsgS('Congratulation! Consecutive strike succeed!\n')
                pct = len(strike_success_list) / habit_strike_day * 100
                main.analysisMsgS(f'You completion percentage is: {pct:.2f}%')
                records_inputted = 5
                if records_inputted == habit_strike_day:
                    completion_performance = main.completionPerformance(pct, len(strike_success_list) + len(strike_fail_list))

                print("")
                strike_success_list, strike_fail_list, strike_count_list = [], [], []

    @patch('main.ActionToTake', return_value='B')
    def test_action_to_take_b_weekly(self, input):
        self.assertEqual(main.actionToTake(), self.select_b)
        if self.select_b == "B":
            self.test_show_all_habits_print
            habit_infos = [('Play An Instrument', 'at least', 12.0, 'hours', 'weekly', 7), ('Listen To Music', 'at least', 10.0, 'songs', 'daily', 5)]
            habit_name = habit_infos[0][0]
            habit_operator = habit_infos[0][1]
            habit_target_qty = habit_infos[0][2]
            habit_unit = habit_infos[0][3]
            habit_frequency = habit_infos[0][4]
            habit_strike_day = habit_infos[0][5]
            main.infoMsg('## Habit Selection ##')
            main.infoMsg(f'{habit_name} for {habit_operator} {habit_target_qty} {habit_unit} {habit_frequency} in {habit_strike_day} days\n')

            if habit_frequency == 'weekly':
                weekly_temp = [(7.0,), (20.0,), (17.0,), (11.0,)]
                weekly_act_qtys = [x[0] for x in weekly_temp]
                # print(weekly_act_qtys)  # [7.0, 20.0, 17.0, 11.0]

                week_num = 1
                strike_success_list, strike_fail_list, strike_count_list = [], [], []
                for weekly_act_qty in weekly_act_qtys:
                    if habit_operator == "at least":
                        strike_result = weekly_act_qty >= habit_target_qty
                    elif habit_operator == "less than":
                        strike_result = weekly_act_qty <= habit_target_qty
                    strike_count_list.append(strike_result)
                    if strike_result == True:
                        main.analysisMsgS(f'Week {week_num} record: {weekly_act_qty} {habit_unit} meets the target!')
                        strike_success_list.append(1)
                    elif strike_result == False:
                        main.analysisMsgF(f'Week {week_num} record: {weekly_act_qty} {habit_unit} fails to meet the target.')
                        strike_fail_list.append(1)
                    week_num += 1

                main.infoMsg('####################')
                longest_strike = main.longestStrike(strike_count_list)
                main.analysisMsgS(f'Your longest strike for this habit is: {longest_strike}!')

                try:
                    main.analysisMsgS(f'Strike completion: {len(strike_success_list)}/{len(weekly_act_qtys)}')
                except ZeroDivisionError:
                    main.analysisMsgS('Strike completion: 0')
                if len(strike_fail_list) > 0:
                    main.analysisMsgF('Sorry, consecutive strike fail!\n')
                elif len(weekly_act_qtys) == 0:
                    pass
                elif len(strike_success_list) == len(weekly_act_qtys):
                    main.analysisMsgS('Congratulation! Consecutive strike succeed!\n')
                try:
                    pct = len(strike_success_list) / len(weekly_act_qtys) * 100
                except ZeroDivisionError:
                    pct = 0
                main.analysisMsgS(f'You completion percentage is: {pct:.2f}%')
                records_inputted = 46
                if math.ceil(records_inputted / 7) == len(weekly_act_qtys):
                    completion_performance = main.completionPerformance(pct, len(strike_success_list) + len(strike_fail_list))

                week_num = 1
                print("")
                strike_success_list, strike_fail_list, strike_count_list = [], [], []

    @patch('main.ActionToTake', return_value='C')
    def test_action_to_take_c(self, input):
        self.assertEqual(main.actionToTake(), self.select_c)
        if self.select_a == "C":
            self.test_add_habit_name_input
            self.test_add_description
            self.test_add_operator_a
            self.test_add_edit_target_quantity_float
            self.test_add_unit
            self.test_add_frequency_a
            self.test_add_days_to_success_2

            print("")
            self.test_show_all_habit_only

    @patch('main.ActionToTake', return_value='D')
    def test_action_to_take_d(self, input):
        self.assertEqual(main.actionToTake(), self.select_d)
        if self.select_a == "D":
            habit_infos = [('Play An Instrument', 'at least', 12.0, 'hours', 'weekly', 7), ('Listen To Music', 'at least', 10.0, 'songs', 'daily', 5)]
            record_inputted = 5
            if habit_infos[0][5] <= record_inputted:
                main.errorMsg('This habit has finished all records, please reselect your option.')
                return self.test_action_to_take_d
            else:
                main.infoMsg('## Habit Selection ##')
                main.infoMsg(f'{habit_infos[0][0]} for {habit_infos[0][1]} {habit_infos[0][2]} {habit_infos[0][3]} {habit_infos[0][4]} in {habit_infos[0][5]} days\n')

                # GET NEW RECORD INFO
                self.test_record_day_and_week_2
                record_day_n_week = (2, 1)
                record_day = record_day_n_week[0]
                record_week = record_day_n_week[1]
                self.test_add_edit_record_quantity_2

    @patch('main.ActionToTake', return_value='E')
    def test_action_to_take_e(self, input):
        self.assertEqual(main.actionToTake(), self.select_e)
        if self.select_a == "E":
            habit_infos = [('Play An Instrument', 'at least', 12.0, 'hours', 'weekly', 7), ('Listen To Music', 'at least', 10.0, 'songs', 'daily', 5)]
            main.infoMsg(f'{habit_infos[0][0]} for {habit_infos[0][1]} {habit_infos[0][2]} {habit_infos[0][3]} {habit_infos[0][4]} in {habit_infos[0][5]} days\n')

            self.test_add_edit_target_quantity_float
            edit_target_quantity = 11.0
            main.infoMsg(f'UPDATED: {habit_infos[0][0]} for {habit_infos[0][1]} {edit_target_quantity} {habit_infos[0][3]} {habit_infos[0][4]} in {habit_infos[0][5]} days\n')

    @patch('main.ActionToTake', return_value='F')
    def test_action_to_take_f(self, input):
        self.assertEqual(main.actionToTake(), self.select_f)
        self.test_edit_a_habit_2
        habit_infos = [('Listen To Music', 'at least', 10.0, 'songs', 'daily', 5), ('Play An Instrument', 'at least', 12.0, 'hours', 'weekly', 7)]
        main.infoMsg(f'{habit_infos[0][0]} for {habit_infos[0][1]} {habit_infos[0][2]} {habit_infos[0][3]} {habit_infos[0][4]} in {habit_infos[0][5]} days\n')

        edit_days_list = []
        task_details = [(1, 'Day 1', '1', 0.0, 2), (2, 'Day 2', '1', 0.0, 2), (3, 'Day 3', '1', 2.0, 2), (4, 'Day 4', '1', 2.0, 2), (5, 'Day 5', '1', 1.0, 2)]
        for task_detail in task_details:
            days_info = task_detail[1]
            days_num = int(days_info.split(" ")[1])
            edit_days_list.append(days_num)
            weeks_info = task_detail[2]
            actual_qty_info = task_detail[3]
            habit_id_info = task_detail[4]
            main.infoMsg(f'{days_info} (Week {weeks_info}) the inputted quantity is {actual_qty_info} {habit_infos[0][3]}')

        self.test_edit_record_day_2
        edit_record_day = (2, 1)
        edit_day = edit_record_day[0]
        edit_week = edit_record_day[1]
        self.test_add_edit_record_quantity_2

        edit_days_list = []

    @patch('main.ActionToTake', return_value='G')
    def test_action_to_take_g(self, input):
        self.assertEqual(main.actionToTake(), self.select_g)
        self.test_delete_a_habit_2

    @patch('main.ActionToTake', return_value='H')
    def test_action_to_take_h(self, input):
        self.assertEqual(main.actionToTake(), self.select_h)
        habit_infos = [('Listen To Music', 'at least', 10.0, 'songs', 'daily', 5), ('Play An Instrument', 'at least', 12.0, 'hours', 'weekly', 7)]
        main.infoMsg(f'{habit_infos[0][0]} for {habit_infos[0][1]} {habit_infos[0][2]} {habit_infos[0][3]} {habit_infos[0][4]} in {habit_infos[0][5]} days\n')

        delete_days_list = []
        task_details = [(1, 'Day 1', '1', 0.0, 2), (2, 'Day 2', '1', 0.0, 2), (3, 'Day 3', '1', 2.0, 2), (4, 'Day 4', '1', 2.0, 2), (5, 'Day 5', '1', 1.0, 2)]
        for task_detail in task_details:
            days_info = task_detail[1]
            days_num = int(days_info.split(" ")[1])
            delete_days_list.append(days_num)
            weeks_info = task_detail[2]
            actual_qty_info = task_detail[3]
            habit_id_info = task_detail[4]
            main.infoMsg(f'{days_info} (Week {weeks_info}) the inputted quantity is {actual_qty_info} {habit_infos[0][3]}')

        self.test_delete_record_day_2
        delete_days_list = []

    @patch('main.ActionToTake', return_value='I')
    def test_action_to_take_i(self, input):
        self.assertEqual(main.actionToTake(), self.select_i)
        main.infoMsg('See you next time!')

    @patch('main.ActionToTake', return_value='X')
    def test_action_to_take_x(self, input):
        self.assertEqual(main.actionToTake(), self.select_others)
        main.errorMsg('Wrong input. Please try again. (ATT)')
        return self.test_action_to_take_x

    # 6A, 6C) SHOW HABITS
    # ------------------------------
    @patch('builtins.print')
    def test_show_all_habit_only(self, mock_print):
        all_habits = ['Listen To Music', 'Play An Instrument', 'Sleep', 'Run', 'Swim']
        main.infoMsg('Below are all the available habits: ')
        for all_habit in all_habits:
            main.infoMsg(f'{all_habit}')
            mock_print.assert_called_with(f'{Fore.BLUE}{all_habit}{Style.RESET_ALL}')
        print('')

    # 6B, 6D) SHOW HABIT & ANALYSIS
    # ------------------------------
    @patch('builtins.print')
    def test_show_all_habits_print(self, mock_print):
        all_habits = ['Listen To Music', 'Play An Instrument', 'Sleep', 'Run', 'Swim']
        main.infoMsg('Below are all the available habits: ')
        habit_num_list = []
        for all_habit in all_habits:
            main.infoMsg(f'{all_habit}')
            mock_print.assert_called_with(f'{Fore.BLUE}{all_habit}{Style.RESET_ALL}')
        print('')
        habit_num_list = []

    @patch('main.ShowAllHabits', return_value='2')
    def test_show_all_habits_int(self, input):
        self.assertEqual(main.showAllHabits(), self.qty_selection2)
        input_habit = int(self.qty_selection2)

    @patch('builtins.print')
    def test_show_all_habits_nonint(self, mock_print):
        input_habit = 'Hello'
        with self.assertRaises(ValueError):
            input_habit = int(input_habit)
            main.errorMsg('Wrong input. Please try again. (SAH)')
            return self.test_show_all_habit_only

    def test_show_all_habits_in_list(self):
        habit_num_list = [1, 2, 3, 4, 5]
        input_habit = int(self.qty_selection2)
        if input_habit not in habit_num_list:
            main.errorMsg('Wrong input. Please try again. (SAH2)')
            return self.test_show_all_habits_in_list
        else:
            return input_habit

    def test_show_all_habits_not_in_list(self):
        habit_num_list = [1, 3, 4, 5]
        input_habit = int(self.qty_selection2)
        if input_habit not in habit_num_list:
            main.errorMsg('Wrong input. Please try again. (SAH2)')
            return self.test_show_all_habits_in_list
        else:
            return input_habit

    # 6C) ADD NEW HABIT NAME
    # ------------------------------
    @patch('main.AddHabitName', return_value='Drink Coffee')
    def test_add_habit_name_input(self, input):
        self.assertEqual(main.addHabitName(), self.habit_name.title())

    def test_add_habit_name_duplicate(self):
        self.test_add_habit_name_input
        duplicated_list = []
        if self.habit_name.title() not in duplicated_list:
            duplicated_list.append(self.habit_name.title())
        else:
            duplicated_list.remove(self.habit_name.title())
        if len(duplicated_list) > 0:
            main.errorMsg('Duplicated Input, please try again. (AHN)')
            return self.test_add_habit_name_duplicate

    def test_add_habit_name_not_duplicate(self):
        duplicated_list = ['Drink Coffee']
        if self.habit_name.title() not in duplicated_list:
            duplicated_list.append(self.habit_name.title())
        else:
            duplicated_list.remove(self.habit_name.title())
        if len(duplicated_list) > 0:
            main.errorMsg('Duplicated Input, please try again. (AHN)')
            return self.test_add_habit_name_duplicate

    # 6C) ADD NEW DESCRIPTION
    # ------------------------------
    @patch('main.AddDescription', return_value='to wake myself')
    def test_add_description(self, input):
        self.assertEqual(main.addDescription(), self.habit_description)

    def test_add_description_short(self):
        input_de = self.habit_description
        return self.test_add_description_short

    def test_add_description_long(self):
        input_de = self.habit_description_long
        if len(input_de) > 50:
            main.errorMsg('Description has to be within 50 characters. Please try again.')
            return self.test_add_description_long

    # 6C) ADD NEW OPERATOR
    # ------------------------------
    @patch('main.AddOperator', return_value='A')
    def test_add_operator_a(self, input):
        self.assertEqual(main.addOperator(), self.select_a)
        if self.select_a == "A":
            input_op = "at least"
        elif self.select_a == "B":
            input_op = "less than"
        else:
            main.errorMsg('Wrong input. Please try again. (AO)')
            return self.test_add_operator_a

    @patch('main.AddOperator', return_value='B')
    def test_add_operator_b(self, input):
        self.assertEqual(main.addOperator(), self.select_b)
        if self.select_b == "A":
            input_op = "at least"
        elif self.select_b == "B":
            input_op = "less than"
        else:
            main.errorMsg('Wrong input. Please try again. (AO)')
            return self.test_add_operator_b

    @patch('main.AddOperator', return_value='X')
    def test_add_operator_x(self, input):
        self.assertEqual(main.addOperator(), self.select_others)
        if self.select_others == "A":
            input_op = "at least"
        elif self.select_others == "B":
            input_op = "less than"
        else:
            main.errorMsg('Wrong input. Please try again. (AO)')
            return self.test_add_operator_x

    # 6C, 6E) ADD NEW TARGET QUANTITY
    # ------------------------------
    @patch('main.AddEditTargetQuantity', return_value='2')
    def test_add_edit_target_quantity_float(self, input):
        self.assertEqual(main.addEditTargetQuantity(), self.qty_selection2)
        float(self.qty_selection2)
        return self.qty_selection2

    @patch('main.AddEditTargetQuantity')
    def test_add_edit_target_quantity_nonfloat(self, mock_print):
        with self.assertRaises(ValueError):
            float(self.select_others)
            main.errorMsg('Wrong input. Please try again. (AETQ)')
            return self.test_add_edit_target_quantity_nonfloat

    # 6C) ADD NEW UNIT
    # ------------------------------
    @patch('main.AddUnit', return_value='times')
    def test_add_unit(self, input):
        self.assertEqual(main.addUnit(), self.habit_unit)

    # 6C) ADD NEW FREQUENCY
    # ------------------------------
    @patch('main.AddFrequency', return_value='A')
    def test_add_frequency_a(self, input):
        self.assertEqual(main.addFrequency(), self.select_a)
        if self.select_a == "A":
            input_fr = "at least"
        elif self.select_a == "B":
            input_fr = "less than"
        else:
            main.errorMsg('Wrong input. Please try again. (AF)')
            return self.test_add_frequency_a

    @patch('main.AddFrequency', return_value='B')
    def test_add_frequency_b(self, input):
        self.assertEqual(main.addFrequency(), self.select_b)
        if self.select_b == "A":
            input_fr = "at least"
        elif self.select_b == "B":
            input_fr = "less than"
        else:
            main.errorMsg('Wrong input. Please try again. (AF)')
            return self.test_add_frequency_b

    @patch('main.AddFrequency', return_value='X')
    def test_add_frequency_x(self, input):
        self.assertEqual(main.addFrequency(), self.select_others)
        if self.select_others == "A":
            input_fr = "at least"
        elif self.select_others == "B":
            input_fr = "less than"
        else:
            main.errorMsg('Wrong input. Please try again. (AF)')
            return self.test_add_frequency_x

    # 6C) ADD NEW DAYS TO SUCCESS
    # ------------------------------
    @patch('main.AddDaysToSuccess', return_value='0')
    def test_add_days_to_success_0(self, input):
        self.assertEqual(main.addDaysToSuccess(), self.qty_selection0)
        if self.qty_selection0 == '0' or self.qty_selection0 == 0:
            main.errorMsg('Cannot be 0. Please try again. (ADTS)')
            return self.test_add_days_to_success_0

    @patch('main.AddDaysToSuccess', return_value='2')
    def test_add_days_to_success_2(self, input):
        self.assertEqual(main.addDaysToSuccess(), self.qty_selection2)
        if self.qty_selection2 == '0' or self.qty_selection2 == 0:
            main.errorMsg('Cannot be 0. Please try again. (ADTS)')
            return self.test_add_days_to_success_2
        int(self.qty_selection2)
        return self.qty_selection2

    @patch('main.AddDaysToSuccess', return_value='X')
    def test_add_days_to_success_x(self, input):
        self.assertEqual(main.addDaysToSuccess(), self.select_others)
        if self.select_others == '0' or self.select_others == 0:
            main.errorMsg('Cannot be 0. Please try again. (ADTS)')
            return self.test_add_days_to_success_x
        with self.assertRaises(ValueError):
            int(self.select_others)
            main.errorMsg('Wrong input. Please try again. (ADTS2)')
            return self.test_add_days_to_success_x

    # 6D) RECORD INFO
    # ------------------------------
    @patch('main.RecordDayAndWeek', return_value='2')
    def test_record_day_and_week_2(self, input):
        self.assertEqual(main.recordDayAndWeek(), self.qty_selection2)
        input_day = int(self.qty_selection2)

        date_info = f'Day {input_day}'
        week_info = math.ceil(int(input_day)/7)
        self.assertEqual(date_info, 'Day 2')
        self.assertEqual(week_info, 1)

    @patch('main.RecordDayAndWeek', return_value='13')
    def test_record_day_and_week_13(self, input):
        self.assertEqual(main.recordDayAndWeek(), self.qty_selection13)
        input_day = int(self.qty_selection13)

        date_info = f'Day {input_day}'
        week_info = math.ceil(int(input_day)/7)
        self.assertEqual(date_info, 'Day 13')
        self.assertEqual(week_info, 2)

    @patch('main.RecordDayAndWeek', return_value='X')
    def test_record_day_and_week_x(self, input):
        self.assertEqual(main.recordDayAndWeek(), self.select_others)
        with self.assertRaises(ValueError):
            input_day = int(self.select_others)
            main.errorMsg('Wrong input. Please try again. (RDAW)')
            return self.test_record_day_and_week_x

    # 6D, 6F) RECORD QUANTITY
    # ------------------------------
    @patch('main.AddEditRecordQuantity', return_value='2')
    def test_add_edit_record_quantity_2(self, input):
        self.assertEqual(main.addEditRecordQuantity(), self.qty_selection2)
        float(self.qty_selection2)

    @patch('main.AddEditRecordQuantity', return_value='X')
    def test_add_edit_record_quantity_x(self, input):
        self.assertEqual(main.addEditRecordQuantity(), self.select_others)
        with self.assertRaises(ValueError):
            float(self.select_others)
            main.errorMsg('Wrong input. Please try again. (AERQ)')
            return self.test_add_edit_record_quantity_x

    # 6E, 6F) EDIT A HABIT
    # ------------------------------
    @patch('main.EditAHabit', return_value='2')
    def test_edit_a_habit_2(self, input):
        main.infoMsg('Below are all the available habits: ')
        habit_num_list = []
        all_habits = [(1, 'Listen To Music'), (2, 'Play An Instrument'), (3, 'Sleep'), (4, 'Run'), (5, 'Swim')]
        for all_habit in all_habits:
            main.infoMsg(f'{all_habit}')
            habit_num_list.append(all_habit[0])

        self.assertEqual(main.editAHabit(), self.qty_selection2)
        edit_habit = int(self.qty_selection2)

        habit_num_list = []

    @patch('main.EditAHabit', return_value='X')
    def test_edit_a_habit_x(self, input):
        main.infoMsg('Below are all the available habits: ')
        habit_num_list = []
        all_habits = [(1, 'Listen To Music'), (2, 'Play An Instrument'), (3, 'Sleep'), (4, 'Run'), (5, 'Swim')]
        for all_habit in all_habits:
            main.infoMsg(f'{all_habit}')
            habit_num_list.append(all_habit[0])

        self.assertEqual(main.editAHabit(), self.select_others)
        with self.assertRaises(ValueError):
            edit_habit = int(self.select_others)
            main.errorMsg('Wrong input. Please try again. (EAH)')
            return self.test_edit_a_habit_x

        habit_num_list = []

    @patch('main.EditAHabit', return_value='0')
    def test_edit_a_habit_0(self, input):
        main.infoMsg('Below are all the available habits: ')
        habit_num_list = []
        all_habits = [(1, 'Listen To Music'), (2, 'Play An Instrument'), (3, 'Sleep'), (4, 'Run'), (5, 'Swim')]
        for all_habit in all_habits:
            main.infoMsg(f'{all_habit}')
            habit_num_list.append(all_habit[0])

        self.assertEqual(main.editAHabit(), self.qty_selection0)
        edit_habit = int(self.qty_selection0)

        if edit_habit not in habit_num_list:
            main.errorMsg('Wrong input. Please try again. (EAH2)')
            return self.test_edit_a_habit_0
        else:
            return edit_habit

        habit_num_list = []

    # 6F) EDIT RECORD DAY SELECTION
    # ------------------------------
    @patch('main.EditRecordDay', return_value='2')
    def test_edit_record_day_2(self, input):
        self.assertEqual(main.editRecordDay(), self.qty_selection2)
        edit_day = int(self.qty_selection2)

        date_info = f'Day {edit_day}'
        week_info = math.ceil(int(edit_day)/7)
        self.assertEqual(date_info, 'Day 2')
        self.assertEqual(week_info, 1)

    @patch('main.EditRecordDay', return_value='X')
    def test_edit_record_day_x(self, input):
        self.assertEqual(main.editRecordDay(), self.select_others)
        with self.assertRaises(ValueError):
            edit_day = int(self.select_others)
            main.errorMsg('Wrong input. Please try again. (ERD)')
            return self.test_edit_record_day_x

    @patch('main.EditRecordDay', return_value='0')
    def test_edit_record_day_0(self, input):
        edit_days_list = [1, 2, 3, 4, 5]
        self.assertEqual(main.editRecordDay(), self.qty_selection0)
        edit_day = int(self.qty_selection0)

        if edit_day not in edit_days_list:
            main.errorMsg('No such day info. Please try again. (ERD2)')
            return self.test_edit_record_day_0

    # 6G, 6H) DELETE A HABIT
    # ------------------------------
    @patch('main.DeleteAHabit', return_value='2')
    def test_delete_a_habit_2(self, input):
        main.infoMsg('Below are all the available habits: ')
        habit_num_list = []
        all_habits = [(1, 'Listen To Music'), (2, 'Play An Instrument'), (3, 'Sleep'), (4, 'Run'), (5, 'Swim')]
        for all_habit in all_habits:
            main.infoMsg(f'{all_habit}')
            habit_num_list.append(all_habit[0])
        print("")

        self.assertEqual(main.deleteAHabit(), self.qty_selection2)
        delete_habit = int(self.qty_selection2)

        habit_num_list = []

    @patch('main.DeleteAHabit', return_value='X')
    def test_delete_a_habit_x(self, input):
        main.infoMsg('Below are all the available habits: ')
        habit_num_list = []
        all_habits = [(1, 'Listen To Music'), (2, 'Play An Instrument'), (3, 'Sleep'), (4, 'Run'), (5, 'Swim')]
        for all_habit in all_habits:
            main.infoMsg(f'{all_habit}')
            habit_num_list.append(all_habit[0])
        print("")

        self.assertEqual(main.deleteAHabit(), self.select_others)
        with self.assertRaises(ValueError):
            delete_habit = int(self.select_others)
            main.errorMsg('Wrong input. Please try again. (DAH)')
            return self.test_delete_a_habit_x

        habit_num_list = []

    @patch('main.DeleteAHabit', return_value='0')
    def test_delete_a_habit_0(self, input):
        main.infoMsg('Below are all the available habits: ')
        habit_num_list = []
        all_habits = [(1, 'Listen To Music'), (2, 'Play An Instrument'), (3, 'Sleep'), (4, 'Run'), (5, 'Swim')]
        for all_habit in all_habits:
            main.infoMsg(f'{all_habit}')
            habit_num_list.append(all_habit[0])
        print("")

        self.assertEqual(main.deleteAHabit(), self.qty_selection0)
        delete_habit = int(self.qty_selection0)

        if delete_habit not in habit_num_list:
            main.errorMsg('Wrong input. Please try again. (DAH2)')
            return self.test_delete_a_habit_0
        else:
            return delete_habit

        habit_num_list = []

    # 6H) DELETE RECORD DAY SELECTION
    # ------------------------------
    @patch('main.DeleteRecordDay', return_value='2')
    def test_delete_record_day_2(self, input):
        self.assertEqual(main.deleteRecordDay(), self.qty_selection2)
        delete_day = int(self.qty_selection2)

        date_info = f'Day {delete_day}'
        self.assertEqual(date_info, 'Day 2')

    @patch('main.DeleteRecordDay', return_value='X')
    def test_delete_record_day_x(self, input):
        self.assertEqual(main.deleteRecordDay(), self.select_others)
        with self.assertRaises(ValueError):
            delete_day = int(self.select_others)
            main.errorMsg('Wrong input. Please try again. (DRD)')
            return self.test_delete_record_day_x

    @patch('main.DeleteRecordDay', return_value='0')
    def test_delete_record_day_0(self, input):
        delete_days_list = [1, 2, 3, 4, 5]
        self.assertEqual(main.deleteRecordDay(), self.qty_selection0)
        delete_day = int(self.qty_selection0)

        if delete_day not in delete_days_list:
            main.errorMsg('No such day info. Please try again. (DRD2)')
            return self.test_delete_record_day_0

    # PART 7
    # ------------------------------
    def test_completion_performance(self):
        self.assertEqual(main.completionPerformance(0, 0), main.analysisMsgF('Your problem might be forgetful! Key in some records for your habit.\n'))
        self.assertEqual(main.completionPerformance(0, 5), main.analysisMsgF('If your have already tried your best. Maybe you should reset your habit target.\n'))
        self.assertEqual(main.completionPerformance(18, 5), main.analysisMsgF('Your performance is way behind. But no worry, things would get better, keep going!\n'))
        self.assertEqual(main.completionPerformance(38, 5), main.analysisMsgF('Be more aggressive to achieve your habit target or lower your target setting.\n'))
        self.assertEqual(main.completionPerformance(58, 5), main.analysisMsgS('I am sure you could do better!\n'))
        self.assertEqual(main.completionPerformance(78, 5), main.analysisMsgS('You are doing better and better!\n'))
        self.assertEqual(main.completionPerformance(98, 5), main.analysisMsgS('You are about to be perfect\n'))
        self.assertEqual(main.completionPerformance(100, 5), main.analysisMsgS('You are a (wo)man of word!\n'))

    def test_longest_strike(self):
        self.assertEqual(main.longestStrike(strike_list=[True, True, False, True, False, False, True, True, True, True, False, True]), 4)
        self.assertEqual(main.longestStrike(strike_list=[True, True, False, True, False, False, True, True, True, False, True]), 3)
        self.assertEqual(main.longestStrike(strike_list=[True, True, False, True, False, False, True, True, False, True]), 2)
        self.assertEqual(main.longestStrike(strike_list=[]), 0)


''' TEST FOR DATABASE IS MEANT TO BE INCORRECT AS INFORMATION WOULD ALWAYS BE UPDATED '''
# USER DB
# ------------------------------
class TestUserDB(unittest.TestCase):
    def test_insert_user(self):
        self.assertEqual(user_db.insertUser(main.UserCreate('test1@gmail.com', 'TEST1234', '2022-03-21')), None)

    def test_search_first_habit(self):
        self.assertEqual(user_db.searchFirstInput(1), [(1,)])
        self.assertEqual(user_db.searchFirstInput(2), [(2,)])

    def test_search_user(self):
        self.assertEqual(user_db.searchUser('test1@gmail.com'), [(1, 'test1@gmail.com', 'TEST1234', '2022-07-14')])

    def test_first_reg_login_id(self):
        self.assertEqual(user_db.firstRegLoginID(), (5,))

    def test_update_password(self):
        self.assertEqual(user_db.updatePassword(3, '2022-03-06'), None)

    def test_check_database(self):
        self.assertEqual(user_db.checkDB()[0], (1, 'test1@gmail.com', 'TEST1234', '2022-07-16'))

# HABIT DB
# ------------------------------
class TestHabitDB(unittest.TestCase):
    def test_insert_habit(self):
        habit = main.HabitCreate('Drink Coffee', 'Awake Myself', 'at least', 1.0, 'cups', 'daily', 5, 1)
        self.assertEqual(habit_db.insertHabit(habit), None)

    def test_search_first_habit(self):
        self.assertEqual(habit_db.searchFirstHabit(1), [(1,), (1,), (1,), (1,), (1,)])

    def test_all_habit(self):
        self.assertEqual(habit_db.allHabit(1), [(1, 'Listen To Music'), (2, 'Play An Instrument'), (3, 'Sleep'), (4, 'Run'), (5, 'Swim')])

    def test_search_latest_habit(self):
        self.assertEqual(habit_db.searchLatestHabit(), (35, 30, 'Swim'))

    def test_search_habit(self):
        self.assertEqual(habit_db.searchHabit(1), [('Listen To Music', 'at least', 10.0, 'songs', 'daily', 30)])

    def test_duplicate_habit_check(self):
        self.assertEqual(habit_db.duplicateHabitCheck('Go to Church'), [])
        self.assertEqual(habit_db.duplicateHabitCheck('Run')[0], (4, 'Run', 'Build up strength', 'at least', 3.0, 'times', 'weekly', 28, 1))


    def test_update_habit(self):
        self.assertEqual(habit_db.updateHabit(1, "at least", 100, 'times', 'weekly', 49), None)

    def test_remove_habit(self):
        self.assertEqual(habit_db.removeHabit(1), None)

    def test_check_database(self):
        self.assertEqual(habit_db.checkDB()[1], (2, 'Play An Instrument', 'Build up the art sense', 'at least', 12.0, 'hours', 'weekly', 28, 1))

# TASK DETAIL DB
# ------------------------------
class TestTaskDetailDB(unittest.TestCase):
    def test_auto_create_task_detail(self):
        self.assertEqual(task_detail_db.autoCreateTaskDetail(), None)

    def test_insesrt_task_detail(self):
        task = main.RecordCreate(1, 1, 2, 2)
        self.assertEqual(task_detail_db.insertTaskDetail(task), None)

    def test_search_task_detail(self):
        self.assertEqual(task_detail_db.searchTaskDetail(100), [])

    def test_sum_quantity(self):
        self.assertEqual(task_detail_db.sumQuantity(2), [(17.0,), (13.0,), (9.0,), (8.0,)])

    def test_search_task_id(self):
        self.assertEqual(task_detail_db.searchTaskID('2022-03-06', 100), [])

    def test_update_task_detail(self):
        self.assertEqual(task_detail_db.updateTaskDetail('1', 1, 1, 3.0), None)

    def test_remove_task_detail(self):
        self.assertEqual(task_detail_db.removeTaskDetail(4), None)

    def test_remove_task_detail_two(self):
        self.assertEqual(task_detail_db.removeTaskDetailTwo(2), None)

    def test_count_records_inputted(self):
        self.assertEqual(task_detail_db.countRecordsInputted(1), [(29,)])

    def test_check_database(self):
        self.assertEqual(task_detail_db.checkDB()[0], (1, '1', '1', 3.0, 1))


if __name__ == '__main__':
    unittest.main()