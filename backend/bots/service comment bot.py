import sqlite3
import jdatetime
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from persiantools.jdatetime import JalaliDate
from datetime import datetime, date, timezone, timedelta
from functools import wraps
from unidecode import unidecode


# frz test bot token: 1163491358:AAFsn2EW38nMpLI_vlPKelmTEvO9N-fDQ0o
# comments bot token: 6402890011:AAGwC_XBRYNWKAjZ9gqHvp76TCXxsf3BIAQ
bot = telebot.TeleBot("6402890011:AAGwC_XBRYNWKAjZ9gqHvp76TCXxsf3BIAQ")

# weekdays:
weekday_dict = {
"0" : "دوشنبه" ,
"1" : "سه شنبه" ,
"2" : "چهارشنبه" ,
"3" : "پنج شنبه" ,
"4" : "جمعه" ,
"5" : "شنبه" ,
"6" : "یکشنبه"
}

# conn = sqlite3.connect('database_2.db', check_same_thread=False)
# cursor = conn.cursor()
# cursor.execute('''CREATE TABLE IF NOT EXISTS comments(
#     "id"    INTEGER NOT NULL PRIMARY KEY,
#     "date_of_insert"    TEXT NOT NULL,
#     "time_of_insert"  TEXT NOT NULL,
#     "user_name"    TEXT NOT NULL,
#     "user_id"    INTEGER NOT NULL,
#     "ordinal_date"    TEXT NOT NULL,

#     "branch"    TEXT NOT NULL,
#     "shift"    TEXT NOT NULL,
#     "comment_type"    TEXT NOT NULL,
#     "comment"    TEXT NOT NULL,
#     "related_section"    TEXT NOT NULL,
#     "receipt_number"    TEXT,
#     "description"    TEXT
#     );
#     ''')

