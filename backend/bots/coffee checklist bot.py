import sqlite3
import jdatetime
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from persiantools.jdatetime import JalaliDate
from datetime import datetime, date, timezone, timedelta
from functools import wraps
from unidecode import unidecode

########################################################################################
bot = telebot.TeleBot("6529303457:AAH7KeM8AJdruJQ8YqlabNIknFKBeMT9uYY")
# the d bot token: 6529303457:AAH7KeM8AJdruJQ8YqlabNIknFKBeMT9uYY
# frz test bot token: 1163491358:AAFsn2EW38nMpLI_vlPKelmTEvO9N-fDQ0o
########################################################################################
user_name = None
user_id = None
month_selected = None
day_selected = None
branch = None
section = str()
shift = None
roastery_name = None
coffee_line = None
coffee_given = None
coffee_remain = None
espresso_dosage = None
espresso_yield = None
espresso_temp = None
espresso_time = None
water_tds = None
waste_and_caliber = None
test_and_qc = None
description_data = None
########################################################################################
conn = sqlite3.connect('database_2.db', check_same_thread=False)
cursor = conn.cursor()
# cursor.execute('''CREATE TABLE IF NOT EXISTS checklist (
# 	"id"	 INTEGER NOT NULL PRIMARY KEY,
#     "date_of_insert"     TEXT NOT NULL,
#     "time_of_insert"    TEXT NOT NULL,
#     "date_ordinal"    INTEGER NOT NULL,

#     "branch"    TEXT NOT NULL,
# 	"
# "	TEXT NOT NULL,
# 	"section"	TEXT NOT NULL,
# 	"shift"    TEXT NOT NULL,
# 	"roastery_name"    TEXT NOT NULL,
# 	"coffee_line"	TEXT NOT NULL,
# 	"coffee_given"    INTEGER NOT NULL,
# 	"coffee_remain"    INTEGER NOT NULL,
# 	"espresso_dosage"	INTEGER,
# 	"espresso_yield"	INTEGER,
# 	"espresso_temp"    INTEGER,
# 	"espresso_time"    INTEGER,
#     "water_tds"    INTEGER,
# 	"waste_and_caliber"  INTEGER NOT NULL,
#     "test_and_qc"    INTEGER NOT NULL,
#     "description"    TEXT,
#     "edited"    INTEGER DEFAULT '0'
# );
# ''')
cursor.execute('''CREATE TABLE IF NOT EXISTS checklist (
	"id"	 INTEGER NOT NULL PRIMARY KEY,
    "date_of_insert"     TEXT NOT NULL,
    "time_of_insert"    TEXT NOT NULL,
    "date_ordinal"    INTEGER NOT NULL,
    "data_month"    TEXT NOT NULL,
    "data_date"    INT NOT NULL,
    "branch"    TEXT NOT NULL,
	"user_name"	TEXT NOT NULL,
    "user_id"    INT NOT NULL,
	"section"	TEXT NOT NULL,
	"shift"    TEXT NOT NULL,
	"roastery_name"    TEXT NOT NULL,
	"coffee_line"	TEXT NOT NULL,
	"coffee_given"    INTEGER NOT NULL,
	"coffee_remain"    INTEGER NOT NULL,
	"espresso_dosage"	INTEGER,
	"espresso_yield"	INTEGER,
	"espresso_temp"    INTEGER,
	"espresso_time"    INTEGER,
    "water_tds"    INTEGER,
	"waste_and_caliber"  INTEGER NOT NULL,
    "test_and_qc"    INTEGER NOT NULL,
    "description"    TEXT,
    "edited"    INTEGER DEFAULT '0'
);
''')

# def insert_to_db(time_now:str, ordinal_date: int, month_selected:str, day_selected:int, branch:str, user_name:str, section:str, shift:str, roastery_name:str, coffee_line:str, coffee_given:int, coffee_remain:int, espresso_dosage:int, espresso_yield:int, espresso_temp:int, espresso_time:int, water_tds:int, waste_and_caliber:int, test_and_qc:int, description_data:str):
#     cursor.execute('INSERT INTO checklist (time_of_insert, date_ordinal, data_month, data_date, branch, user_name, section, shift, roastery_name, coffee_line, coffee_given, coffee_remain, espresso_dosage, espresso_yield, espresso_temp, espresso_time, water_tds, waste_and_caliber, test_and_qc, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (time_now, ordinal_date, month_selected, day_selected, branch, user_name, section, shift, roastery_name, coffee_line, coffee_given, coffee_remain, espresso_dosage, espresso_yield, espresso_temp, espresso_time, water_tds, waste_and_caliber, test_and_qc, description_data))
#     conn.commit()

########################################################################################
month_markup = types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True, resize_keyboard=True)

month_markup.add("خرداد", "اردیبهشت", "فروردین", "شهریور", "مرداد", "تیر", "آذر", "آبان", "مهر", "اسفند", "بهمن", "دی")
month = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
month_dict = {
    "فروردین" : 1 ,
    "اردیبهشت" : 2 ,
    "خرداد" : 3 ,
    "تیر" : 4 ,
    "مرداد" : 5 ,
    "شهریور" : 6 ,
    "مهر" : 7 ,
    "آبان" : 8 ,
    "آذر" : 9 ,
    "دی" : 10 ,
    "بهمن" : 11 ,
    "اسفند" : 12  
}
month_31 = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور"]
month_30 = ["مهر", "آبان", "آذر", "دی", "بهمن"]
month_29 = ["اسفند"]
########################################################################################
branch_markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
branch_markup.add("شهرک غرب", "فرشته")
branches = ["شهرک غرب", "فرشته"]
########################################################################################
section_markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
section_markup.add("قهوه سیاه", "قهوه با شیر", "بار دمی")
sections = ["قهوه سیاه", "قهوه با شیر", "بار دمی"]
########################################################################################
shifts_markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
shifts_markup.add("صبح", "عصر")
shifts = ["صبح", "عصر"]
########################################################################################
roastery_markup = types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True, resize_keyboard=True)
roastery_markup.add("TDS", "Moa", "Line","Hayk", "Alba", "Xav", "Dam", "Rei")
roastery = ["tds", "hayk", "line", "alba", "xav", "moa", "dam", "rei"]
########################################################################################
tds_markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
tds_markup.add("Mashima", "Masama Mula", "Colombia", "Panama", "Ethiopia")
tds_lines = ["mashima", "masama mula", "colombia", "panama", "ethiopia"]
########################################################################################
moa_markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
moa_markup.add("Wazn", "Colombia", "Sirus")
moa_lines = ["wazn", "colombia", "sirus"]
########################################################################################
dam_markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
dam_markup.add("Ethiopia", "Colombia")
dam_lines = ["ethiopia", "colombia"]
########################################################################################
line_roastery_markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
line_roastery_markup.add("El Salvador")
line_roastery_lines = ["el salvador"]
########################################################################################
yes_no_markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
yes_no_markup.add("بله", "خیر")
########################################################################################
next_markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
next_markup.add("بعدی")
########################################################################################
back_markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
back_markup.add("بازگشت")

########################################################################################
# finished_restart_markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
# finished_restart_markup.add("ورود اطلاعات جدید")
# new_data = "ورود اطلاعات جدید"

sure = "\n از انتخاب خود مطمئن هستید؟"
incorrect_format = "لطفا اطلاعات را با فرمت درست وارد کنید"
wrong_input = "مقدار وارد شده صحیح نمیباشد"

########################################################################################
year = 1402
def convert_to_excel_ordinal(year, month, day):
    offset = 693594
    mytime = JalaliDate(year, month, day).to_gregorian()
    n = mytime.toordinal()
    return (n - offset)
########################################################################################



def is_known_username(username):
    '''
    Returns a boolean if the username is known in the user-list.
    '''
    # known_usernames = ["Fuadrn", "mahannemati", ]
    known_usernames = ["Fuadrn", "mahannemati", "Azerila101", "Daniamd", "Salarlj", "siinao", "Aria_shahmoradi", "Salehinjas", "radman_ad", "mersedehsf", "Dihav22", "atiyeesalehi", "norronn", "Aynztrki", "mehghsa", "mamadmalih", "ariyan_vmvmv", "Alirzakhosravi", "Parisa_shabahang", "moonborn666", "Bigapoune", "Alizm9774", "Layazahdi", "arminAdis", "violet_kr", "Ialibarzegar", "Mahdimohebiii", "Parzzaa"]

    return username in known_usernames


def private_access():
    """
    Restrict access to the command to users allowed by the is_known_username function.
    """
    def deco_restrict(f):

        @wraps(f)
        def f_restrict(message, *args, **kwargs):
            username = message.from_user.username

            if is_known_username(username):
                return f(message, *args, **kwargs)
            else:
                bot.reply_to(message, text='شما مجاز به ورود اطلاعات نیستید')

        return f_restrict  # true decorator

    return deco_restrict


########################################################################################






@bot.message_handler(commands=['start'])
########################################################################################
@private_access()
########################################################################################


def start(message):

    global user_name
    global user_id
    if message.from_user.username:
        user_name = message.from_user.username
    else:
        user_name = message.from_user.first_name

    user_id = message.from_user.id
    # message.from_user.first_name
    # message.from_user.last_name
    # message.from_user.username

    msg = bot.send_message(message.chat.id, "انتخاب ماه", reply_markup=month_markup)
    bot.register_next_step_handler(msg, month_validation)