conn = sqlite3.connect('database_2.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS comments(
    "id"    INTEGER NOT NULL PRIMARY KEY,
    "date_of_insert"    TEXT NOT NULL,
    "time_of_insert"  TEXT NOT NULL,
    "user_name"    TEXT NOT NULL,
    "user_id"    INTEGER NOT NULL,
    "ordinal_date"    TEXT NOT NULL,
    "month_selected"   TEXT NOT NULL,
    "day_selected"    INTEGER NOT NULL,
    "branch"    TEXT NOT NULL,
    "shift"    TEXT NOT NULL,
    "comment_type"    TEXT NOT NULL,
    "comment"    TEXT NOT NULL,
    "related_section"    TEXT NOT NULL,
    "receipt_number"    TEXT,
    "description"    TEXT
    );
    ''')
date_of_insert = None
time_of_insert = None
user_name = None
user_id = None
ordinal_date = None
month_selected = None
day_selected = None
branch = None
shift = None
comment_type = None
comment = None
related_section = None
receipt_number = None
description = None
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
shifts_markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
shifts_markup.add("عصر", "صبح")
shifts = ["عصر", "صبح"]
########################################################################################
pos_neg_markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
pos_neg_markup.add("منفی", "مثبت")
pos_neg_list = ["منفی", "مثبت"]
########################################################################################
back_markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
back_markup.add("بازگشت")
########################################################################################
next_markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
next_markup.add("بعدی")
########################################################################################
section_markup = types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True, resize_keyboard=True)
section_markup.add("بار", "سالن", "بیکری", "پیستری", "آشپزخانه", "بار/سالن", "آشپزخانه/سالن", "بیکری/سالن", "پیستری/سالن", "آشپزخانه/بیکری", "آشپزخانه/بار", "انبار مرکزی", "مدیریت", "مارکتینگ")
section_list = ["بار", "سالن", "بیکری", "پیستری", "آشپزخانه", "بار/سالن", "آشپزخانه/سالن", "بیکری/سالن", "پیستری/سالن", "آشپزخانه/بیکری", "آشپزخانه/بار", "انبار مرکزی", "مدیریت", "مارکتینگ"]

########################################################################################
incorrect_format = "لطفا اطلاعات را با فرمت درست وارد کنید"
########################################################################################
submit_text = " در صورتی که از صحت اطلاعات وارد شده مطمئن هستید از /submit و در غیر این صورت برای شروع مجدد از /restart استفاده کنید"

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
    known_usernames = ["Fuadrn", "Azerila101", "Dourriz", "Hematsogol", "timakhosravi", "Bd_moh", "kimiazangene", "Itsmehrabb", "lshayshayshayanl", "Amirremon", "Ma_ry_am_sh", "mehghsa", "Parzzaa", "mar_1am77", "masodyan", "Fuadgoftbesazam"]

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
    # message.from_user.id
    # message.from_user.first_name
    # message.from_user.last_name
    # message.from_user.username

    msg = bot.send_message(message.chat.id, "انتخاب ماه", reply_markup=month_markup)
    bot.register_next_step_handler(msg, month_validation)

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

########################################################################################################################
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
########################################################################################

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
            shift_choose(message)
########################################################################################

def shift_choose(message):
    msg = bot.send_message(message.chat.id, "انتخاب شیفت", reply_markup=shifts_markup)
    bot.register_next_step_handler(msg, shift_validation)

########################################################################################
def shift_validation(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        branch_selection(message)
    else:
        if message.text.lower() in shifts:
            global shift
            shift = message.text
            # shift_select(message)
            comment_type_input(message)
        else:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            bot.register_next_step_handler(msg, shift_validation)
########################################################################################

def comment_type_input(message):
    msg = bot.send_message(message.chat.id, "انتخاب نوع نظر", reply_markup=pos_neg_markup)
    bot.register_next_step_handler(msg, comment_type_validation)

def comment_type_validation(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        shift_choose(message)
    else:
        if message.text.lower() in pos_neg_list:
            global comment_type
            comment_type = message.text.lower()

            comment_input(message)
        else:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            bot.register_next_step_handler(msg, comment_type_input)
########################################################################################

def comment_input(message):
    msg = bot.send_message(message.chat.id, "لطفا متن نظر را وارد کنید", reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, comment_assignment)

def comment_assignment(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        comment_type_input(message)
    else:
        global comment
        comment = message.text
        responsible_section_message(message)
########################################################################################

def responsible_section_message(message):
    msg = bot.send_message(message.chat.id, "انتخاب سکشن مربوطه", reply_markup=section_markup)
    bot.register_next_step_handler(msg, responsible_section_input)

def responsible_section_input(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        comment_input(message)
    else:
        if message.text.lower() in section_list:
            global related_section
            related_section = message.text.lower()

            receipt_number_message(message)
        else:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            bot.register_next_step_handler(msg, responsible_section_input)
########################################################################################
def receipt_number_message(message):
    msg = bot.send_message(message.chat.id, "لطفا شماره فاکتور را وارد کنید، در غیر این صورت 'بعدی' را انتخاب کنید", reply_markup=next_markup)
    bot.register_next_step_handler(msg, receipt_number_input)

def receipt_number_input(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        responsible_section_message(message)
    else:
        global receipt_number
        try:
            receipt = message.text
            if receipt.isdigit() == True:
                receipt = int(receipt)
                if receipt > 99999 or receipt < 1:
                    msg = bot.reply_to(message, "مقدار وارد شده صحیح نیست")
                    bot.register_next_step_handler(msg, receipt_number_input)
                else:
                    receipt_number = message.text
                    description_input(message)
            elif receipt == "بعدی":
                receipt_number = None
                description_input(message)
            else:
                msg = bot.reply_to(message, "ورودی غیر مجاز")
                bot.register_next_step_handler(msg, receipt_number_input)
        except ValueError:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            bot.register_next_step_handler(msg, receipt_number_input)


########################################################################################

def description_input(message):
    msg = bot.send_message(message.chat.id, "لطفا توضیحات مورد نیاز را وارد کنید", reply_markup=next_markup)
    bot.register_next_step_handler(msg, description_assignment)

def description_assignment(message):
    global description
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        receipt_number_message(message)
    else:
        desc = message.text.lower()
        if desc == "" or desc == "بعدی":
            description = None
        else:
            description = message.text

        edit_menu(message)

########################################################################################

def finale (message):

    global date_of_insert
    global time_of_insert
    global user_name
    global user_id
    global ordinal_date
    global month_selected
    global day_selected
    global branch
    global shift
    global comment_type
    global comment
    global related_section
    global receipt_number
    global description

    date_of_insert = str(date.today())

    time_a = datetime.now()
    time_b = timedelta(minutes = 210)
    time_of_insert = time_a + time_b
    time_of_insert = str(time_of_insert.time())

    to_ordinal_day = int(day_selected)
    to_ordinal_month = int(month_dict[month_selected])

    ordinal_date = jdatetime.date(year, to_ordinal_month, to_ordinal_day).togregorian()


    weekday_int = str(datetime.weekday(date.today()))
    # weekday_int = str(weekday_int)

    if weekday_int in weekday_dict.keys():
        day_of_week = weekday_dict[weekday_int]
            




    if receipt_number == None:
        cursor.execute("INSERT INTO comments (date_of_insert, time_of_insert, user_name, user_id, ordinal_date, month_selected, day_selected,  branch, shift, comment_type, comment, related_section, description) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (date_of_insert, time_of_insert, user_name, user_id, ordinal_date, month_selected, unidecode(day_selected), branch, shift, comment_type, comment, related_section, description))




    else:

        cursor.execute("INSERT INTO comments (date_of_insert, time_of_insert, user_name, user_id, ordinal_date, month_selected, day_selected, branch, shift, comment_type, comment, related_section, receipt_number, description) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (date_of_insert, time_of_insert, user_name, user_id, ordinal_date, month_selected, unidecode(day_selected), branch, shift, comment_type, comment, related_section, unidecode(receipt_number), description))
    
    text_for_azerila = shift + " " + day_of_week + " " + str(unidecode(day_selected)) + " " + month_selected + "\n" + "شعبه " + branch + "\n" + related_section + " - " + comment_type + " - " + user_name + "\n" + "نظر: " + comment + "\n" + "توضیحات: " + description


    bot.send_message(978997945, text_for_azerila)
    bot.send_message(85607859, text_for_azerila)

    date_of_insert = None
    time_of_insert = None
    user_name = None
    user_id = None
    ordinal_date = None
    month_selected = None
    day_selected = None
    branch = None
    shift = None
    comment_type = None
    comment = None
    related_section = None
    receipt_number = None
    description = None

    conn.commit()

    bot.send_message(message.chat.id, "اطلاعات ذخیره شد، برای ورود رکورد جدید از /start استفاده کنید")
    hide_menu(message)

########################################################################################

def edit_menu(message):

    global edit_menu_message

    global month_selected
    global day_selected
    global branch
    global shift
    global comment_type
    global comment
    global related_section
    global receipt_number
    global description

    description = str(description)

    agree_markup = InlineKeyboardMarkup()
    agree_markup.row_width = 3
    agree_markup.add(
    InlineKeyboardButton("شعبه", callback_data = "cb_branch"),
    # InlineKeyboardButton("روز", callback_data="cb_day"),
    InlineKeyboardButton("ماه", callback_data="cb_month"),
    InlineKeyboardButton("نظر", callback_data="cb_comment"),
    InlineKeyboardButton("نوع نظر", callback_data="cb_com_type"),
    InlineKeyboardButton("شیفت", callback_data="cb_shift"),
    InlineKeyboardButton("توضیحات", callback_data="cb_desc"),
    InlineKeyboardButton("سکشن مربوطه", callback_data = "cb_section"),
    InlineKeyboardButton("شماره فاکتور", callback_data = "cb_receipt"),
    InlineKeyboardButton("لغو عملیات", callback_data = "cb_cancel")
    )

    if receipt_number != None:

        final_message = "ماه: " + month_selected + "\n" + "روز: " + day_selected + "\n" + "شعبه: " + branch + "\n" + "شیفت: " + shift + "\n" + "نوع نظر: " + comment_type + "\n" + "نظر: " + comment + "\n" + "شماره فاکتور: " + receipt_number + "\n" + "سکشن مربوطه: " + related_section + "\n" + "توضیحات: " + description + "\n \n"+ submit_text
    else:
        final_message = "ماه: " + month_selected + "\n" + "روز: " + day_selected + "\n" + "شعبه: " + branch + "\n" + "شیفت: " + shift + "\n" + "نوع نظر: " + comment_type + "\n" + "نظر: " + comment + "\n" + "شماره فاکتور: " + "-" + "\n" + "سکشن مربوطه: " + related_section + "\n" + "توضیحات: " + description + "\n \n"+ submit_text

    edit_menu_message = bot.send_message(message.chat.id, final_message, reply_markup=agree_markup)
########################################################################################

     
########################################################################################
@bot.message_handler(commands=["submit"])
def submit(message):
    finale(message)
########################################################################################


def branch_edit (message):
    msg = bot.send_message(message.chat.id, "انتخاب شعبه", reply_markup=branch_markup)
    bot.register_next_step_handler(msg, branch_editing)

def branch_editing(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        edit_menu(message)
    else:
        if message.text.lower() not in branches:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            branch_editing(message)
        else:

            global branch
            branch = message.text
            branch_edited(message)

def branch_edited(message):
    edit_menu(message)

########################################################################################
def day_edit (message):
    msg = bot.send_message(message.chat.id, "روز را وارد کنید", reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, day_editing)

def day_editing(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        month_edit(message)
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
    edit_menu(message)

########################################################################################
def month_edit (message):
    msg = bot.send_message(message.chat.id, "انتخاب ماه", reply_markup=month_markup)
    bot.register_next_step_handler(msg, month_editing)

def month_editing(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        edit_menu(message)
    else:
        if message.text.lower() not in month:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            bot.register_next_step_handler(msg, month_editing)
        else:
            global month_selected
            month_selected = message.text
            day_edit (message)

########################################################################################

def comment_edit (message):
    msg = bot.send_message(message.chat.id, "لطفا متن نظر را وارد کنید", reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, comment_editing)

def comment_editing(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        edit_menu(message)
    else:
        global comment
        comment = message.text
        comment_edited(message)

def comment_edited(message):
    edit_menu(message)
########################################################################################

def comment_type_edit (message):
    msg = bot.send_message(message.chat.id, "انتخاب نوع نظر", reply_markup=pos_neg_markup)
    bot.register_next_step_handler(msg, comment_type_editing)

def comment_type_editing(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        edit_menu(message)
    else:
        if message.text.lower() in pos_neg_list:
            global comment_type
            comment_type = message.text.lower()

            comment_type_edited(message)
        else:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            bot.register_next_step_handler(msg, comment_type_input)

def comment_type_edited(message):
    edit_menu(message)

########################################################################################

def shift_edit (message):
    msg = bot.send_message(message.chat.id, "انتخاب شیفت", reply_markup=shifts_markup)
    bot.register_next_step_handler(msg, shift_editing)

def shift_editing(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        edit_menu(message)
    else:    
        if message.text.lower() in shifts:
            global shift
            shift = message.text
            # shift_select(message)
            shift_edited(message)
        else:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            bot.register_next_step_handler(msg, shift_validation)

def shift_edited(message):
    edit_menu(message)

########################################################################################
def section_edit(message):
    msg = bot.send_message(message.chat.id, "انتخاب سکشن مربوطه", reply_markup=section_markup)
    bot.register_next_step_handler(msg, section_editing)

def section_editing(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        edit_menu(message)
    else:
        if message.text.lower() in section_list:
            global related_section
            related_section = message.text.lower()

            edit_menu(message)
        else:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            bot.register_next_step_handler(msg, section_editing)
########################################################################################



def receipt_number_edit(message):
    msg = bot.send_message(message.chat.id, "لطفا شماره فاکتور را وارد کنید، در غیر این صورت 'بعدی' را انتخاب کنید", reply_markup=next_markup)
    bot.register_next_step_handler(msg, receipt_number_editing)

def receipt_number_editing(message):
    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        edit_menu(message)
    else:
        global receipt_number
        try:
            receipt = int(message.text)
            if receipt > 99999 or receipt < 1:
                msg = bot.reply_to(message, "عدد وارد شده صحیح نیست")
                bot.register_next_step_handler(msg, receipt_number_editing)
            elif receipt == "بازگشت":
                receipt_number = None
                edit_menu(message)
            else:
                receipt_number = message.text
                edit_menu(message)
        except ValueError:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            bot.register_next_step_handler(msg, receipt_number_editing)




########################################################################################

def description_edit (message):
    msg = bot.send_message(message.chat.id, "لطفا توضیحات مورد نیاز را وارد کنید", reply_markup=back_markup)
    bot.register_next_step_handler(msg, description_editing)

def description_editing(message):
    global description

    if message.text.lower() == "/cancel":
        cancel(message)
    elif message.text.lower() == "/back":
        edit_menu(message)
    elif message.text.lower() == "بازگشت":
        description_data = None
        edit_menu(message)
    else:
        description = message.text
        edit_menu(message)

########################################################################################

def hide_menu(message):
    bot.delete_message(message.chat.id, edit_menu_message.message_id)

########################################################################################
# month, day, branch, shift, comment_type, comment, description



@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    if call.data == "cb_branch":
        hide_menu(call.message)
        branch_edit(call.message)

    # elif call.data == "cb_day":
    #     hide_menu(call.message)
    #     day_edit(call.message)

    elif call.data == "cb_month":
        hide_menu(call.message)
        month_edit(call.message)

    elif call.data == "cb_comment":
        hide_menu(call.message)
        comment_edit(call.message)

    elif call.data == "cb_com_type":
        hide_menu(call.message)
        comment_type_edit(call.message)

    elif call.data == "cb_shift":
        hide_menu(call.message)
        shift_edit(call.message)

    elif call.data == "cb_section":
        hide_menu(call.message)
        section_edit(call.message)

    elif call.data == "cb_desc":
        hide_menu(call.message)
        description_edit(call.message)

    elif call.data == "cb_receipt":
        hide_menu(call.message)
        receipt_number_edit(call.message)

    elif call.data == "cb_cancel":
        hide_menu(call.message)
        cancel(call.message)

    else:
        pass
########################################################################################
@bot.message_handler(commands=['restart'])
def restart(message):
    hide_menu(message)
    global edit_menu_message
    global date_of_insert
    global time_of_insert
    global user_name
    global user_id
    global ordinal_date
    global month_selected
    global day_selected
    global branch
    global shift
    global comment_type
    global comment
    global receipt_number
    global description

    edit_menu_message = None
    date_of_insert = None
    time_of_insert = None
    user_name = None
    user_id = None
    ordinal_date = None
    month_selected = None
    day_selected = None
    branch = None
    shift = None
    comment_type = None
    comment = None
    receipt_number = None
    receipt_number = None
    description = None
    start(message)
########################################################################################

def cancel(message):
    global date_of_insert
    global time_of_insert
    global user_name
    global user_id
    global ordinal_date
    global month_selected
    global day_selected
    global branch
    global shift
    global comment_type
    global comment
    global receipt_number
    global description

    edit_menu_message = None
    date_of_insert = None
    time_of_insert = None
    user_name = None
    user_id = None
    ordinal_date = None
    month_selected = None
    day_selected = None
    branch = None
    shift = None
    comment_type = None
    comment = None
    receipt_number = None
    description = None
    bot.send_message(message.chat.id, "عملیات لغو شد، برای شروع مجدد /start را بزنید", reply_markup=telebot.types.ReplyKeyboardRemove())


########################################################################################

bot.infinity_polling()


# receipt code
# expanding responsible section options