########################################################################################
def month_validation(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    else:
        if message.text.lower() not in month:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            bot.register_next_step_handler(msg, month_validation)
        else:
            global month_selected

            month_selected = message.text
            
            day_select (message)

########################################################################################
def day_select(message):
    msg = bot.send_message(message.chat.id, "روز را وارد کنید", reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, day_validation)

def day_validation(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        start(message)
    else:
        global day_selected
        if month_selected in month_31:
            try:
                day_input = int(message.text)
                if day_input > 31 or day_input < 1:
                    msg = bot.reply_to(message, "ماه نهایتا 31 روز دارد!")
                    bot.register_next_step_handler(msg, day_validation)
                else:
                    day_selected = message.text
                    # day_assurance (message)
                    branch_selection(message)
            except ValueError:
                msg = bot.reply_to(message, "ورودی غیر مجاز")
                # bot.register_next_step_handler(msg, day_validation)
                bot.register_next_step_handler(msg, day_validation)


        elif month_selected in month_30:
            try:
                day_input = int(message.text)
                if day_input > 30 or day_input < 1:
                    msg = bot.reply_to(message, "ماه انتخابی شما 30 روز دارد")
                    bot.register_next_step_handler(msg, day_validation)
                else:
                    day_selected = message.text
                    # day_assurance (message)
                    branch_selection(message)
            except ValueError:
                msg = bot.reply_to(message, "ورودی غیر مجاز")
                # bot.register_next_step_handler(msg, day_validation)
                bot.register_next_step_handler(msg, day_select)
        elif month_selected in month_29:
            try:
                day_input = int(message.text)
                if day_input > 29 or day_input < 1:
                    msg = bot.reply_to(message, "اسفند 29 روز دارد")
                    bot.register_next_step_handler(msg, day_validation)
                else:
                    day_selected = message.text
                    # day_assurance (message)
                    branch_selection(message)
            except ValueError:
                msg = bot.reply_to(message, "ورودی غیر مجاز")
                # bot.register_next_step_handler(msg, day_validation)
                bot.register_next_step_handler(msg, day_select)

        else:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            # bot.register_next_step_handler(msg, day_validation)
            bot.register_next_step_handler(msg, day_select)

    # def day_assurance(message):
    #     msg = bot.send_message(message.chat.id, message.text +  sure, reply_markup=yes_no_markup)
    #     bot.register_next_step_handler(msg, day_assured)

########################################################################################################################
def branch_selection(message):
    msg = bot.send_message(message.chat.id, "انتخاب شعبه", reply_markup=branch_markup)
    bot.register_next_step_handler(msg, branch_validation)

def branch_validation(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        day_select(message)
    else:
        if message.text.lower() not in branches:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            branch_selection(message)
        else:

            global branch
            branch = message.text
            sections_func(message)

def sections_func(message):
    msg = bot.send_message(message.chat.id, "انتخاب سکشن", reply_markup=section_markup)
    bot.register_next_step_handler(msg, section_validation)
########################################################################################
def section_validation(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        branch_selection(message)
    else:
        if message.text.lower() not in sections:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            bot.register_next_step_handler(msg, section_validation)
        else:
            global section
            section = message.text
            shift_choose(message)

########################################################################################
def shift_choose(message):
    msg = bot.send_message(message.chat.id, "انتخاب شیفت", reply_markup=shifts_markup)

    if section.lower() in sections:
        bot.register_next_step_handler(msg, shift_validation)        

    else:
        bot.reply_to(message, incorrect_format)
        bot.register_next_step_handler(msg, sections_func)
########################################################################################
def shift_validation(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        sections_func(message)
    else:
        if message.text.lower() in shifts:
            global shift
            shift = message.text
            shift_select(message)
        else:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            bot.register_next_step_handler(msg, shift_validation)
########################################################################################
# def shift_assurance(message):
#     msg = bot.send_message(message.chat.id, message.text +  sure, reply_markup=yes_no_markup)
#     bot.register_next_step_handler(msg, shift_assured)
########################################################################################
def shift_select(message):

    if shift.lower() in shifts:
        roastery_select(message)

    else:
        bot.reply_to(message, incorrect_format)
        shift_select(message)
########################################################################################
def roastery_select(message):
    msg = bot.send_message(message.chat.id, "انتخاب روستری", reply_markup=roastery_markup)
    bot.register_next_step_handler(msg, roastery_validation)

def roastery_validation(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        shift_choose(message)
    else:
        global roastery_name
        if message.text.lower() in roastery:
            if message.text.lower() == "tds":
                roastery_name = message.text
                tds_roastery_chosen(message)
                # roastery_assurance(message)
            elif message.text.lower() == "moa":
                roastery_name = message.text
                moa_roastery_chosen(message)

            #################################################
            elif message.text.lower() == "dam":
                roastery_name = message.text
                dam_roastery_chosen(message)
            #################################################
            elif message.text.lower() == "line":
                roastery_name = message.text
                line_roastery_chosen(message)
            #################################################
                # roastery_assurance(message)
            else:
                msg = bot.send_message(message.chat.id, "گزینه انتخاب شده فعلا موجود نمیباشد")
                roastery_select(message)
        else:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            roastery_select(message)
########################################################################################
def dam_roastery_chosen(message):
    msg = bot.send_message(message.chat.id, "انتخاب لاین", reply_markup=dam_markup)
    bot.register_next_step_handler(msg, dam_assurance)

def dam_assurance(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        roastery_select(message)
    else:
        global coffee_line
        if roastery_name.lower() == "dam":
            if message.text.lower() in dam_lines:

                coffee_line = message.text
                coffee_in_validation(message)
            else:
                msg = bot.reply_to(message, incorrect_format)
                dam_roastery_chosen(message)
        else:
            msg = bot.reply_to(message, incorrect_format)
            dam_roastery_chosen(message)      
########################################################################################
def line_roastery_chosen(message):
    msg = bot.send_message(message.chat.id, "انتخاب لاین", reply_markup=line_roastery_markup)
    bot.register_next_step_handler(msg, line_roastery_assurance)

def line_roastery_assurance(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        roastery_select(message)
    else:
        global coffee_line
        if roastery_name.lower() == "line":
            if message.text.lower() in line_roastery_lines:

                coffee_line = message.text
                coffee_in_validation(message)
            else:
                msg = bot.reply_to(message, incorrect_format)
                line_roastery_chosen(message)
        else:
            msg = bot.reply_to(message, incorrect_format)
            line_roastery_chosen(message)      




########################################################################################
def tds_roastery_chosen(message):
    msg = bot.send_message(message.chat.id, "انتخاب لاین", reply_markup=tds_markup)
    bot.register_next_step_handler(msg, tds_assurance)

def tds_assurance(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        roastery_select(message)
    else:
        global coffee_line
        if roastery_name.lower() == "tds":
            if message.text.lower() in tds_lines:

                coffee_line = message.text
                coffee_in_validation(message)
            else:
                msg = bot.reply_to(message, incorrect_format)
                tds_roastery_chosen(message)
        else:
            msg = bot.reply_to(message, incorrect_format)
            tds_roastery_chosen(message)      

########################################################################################
def moa_roastery_chosen(message):
    msg = bot.send_message(message.chat.id, "انتخاب لاین", reply_markup=moa_markup)
    bot.register_next_step_handler(msg, moa_assurance)

def moa_assurance(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        roastery_select(message)
    else:
        global coffee_line
        if roastery_name.lower() == "moa":
            if message.text.lower() in moa_lines:

                coffee_line = message.text
                coffee_in_validation(message)
            else:
                msg = bot.reply_to(message, incorrect_format)
                moa_roastery_chosen(message)
        else:
            msg = bot.reply_to(message, incorrect_format)
            moa_roastery_chosen(message)

########################################################################################
def coffee_in_validation(message):
    msg = bot.send_message(message.chat.id, "میزان ورودی قهوه (تحویلی) به سکشن خود را با واحد گرم وارد کنید", reply_markup=False)
    bot.register_next_step_handler(msg, coffee_in)
########################################################################################
def coffee_in (message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        roastery_select(message)
    else:

        if message.text.isdigit():
            global coffee_given
            if int(message.text) > 100000 or int(message.text) <= 0:
                msg = bot.send_message(message.chat.id, wrong_input)
                bot.register_next_step_handler(msg, coffee_in)
            else:
                coffee_given = message.text
                coffee_remaining_validation(message)
        else: 
            msg = bot.send_message(message.chat.id, "لطفا مقدار عددی وارد کنید")
            bot.register_next_step_handler(msg, coffee_in)

########################################################################################

def coffee_remaining_validation(message):
    msg = bot.send_message(message.chat.id, "میزان باقی مانده قهوه سکشن خود را با واحد گرم وارد کنید")
    bot.register_next_step_handler(msg, coffee_remaining)

########################################################################################
def coffee_remaining (message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        coffee_in_validation(message)
    else:
        global coffee_remain
        if message.text.isdigit():
            if int(message.text) > int(coffee_given):
                msg = bot.send_message(message.chat.id, wrong_input)
                bot.register_next_step_handler(msg, coffee_remaining)
            else:
                coffee_remain = message.text
                shift_diff_validation(message)
        else: 
            msg = bot.send_message(message.chat.id, wrong_input)
            bot.register_next_step_handler(msg, coffee_remaining)

########################################################################################
def shift_diff_validation(message):
    if section.lower() == "قهوه سیاه" or section.lower() == "قهوه با شیر":
        dose_in_validation(message)
    else:
        brew_data(message)

########################################################################################

def dose_in_validation(message):

    msg = bot.send_message(message.chat.id, "میزان کالیبر خود را با واحد گرم وارد کنید")
    bot.register_next_step_handler(msg, dose_in)

########################################################################################
def dose_in(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        coffee_remaining_validation(message)
    else:
        global espresso_dosage
        try:
            dose = float(message.text)
            if dose > 24 or dose < 17:
                msg = bot.send_message(message.chat.id, wrong_input)
                bot.register_next_step_handler(msg, dose_in)
            else:
                espresso_dosage = message.text
                # dose_out_validation(message)
                dose_out_validation(message)

        except ValueError:
            msg = bot.send_message(message.chat.id, wrong_input)
            bot.register_next_step_handler(msg, dose_in)

########################################################################################
def dose_out_validation(message):

    msg = bot.send_message(message.chat.id, "میزان خروجی کالیبر خود را با واحد گرم وارد کنید")
    bot.register_next_step_handler(msg, dose_out)

########################################################################################
def dose_out(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        dose_in_validation(message)
    else:
        global espresso_yield
        try:
            dose = float(message.text)
            if dose > 60 or dose < 20:
                msg = bot.send_message(message.chat.id, wrong_input)
                bot.register_next_step_handler(msg, dose_out)
            else:
                espresso_yield = message.text
                temperature_validation(message)
                # temperature_validation(message)

        except ValueError:
            msg = bot.send_message(message.chat.id, wrong_input)
            bot.register_next_step_handler(msg, dose_out)

########################################################################################

def temperature_validation(message):
    msg = bot.send_message(message.chat.id, "دمای عصاره گیری خود را بر حسب درجه سانتیگراد وارد کنید")
    bot.register_next_step_handler(msg, temprature)

########################################################################################
def temprature(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        dose_out_validation(message)
    else:
        global espresso_temp
        try:
            temp = float(message.text)
            if temp > 95 or temp < 88:
                msg = bot.send_message(message.chat.id, wrong_input)
                bot.register_next_step_handler(msg, temprature)
            else:
                espresso_temp = message.text
                esp_time(message)

        except ValueError:
            msg = bot.send_message(message.chat.id, wrong_input)
            bot.register_next_step_handler(msg, temprature)

########################################################################################


def esp_time(message):
    msg = bot.send_message(message.chat.id, "زمان عصاره گیری خود را با واحد ثانیه وارد کنید")
    bot.register_next_step_handler(msg, espresso_time_validation)

def espresso_time_validation(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        temperature_validation(message)
    else:
        global espresso_time
        try:
            temp = float(message.text)
            if temp > 80 or temp < 10:
                msg = bot.send_message(message.chat.id, wrong_input)
                esp_time(message)
            else:
                espresso_time = message.text
                tds_water(message)

        except ValueError:
            msg = bot.send_message(message.chat.id, wrong_input)
            esp_time(message)

########################################################################################

def tds_water(message):
    msg = bot.send_message(message.chat.id, "میزان TDS آب را وارد کنید \n در صورتی که دسترسی به این اطلاعات ندارید گزینه بعدی را انتخاب کنید", reply_markup=next_markup)
    bot.register_next_step_handler(msg, tds_water_validation)

def tds_water_validation(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        esp_time(message)
    else:
        global water_tds
        try:
            tds = message.text
            if tds.isdigit():
                if int(tds) > 500 or int(tds) < 5:
                    msg = bot.send_message(message.chat.id, wrong_input)          
                    tds_water(message)
                else:
                    water_tds = int(tds)
                    waste_test_caliber(message)
            elif tds == "بعدی":
                water_tds = None
                waste_test_caliber(message)
            else:
                msg = bot.send_message(message.chat.id, wrong_input)          
                tds_water(message)

        except ValueError:
                msg = bot.send_message(message.chat.id, wrong_input)          
                tds_water(message)

########################################################################################
def waste_test_caliber(message):
    msg = bot.send_message(message.chat.id, "مجموع ضایعات و قهوه مورد استفاده برای کالیبر خود را با واحد گرم وارد کنید")
    bot.register_next_step_handler(msg, waste_test)

########################################################################################
def waste_test(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        tds_water(message)
    else:
        global waste_and_caliber
        try:
            waste = int(message.text)

            if waste < 600 and waste >= 0 and waste <= (int(coffee_given) - int(coffee_remain)):
                waste_and_caliber = message.text
                test_qc(message)
            else:
                msg = bot.send_message(message.chat.id, wrong_input)
                waste_test_caliber(message)
        except ValueError:
            msg = bot.send_message(message.chat.id, wrong_input)
            waste_test_caliber(message)

########################################################################################
def test_qc(message):

    msg = bot.send_message(message.chat.id, "مجموع قهوه مورد استفاده برای تست و کنترل کیفی را با واحد گرم وارد کنید")
    bot.register_next_step_handler(msg, test_qc_input)

def test_qc_input(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        waste_test_caliber(message)
    else:
        global test_and_qc
        try:
            waste = int(message.text)
            if waste < 600 and waste >= 0 and waste <= (int(coffee_given) - int(coffee_remain) - int(waste_and_caliber)):

                test_and_qc = message.text
                desc_message(message)

            else:
                msg = bot.send_message(message.chat.id, wrong_input)
                test_qc(message)
        except ValueError:
            msg = bot.send_message(message.chat.id, wrong_input)
            test_qc(message)

########################################################################################
def brew_data(message):
    brew_waste_caliber(message)

########################################################################################
def brew_waste_caliber(message):

    msg = bot.send_message(message.chat.id, "مجموع ضایعات و قهوه مورد استفاده برای کالیبر خود را با واحد گرم وارد کنید")
    bot.register_next_step_handler(msg, brew_waste_caliber_input)

def brew_waste_caliber_input(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        coffee_in_validation(message)
    else:
        global waste_and_caliber
        try:
            waste = int(message.text)
            if waste < 600 and waste >= 0 and waste < (int(coffee_given) - int(coffee_remain)):
                waste_and_caliber = message.text
                brew_test_qc(message)
            else:
                msg = bot.send_message(message.chat.id, wrong_input)
                bot.register_next_step_handler(msg, brew_waste_caliber_input)

        except ValueError:
            msg = bot.send_message(message.chat.id, wrong_input)
            bot.register_next_step_handler(msg, brew_waste_caliber_input)

########################################################################################

def brew_test_qc(message):

    msg = bot.send_message(message.chat.id, "مجموع قهوه مورد استفاده برای تست و کنترل کیفی را با واحد گرم وارد کنید")
    bot.register_next_step_handler(msg, brew_test)

def brew_test(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        brew_waste_caliber(message)
    else:
        global test_and_qc
        try:
            qc = int(message.text)
            if qc < 600 and qc >= 0 and qc <= (int(coffee_given) - int(coffee_remain) - int(waste_and_caliber)):

                test_and_qc = message.text
                desc_message(message)
            else:
                msg = bot.send_message(message.chat.id, wrong_input)
                bot.register_next_step_handler(msg, brew_test)

        except ValueError:
            msg = bot.send_message(message.chat.id, wrong_input)
            bot.register_next_step_handler(msg, brew_test)

########################################################################################
def desc_message(message):


    # msg = bot.send_message(message.chat.id, "لطفا توضیحات مورد نیاز را وارد کنید، در غیر این صورت 'بعدی' را بزنید", reply_markup=telebot.types.ReplyKeyboardRemove())
    msg = bot.send_message(message.chat.id, "لطفا توضیحات مورد نیاز را وارد کنید، در غیر این صورت 'بعدی' را بزنید", reply_markup=next_markup)
    bot.register_next_step_handler(msg, desc_confirmed)

def desc_confirmed(message):
    global description_data
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        if section == "بار دمی":
            brew_test_qc(message)
        else:
            test_qc(message)
    else:

        desc = message.text

        if desc == "" or desc == "بعدی":
            description_data = None
        else:
            description_data = message.text
        message_handler(message)


def finale(message):

    global edit_menu_message

    global user_name
    global user_id
    global month_selected    
    global day_selected
    global branch
    global section
    global shift
    global roastery_name
    global coffee_line
    global coffee_given
    global coffee_remain

    global espresso_dosage
    global espresso_yield
    global espresso_temp
    global espresso_time

    global water_tds
    global waste_and_caliber
    global test_and_qc
    global description_data

    # time_now = jdatetime.datetime.now()
    # time_now = str(time_now)
    date_today = str(date.today())
    time_a = datetime.now()
    time_b = timedelta(minutes = 210)
    time_now = time_a + time_b
    time_now = str(time_now.time())
    # time_now = str(datetime.now())

    to_ordinal_day = int(day_selected)
    to_ordinal_month = int(month_dict[month_selected])
    # ordinal_date = convert_to_excel_ordinal(year, to_ordinal_month, to_ordinal_day)
    ordinal_date = jdatetime.date(year, to_ordinal_month, to_ordinal_day).togregorian()



# def insert_to_db(time_now:str, ordinal_date: int, month_selected:str, day_selected:int, branch:str, user_name:str, section:str, shift:str, roastery_name:str, coffee_line:str, coffee_given:int, coffee_remain:int, espresso_dosage:int, espresso_yield:int, espresso_temp:int, espresso_time:int, water_tds:int, waste_and_caliber:int, test_and_qc:int, description_data:str):





    if section.lower() == "بار دمی":
        cursor.execute('INSERT INTO checklist (date_of_insert, time_of_insert, date_ordinal, data_month, data_date, branch, user_name, user_id, section, shift, roastery_name, coffee_line, coffee_given, coffee_remain, waste_and_caliber, test_and_qc, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (date_today, time_now, ordinal_date, month_selected,  unidecode(day_selected), branch, user_name, user_id, section, shift, roastery_name, coffee_line, unidecode(coffee_given), unidecode(coffee_remain), waste_and_caliber, test_and_qc, description_data))
    
    else:
        cursor.execute('INSERT INTO checklist (date_of_insert, time_of_insert, date_ordinal, data_month, data_date, branch, user_name, user_id, section, shift, roastery_name, coffee_line, coffee_given, coffee_remain, espresso_dosage, espresso_yield, espresso_temp, espresso_time, water_tds, waste_and_caliber, test_and_qc, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (date_today, time_now, ordinal_date, month_selected,  unidecode(day_selected), branch, user_name, user_id, section, shift, roastery_name, coffee_line, unidecode(coffee_given), unidecode(coffee_remain), unidecode(espresso_dosage), unidecode(espresso_yield), unidecode(espresso_temp), unidecode(espresso_time), unidecode(water_tds), unidecode(waste_and_caliber), unidecode(test_and_qc), description_data))
    
    # if section.lower() == "بار دمی":
    #     cursor.execute('INSERT INTO checklist (date_of_insert, time_of_insert, date_ordinal, branch, user_name, section, shift, roastery_name, coffee_line, coffee_given, coffee_remain, waste_and_caliber, test_and_qc, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (date_today, time_now, ordinal_date, branch, user_name, section, shift, roastery_name, coffee_line, unidecode(coffee_given), unidecode(coffee_remain), waste_and_caliber, test_and_qc, description_data))
    
    # else:
    #     cursor.execute('INSERT INTO checklist (date_of_insert, time_of_insert, date_ordinal, branch, user_name, section, shift, roastery_name, coffee_line, coffee_given, coffee_remain, espresso_dosage, espresso_yield, espresso_temp, espresso_time, water_tds, waste_and_caliber, test_and_qc, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (date_today, time_now, ordinal_date, branch, user_name, section, shift, roastery_name, coffee_line, unidecode(coffee_given), unidecode(coffee_remain), unidecode(espresso_dosage), unidecode(espresso_yield), unidecode(espresso_temp), unidecode(espresso_time), unidecode(water_tds), unidecode(waste_and_caliber), unidecode(test_and_qc), description_data))
    
    
    conn.commit()



    # insert_to_db(time_now, ordinal_date, month_selected, unidecode(day_selected), branch, user_name, section, shift, roastery_name, coffee_line, unidecode(coffee_given), unidecode(coffee_remain), unidecode(espresso_dosage), unidecode(espresso_yield), unidecode(espresso_temp), unidecode(espresso_time), unidecode(water_tds), unidecode(waste_and_caliber), unidecode(test_and_qc), description_data)

    user_name = None
    user_id = None
    month_selected = None
    day_selected = None
    branch = None
    section = str()
    shift = None
    roastery_name = None
    coffee_line = None
    coffee_given = None
    coffee_remain = None
    espresso_dosage = None
    espresso_yield = None
    espresso_temp = None
    espresso_time = None
    water_tds = None
    waste_and_caliber = None
    test_and_qc = None
    description_data = None

    bot.send_message(message.chat.id, "اطلاعات ذخیره شد، برای ورود رکورد جدید از /start استفاده کنید")
    hide_menu(message)

########################################################################################

def branch_edit(message):
    msg = bot.send_message(message.chat.id, "اصلاح شعبه", reply_markup=branch_markup)
    bot.register_next_step_handler(msg, branch_editing)

def branch_editing(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        message_handler(message)
    else:
        if message.text.lower() not in branches:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            bot.register_next_step_handler(msg, start)
        else:

            global branch
            branch = message.text
        branch_edited(message)

def branch_edited(message):
    message_handler(message)
########################################################################################
def day_edit(message):
    msg = bot.send_message(message.chat.id, "اصلاح روز", reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, day_editing)

def day_editing(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        message_handler(message)
    else:
        global day_selected
        if month_selected in month_31:
            try:
                day_input = int(message.text)
                if day_input > 31 or day_input < 1:
                    msg = bot.reply_to(message, "ماه نهایتا 31 روز دارد!")
                    bot.register_next_step_handler(msg, day_editing)
                else:
                    day_selected = message.text
                    # day_assurance (message)
                    day_edited(message)
            except ValueError:
                msg = bot.reply_to(message, "ورودی غیر مجاز")
                # bot.register_next_step_handler(msg, day_validation)
                bot.register_next_step_handler(msg, day_editing)


        elif month_selected in month_30:
            try:
                day_input = int(message.text)
                if day_input > 30 or day_input < 1:
                    msg = bot.reply_to(message, "ماه انتخابی شما 30 روز دارد")
                    bot.register_next_step_handler(msg, day_editing)
                else:
                    day_selected = message.text
                    # day_assurance (message)
                    day_edited(message)
            except ValueError:
                msg = bot.reply_to(message, "ورودی غیر مجاز")
                # bot.register_next_step_handler(msg, day_validation)
                bot.register_next_step_handler(msg, day_editing)
        elif month_selected in month_29:
            try:
                day_input = int(message.text)
                if day_input > 29 or day_input < 1:
                    msg = bot.reply_to(message, "اسفند 29 روز دارد")
                    bot.register_next_step_handler(msg, day_editing)
                else:
                    day_selected = message.text
                    # day_assurance (message)
                    day_edited(message)
            except ValueError:
                msg = bot.reply_to(message, "ورودی غیر مجاز")
                # bot.register_next_step_handler(msg, day_validation)
                bot.register_next_step_handler(msg, day_editing)

        else:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            # bot.register_next_step_handler(msg, day_validation)
            bot.register_next_step_handler(msg, day_editing)

def day_edited(message):
    message_handler(message)
########################################################################################
def month_edit(message):
    msg = bot.send_message(message.chat.id, "اصلاح ماه", reply_markup=month_markup)
    bot.register_next_step_handler(msg, month_editing)

def month_editing(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        message_handler(message)
    else:
        if message.text.lower() not in month:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            month_edit(message)
        else:
            global month_selected
            month_selected = message.text
            month_edited(message)

def month_edited(message):
    message_handler(message)
########################################################################################
def roastery_edit(message):
    msg = bot.send_message(message.chat.id, "اصلاح روستری", reply_markup=roastery_markup)
    bot.register_next_step_handler(msg, roastery_editing)

def roastery_editing(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        message_handler(message)
    else:
        global roastery_name
        if message.text.lower() in roastery:
            if message.text.lower() == "tds":
                roastery_name = message.text
                tds_roastery_edit(message)
            elif message.text.lower() == "moa":
                roastery_name = message.text
                moa_roastery_edit(message)
            
            elif message.text.lower() == "dam":
                roastery_name = message.text
                dam_roastery_edit(message)

            else:
                msg = bot.send_message(message.chat.id, "گزینه انتخاب شده فعلا موجود نمیباشد")
                roastery_edit(message)
        else:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            roastery_edit(message)

########################################################################################

def tds_roastery_edit(message):
    msg = bot.send_message(message.chat.id, "اصلاح لاین", reply_markup=tds_markup)
    bot.register_next_step_handler(msg, edit_tds_sure)


def moa_roastery_edit(message):
    msg = bot.send_message(message.chat.id, "اصلاح لاین", reply_markup=moa_markup)
    bot.register_next_step_handler(msg, edit_moa_sure)

def dam_roastery_edit(message):
    msg = bot.send_message(message.chat.id, "اصلاح لاین", reply_markup=dam_markup)
    bot.register_next_step_handler(msg, edit_dam_sure)

def edit_dam_sure(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        roastery_edit(message)
    else:
        global coffee_line
        if roastery_name.lower() == "dam":
            if message.text.lower() in dam_lines:
                coffee_line = message.text
                message_handler(message)
            else:
                msg = bot.send_message(msg, incorrect_format)
                dam_roastery_edit(message)
        else:
            msg = bot.send_message(msg, incorrect_format)
            dam_roastery_edit(message)
        
def edit_tds_sure(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        roastery_edit(message)
    else:
        global coffee_line
        if roastery_name.lower() == "tds":
            if message.text.lower() in tds_lines:
                coffee_line = message.text
                message_handler(message)
            else:
                msg = bot.send_message(msg, incorrect_format)
                tds_roastery_edit(message)
        else:
            msg = bot.send_message(msg, incorrect_format)
            tds_roastery_edit(message)

def edit_moa_sure(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        roastery_edit(message)
    else:
        global coffee_line
        if roastery_name.lower() == "moa":
            if message.text.lower() in moa_lines:
                coffee_line = message.text
                message_handler(message)
            else:
                msg = bot.send_message(msg, incorrect_format)
                moa_roastery_edit(message)
        else:
            msg = bot.send_message(msg, incorrect_format)
            moa_roastery_edit(message)

########################################################################################

def shift_edit(message):
    msg = bot.send_message(message.chat.id, "اصلاح شیفت", reply_markup=shifts_markup)
    bot.register_next_step_handler(msg, shift_editing)

def shift_editing(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        message_handler(message)
    else:
        if message.text.lower() in shifts:
            global shift
            shift = message.text
            # shift_assurance(message)
            shift_edited(message)
        else:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            bot.register_next_step_handler(msg, shift_edited)

def shift_edited(message):
    message_handler(message)
########################################################################################
def section_edit(message):
    msg = bot.send_message(message.chat.id, "اصلاح سکشن", reply_markup=section_markup)
    bot.register_next_step_handler(msg, section_editing)

def section_editing(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        message_handler(message)
    else:
        if message.text.lower() not in sections:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            section_edit(message)
        else:
            global section
            section = message.text

            section_edited(message)

def section_edited(message):
    message_handler(message)
########################################################################################
def coffee_remain_edit(message):
    msg = bot.send_message(message.chat.id, "اصلاح قهوه باقی مانده")
    bot.register_next_step_handler(msg, coffee_remain_editing)

def coffee_remain_editing(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        message_handler(message)
    else:

        global coffee_remain
        if message.text.isdigit():
            if int(message.text) > int(coffee_given):
                msg = bot.send_message(message.chat.id, wrong_input)
                coffee_remain_edit(message)
            else:
                coffee_remain = message.text
                coffee_remain_edited(message)
        else: 
            msg = bot.send_message(message.chat.id, wrong_input)
            coffee_remain_edit(message)

def coffee_remain_edited(message):
    message_handler(message)
########################################################################################
def coffee_in_edit(message):

    msg = bot.send_message(message.chat.id, "اصلاح قهوه تحویلی", reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, coffee_in_editing)
def coffee_in_editing(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        message_handler(message)
    else:
    
        if message.text.isdigit():
            global coffee_given
            if int(message.text) > 100000 or int(message.text) < 0:
                msg = bot.send_message(message.chat.id, wrong_input)
                coffee_in_edit(message)
            else:
                coffee_given = message.text
                coffee_in_edited(message)
        else: 
            msg = bot.send_message(message.chat.id, "لطفا مقدار عددی وارد کنید")
            coffee_in_edit(message)

def coffee_in_edited(message):
    message_handler(message)
########################################################################################
def esp_temp_edit(message):
    msg = bot.send_message(message.chat.id, "اصلاح دمای عصاره گیری")
    bot.register_next_step_handler(msg, esp_temp_editing)

def esp_temp_editing(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        message_handler(message)
    else:

        global espresso_temp
        try:
            temp = float(message.text)
            if temp > 95 or temp < 88:
                msg = bot.send_message(message.chat.id, wrong_input)
                esp_temp_edit(message)
            else:
                espresso_temp = message.text
                esp_temp_edited(message)

        except ValueError:
            msg = bot.send_message(message.chat.id, wrong_input)
            esp_temp_edit(message)

def esp_temp_edited(message):
    message_handler(message)

########################################################################################
def esp_yield_edit(message):    
    msg = bot.send_message(message.chat.id, "اصلاح خروجی اسپرسو")
    bot.register_next_step_handler(msg, esp_yield_editing)

def esp_yield_editing(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        message_handler(message)
    else:
   
        global espresso_yield
        try:
            dose = float(message.text)
            if dose > 60 or dose < 20:
                msg = bot.send_message(message.chat.id, wrong_input)
                esp_yield_edit(message)
            else:
                espresso_yield = message.text
                esp_yield_edited(message)

        except ValueError:
            msg = bot.send_message(message.chat.id, wrong_input)
            esp_yield_edit(message)

def esp_yield_edited(message):
    message_handler(message)
########################################################################################
def esp_caliber_edit(message):
    msg = bot.send_message(message.chat.id, "اصلاح کالیبر")
    bot.register_next_step_handler(msg, esp_caliber_editing)

def esp_caliber_editing(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        message_handler(message)
    else:

        global espresso_dosage
        try:
            dose = float(message.text)
            if dose > 24 or dose < 17:
                msg = bot.send_message(message.chat.id, wrong_input)
                esp_caliber_edit(message)
            else:
                espresso_dosage = message.text
                esp_caliber_edited(message)

        except ValueError:
            msg = bot.send_message(message.chat.id, wrong_input)
            esp_caliber_edit()

def esp_caliber_edited(message):
    message_handler(message)
########################################################################################
def waste_edit(message):
    msg = bot.send_message(message.chat.id, "اصلاح ضایعات")
    bot.register_next_step_handler(msg, waste_editing)

def waste_editing(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        message_handler(message)
    else:
        global waste_and_caliber
        try:
            waste = int(message.text)
            if waste < 600 and waste >= 0 and waste <= (int(coffee_given) - int(coffee_remain)):
                waste_and_caliber = message.text
                waste_edited(message)
            else:
                msg = bot.send_message(message.chat.id, wrong_input)
                waste_editing(message)
        except ValueError:
            msg = bot.send_message(message.chat.id, wrong_input)
            waste_editing(message)


def waste_edited(message):
    message_handler(message)
########################################################################################
def water_tds_edit(message):
    msg = bot.send_message(message.chat.id, "اصلاح TDS آب", reply_markup=back_markup)
    bot.register_next_step_handler(msg, water_tds_editing)

def water_tds_editing(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        message_handler(message)
    else:
        global water_tds
        try:
            tds = message.text
            if tds.isdigit():
                if int(tds) > 500 or int(tds) < 5:
                    msg = bot.send_message(message.chat.id, wrong_input)          
                    water_tds_edit(message)
                else:
                    water_tds = int(tds)
                    water_tds_edited(message)
            elif tds == "بازگشت":
                water_tds = None
                water_tds_edited(message)
            else:
                msg = bot.send_message(message.chat.id, wrong_input)          
                water_tds_edit(message)

        except ValueError:
                msg = bot.send_message(message.chat.id, wrong_input)          
                water_tds_edit    (message)


def water_tds_edited(message):
    message_handler(message)    
########################################################################################

def esp_time_edit(message):
    msg = bot.send_message(message.chat.id, "اصلاح زمان عصاره گیری")
    bot.register_next_step_handler(msg, esp_time_editing)

def esp_time_editing(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        message_handler(message)
    else:
        global espresso_time
        try:
            temp = float(message.text)
            if temp > 80 or temp < 10:
                msg = bot.send_message(message.chat.id, wrong_input)
                esp_time_edit(message)
            else:
                espresso_time = message.text
                esp_time_edited(message)

        except ValueError:
            msg = bot.send_message(message.chat.id, wrong_input)
            esp_time_edit(message)

def esp_time_edited(message):
    message_handler(message)
########################################################################################
def qc_test_edit(message):
    msg = bot.send_message(message.chat.id, "اصلاح قهوه تست و کنترل کیفی")
    bot.register_next_step_handler(msg, qc_test_editing)
    
def qc_test_editing(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        message_handler(message)
    else:
        global test_and_qc
        try:
            waste = int(message.text)
            if waste < 600 and waste >= 0 and waste <= (int(coffee_given) - int(coffee_remain) - int(waste_and_caliber)):

                test_and_qc = message.text
                qc_test_edited(message)

            else:
                msg = bot.send_message(message.chat.id, wrong_input)
                qc_test_edit(message)
        except ValueError:
            msg = bot.send_message(message.chat.id, wrong_input)
            qc_test_edit(message)


def qc_test_edited(message):
    message_handler(message)
########################################################################################
def description_edit(message):
    msg = bot.send_message(message.chat.id, "اصلاح توضیحات", reply_markup=back_markup)
    bot.register_next_step_handler(msg, description_editing)
    
def description_editing(message):
    global description_data
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        message_handler(message)
    elif message.text.lower() == "بازگشت":
        description_data = None
        message_handler(message)
    else:
    
        description_data = message.text
        description_edited(message)

def description_edited(message):
    message_handler(message)
########################################################################################

edit_menu_message = None
agree_markup = None

@bot.message_handler(commands=["submit"])
def submit(message):
    finale(message)

def message_handler(message):
    global edit_menu_message
    global agree_markup

    global month_selected    
    global day_selected
    global branch
    global section
    global shift
    global roastery_name
    global coffee_line
    global coffee_given
    global coffee_remain

    global espresso_dosage
    global espresso_yield
    global espresso_temp
    global espresso_time

    global water_tds
    global waste_and_caliber
    global test_and_qc
    global description_data
    
    month_selected= str(month_selected)
    day_selected= str(day_selected)
    branch = str(branch)
    section = str(section)
    shift = str(shift)
    roastery_name = str(roastery_name)
    coffee_line = str(coffee_line)
    coffee_given = str(coffee_given)
    coffee_remain = str(coffee_remain)
    espresso_dosage = str(espresso_dosage)
    espresso_yield = str(espresso_yield)
    espresso_temp = str(espresso_temp)
    espresso_time = str(espresso_time)
    water_tds = str(water_tds)
    waste_and_caliber = str(waste_and_caliber)
    test_and_qc = str(test_and_qc)
    description_data = str(description_data)

    if agree_markup != True:

        if section.lower() == "بار دمی": 
            agree_markup = InlineKeyboardMarkup()
            agree_markup.row_width = 3
            agree_markup.add(
            InlineKeyboardButton("شعبه", callback_data = "cb_branch"),
            InlineKeyboardButton("روز", callback_data="cb_day"),
            InlineKeyboardButton("ماه", callback_data="cb_month"),        
            InlineKeyboardButton("روستری و لاین قهوه", callback_data = "cb_roastery"),    
            InlineKeyboardButton("شیفت", callback_data="cb_shift"),    
            InlineKeyboardButton("سکشن", callback_data="cb_section"),        
            InlineKeyboardButton("قهوه باقی مانده", callback_data="cb_remain"),
            InlineKeyboardButton("قهوه تحویلی", callback_data="cb_coffee_in"),           
            # InlineKeyboardButton("لاین قهوه", callback_data = "cb_coffee_line"),    
            InlineKeyboardButton("دورریز", callback_data = "cb_waste"),
            InlineKeyboardButton("کنترل کیفی", callback_data="cb_qc"),    
            InlineKeyboardButton("توضیحات", callback_data = "cb_desc"),
            InlineKeyboardButton("لغو عملیات", callback_data = "cb_cancel")
        )
            espresso_dosage = None
            espresso_yield = None
            espresso_temp = None
            espresso_time = None

        else:
            agree_markup = InlineKeyboardMarkup()
            agree_markup.row_width = 3
            agree_markup.add(
            InlineKeyboardButton("شعبه", callback_data = "cb_branch"),
            InlineKeyboardButton("روز", callback_data="cb_day"),
            InlineKeyboardButton("ماه", callback_data="cb_month"),        
            InlineKeyboardButton("روستری و لاین قهوه", callback_data = "cb_roastery"),    
            InlineKeyboardButton("شیفت", callback_data="cb_shift"),    
            InlineKeyboardButton("سکشن", callback_data="cb_section"),        
            InlineKeyboardButton("قهوه باقی مانده", callback_data="cb_remain"),
            InlineKeyboardButton("قهوه تحویلی", callback_data="cb_coffee_in"),           
            # InlineKeyboardButton("لاین قهوه", callback_data = "cb_coffee_line"),    
            InlineKeyboardButton("دمای عصاره گیری", callback_data = "cb_esp_temp"),
            InlineKeyboardButton("خروجی اسپرسو", callback_data="cb_yield"),    
            InlineKeyboardButton("کالیبر", callback_data = "cb_caliber"),    
            InlineKeyboardButton("آب TDS", callback_data = "cb_water_tds"),
            InlineKeyboardButton("زمان عصاره گیری", callback_data="cb_esp_time"),       
            InlineKeyboardButton("کنترل کیفی", callback_data="cb_qc"),    
            InlineKeyboardButton("دورریز", callback_data = "cb_waste"),
            InlineKeyboardButton("توضیحات", callback_data = "cb_desc"),
            InlineKeyboardButton("لغو عملیات", callback_data = "cb_cancel")
            )

    else:
        pass


    if section.lower() == "بار دمی": 
        final_message = "ماه:" + month_selected +"\n" +"روز:" + day_selected + "\n" +"شعبه:" + branch +"\n" +"سکشن:" + section + "\n" +"شیفت:" + shift + "\n" +"روستری:" + roastery_name + "\n" +"لاین:" + coffee_line + "\n" +"قهوه تحویلی:" + coffee_given + "\n" +"قهوه باقی مانده:" + coffee_remain + "\n" +"دورریز:" + waste_and_caliber + "\n" +"کنترل کیفی:" + test_and_qc + "\n" +"توضیحات: " + description_data + "\n" + "در صورت نیاز به تغییر هر یک از اطلاعات از کلیدهای زیر استفاده کنید، در غیر اینصورت /submit را بزنید. در صورتی که مایل به حذف اطلاعات وارد شده هستید /restart را بزنید."
    else:
        final_message = "ماه:" + month_selected +"\n" +"روز:" + day_selected + "\n" +"شعبه:" + branch +"\n" +"سکشن:" + section + "\n" +"شیفت:" + shift + "\n" +"روستری:" + roastery_name + "\n" +"لاین:" + coffee_line + "\n" +"قهوه تحویلی:" + coffee_given + "\n" +"قهوه باقی مانده:" + coffee_remain + "\n" + "کالیبر اسپرسو" + espresso_dosage + "\n" + "خروجی اسپرسو" + espresso_yield +"\n" + "دمای عصاره گیری" + espresso_temp +"\n" + "زمان عصاره گیری" + espresso_time + "\n" +"تی دی اس آب:" + water_tds + "\n" +"دورریز:" + waste_and_caliber + "\n" +"کنترل کیفی:" + test_and_qc + "\n" +"توضیحات:" + description_data + "\n" + "در صورت نیاز به تغییر هر یک از اطلاعات از کلیدهای زیر استفاده کنید، در غیر اینصورت /submit را بزنید. در صورتی که مایل به حذف اطلاعات وارد شده هستید /restart را بزنید."

    edit_menu_message = bot.send_message(message.chat.id, final_message, reply_markup=agree_markup)

@bot.callback_query_handler(func=lambda call: True)

def callback_query(call):

    if call.data == "cb_branch":
        hide_menu(call.message)
        branch_edit(call.message)
        
    elif call.data == "cb_day":
        hide_menu(call.message)
        day_edit(call.message)

    elif call.data == "cb_month":
        hide_menu(call.message)
        month_edit(call.message)

    elif call.data == "cb_roastery":
        hide_menu(call.message)
        roastery_edit(call.message)

    elif call.data == "cb_shift":
        hide_menu(call.message)
        shift_edit(call.message)

    elif call.data == "cb_section":
        hide_menu(call.message)
        section_edit(call.message)

    elif call.data == "cb_remain":
        hide_menu(call.message)
        coffee_remain_edit(call.message)

    elif call.data == "cb_coffee_in":
        hide_menu(call.message)
        coffee_in_edit(call.message)

    elif call.data == "cb_coffee_line":
        hide_menu(call.message)
        coffee_line_edit(call.message)

    elif call.data == "cb_caliber":
        hide_menu(call.message)
        esp_caliber_edit(call.message)

    elif call.data == "cb_esp_time":
        hide_menu(call.message)
        esp_time_edit(call.message)

    elif call.data == "cb_esp_temp":
        hide_menu(call.message)
        esp_temp_edit(call.message)

    elif call.data == "cb_yield":
        hide_menu(call.message)
        esp_yield_edit(call.message)

    elif call.data == "cb_water_tds":
        hide_menu(call.message)
        water_tds_edit(call.message)

    elif call.data == "cb_qc":
        hide_menu(call.message)
        qc_test_edit(call.message)

    elif call.data == "cb_waste":
        hide_menu(call.message)
        waste_edit(call.message)

    elif call.data == "cb_desc":
        hide_menu(call.message)
        description_edit(call.message)
    
    elif call.data == "cb_cancel":
        hide_menu(call.message)
        cancel(call.message)

    else:
        pass

def hide_menu(message):
    bot.delete_message(message.chat.id, edit_menu_message.message_id)

def cancel (message):
    global edit_menu_message
    global agree_markup
    global user_name
    global user_id
    global month_selected    
    global day_selected
    global branch
    global section
    global shift
    global roastery_name
    global coffee_line
    global coffee_given
    global coffee_remain

    global espresso_dosage
    global espresso_yield
    global espresso_temp
    global espresso_time

    global water_tds
    global waste_and_caliber
    global test_and_qc
    global description_data

    user_name = None
    user_id = None
    edit_menu_message = None
    agree_markup = None
    month_selected = None
    day_selected = None
    branch = None
    section = None
    shift = None
    roastery_name = None
    coffee_line = None
    coffee_given = None
    coffee_remain = None
    espresso_dosage = None
    espresso_yield = None
    espresso_temp = None
    espresso_time = None
    water_tds = None
    waste_and_caliber = None
    test_and_qc = None
    description_data = None
    
    bot.send_message(message.chat.id, "عملیات لغو شد، برای شروع مجدد /start را بزنید", reply_markup=telebot.types.ReplyKeyboardRemove())

@bot.message_handler(commands=['restart'])
def restart(message):
    hide_menu(message)
    global edit_menu_message
    global agree_markup
    global user_name
    global user_id
    global month_selected    
    global day_selected
    global branch
    global section
    global shift
    global roastery_name
    global coffee_line
    global coffee_given
    global coffee_remain

    global espresso_dosage
    global espresso_yield
    global espresso_temp
    global espresso_time

    global water_tds
    global waste_and_caliber
    global test_and_qc
    global description_data

    user_name = None
    user_id = None
    edit_menu_message = None
    agree_markup = None
    month_selected = None
    day_selected = None
    branch = None
    section = None
    shift = None
    roastery_name = None
    coffee_line = None
    coffee_given = None
    coffee_remain = None
    espresso_dosage = None
    espresso_yield = None
    espresso_temp = None
    espresso_time = None
    water_tds = None
    waste_and_caliber = None
    test_and_qc = None
    description_data = None
    
    start(message)
bot.infinity_polling()
