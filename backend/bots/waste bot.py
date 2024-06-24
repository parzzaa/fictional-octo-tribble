import sqlite3
import jdatetime
import telebot
import pandas as pd
import openpyxl
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from persiantools.jdatetime import JalaliDate
from functools import wraps
from unidecode import unidecode


# frz test bot token: 1163491358:AAFsn2EW38nMpLI_vlPKelmTEvO9N-fDQ0o
# thedwastechecklist bot token: 6533736073:AAHMij2-FdpggDalnbqLaWjkLtCh_nVA33Y
########################################################################################
bot = telebot.TeleBot("6533736073:AAHMij2-FdpggDalnbqLaWjkLtCh_nVA33Y")
########################################################################################
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()
########################################################################################

user_name = None
user_id = None
day_selected = None
month_selected = None
type_select = None
department_selected = None
material = None
item = None
material_qty = None
item_qty = None
shift = None
description_input = None

########################################################################################
raw_list = list()
material_list = list()
item_list = list()

item_bakery_list = list()
item_pastry_list = list()
item_shahrak_bar_list = list()
item_kitchen_list = list()
item_fereshteh_bar_list = list()

material_bakery_list = list()
material_fereshteh_bar_list = list()
material_kitchen_list = list()
material_pastry_list = list()
material_shahrak_bar_list = list()
########################################################################################
file_in_progress = pd.read_excel("test_item_bakery.xlsx")
for row in file_in_progress.itertuples():
    row_as_list = list(row)
    raw_list.append(row_as_list)
for _ in raw_list:
    item_bakery_list.append(_[1])
    
bakery_item_markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)


options = tuple(item_bakery_list)
buttons = [types.KeyboardButton(str(i)) for i in options]
bakery_item_markup.add(*buttons)

for _ in item_bakery_list:
    item_list.append(_)
########################################################################################
raw_list = list()
########################################################################################
file_in_progress = pd.read_excel("test_item_pastry.xlsx")
for row in file_in_progress.itertuples():
    row_as_list = list(row)
    raw_list.append(row_as_list)
for _ in raw_list:
    item_pastry_list.append(_[1])
    
pastry_item_markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)

options = tuple(item_pastry_list)
buttons = [types.KeyboardButton(str(i)) for i in options]
pastry_item_markup.add(*buttons)

for _ in item_pastry_list:
    item_list.append(_)
########################################################################################
raw_list = list()
########################################################################################
file_in_progress = pd.read_excel("test_item_shahrak_bar.xlsx")
for row in file_in_progress.itertuples():
    row_as_list = list(row)
    raw_list.append(row_as_list)
for _ in raw_list:
    item_shahrak_bar_list.append(_[1])
    
shahrak_bar_item_markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)

options = tuple(item_shahrak_bar_list)
buttons = [types.KeyboardButton(str(i)) for i in options]
shahrak_bar_item_markup.add(*buttons)


for _ in item_shahrak_bar_list:
    item_list.append(_)

########################################################################################
raw_list = list()
########################################################################################
file_in_progress = pd.read_excel("test_item_fereshteh_bar.xlsx")
for row in file_in_progress.itertuples():
    row_as_list = list(row)
    raw_list.append(row_as_list)
for _ in raw_list:
    item_fereshteh_bar_list.append(_[1])
    
fereshteh_bar_item_markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)

options = tuple(item_fereshteh_bar_list)
buttons = [types.KeyboardButton(str(i)) for i in options]
fereshteh_bar_item_markup.add(*buttons)

for _ in item_fereshteh_bar_list:
    item_list.append(_)

########################################################################################
raw_list = list()
########################################################################################
file_in_progress = pd.read_excel("test_item_kitchen.xlsx")
for row in file_in_progress.itertuples():
    row_as_list = list(row)
    raw_list.append(row_as_list)
for _ in raw_list:
    item_kitchen_list.append(_[1])
    
kitchen_item_markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)

options = tuple(item_kitchen_list)
buttons = [types.KeyboardButton(str(i)) for i in options]
kitchen_item_markup.add(*buttons)

for _ in item_kitchen_list:
    item_list.append(_)

########################################################################################
raw_list = list()
########################################################################################
########################################################################################

file_in_progress = pd.read_excel("test_material_bakery.xlsx")
for row in file_in_progress.itertuples():
    row_as_list = list(row)
    raw_list.append(row_as_list)
for _ in raw_list:
    material_bakery_list.append(_[1])
    
bakery_material_markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)

options = tuple(material_bakery_list)
buttons = [types.KeyboardButton(str(i)) for i in options]
bakery_material_markup.add(*buttons)

for _ in material_bakery_list:
    material_list.append(_)
########################################################################################
raw_list = list()
########################################################################################
file_in_progress = pd.read_excel("test_material_fereshteh_bar.xlsx")
for row in file_in_progress.itertuples():
    row_as_list = list(row)
    raw_list.append(row_as_list)
for _ in raw_list:
    material_fereshteh_bar_list.append(_[1])

fereshteh_bar_material_markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)

options = tuple(material_fereshteh_bar_list)
buttons = [types.KeyboardButton(str(i)) for i in options]
fereshteh_bar_material_markup.add(*buttons)


for _ in material_fereshteh_bar_list:
    material_list.append(_)
########################################################################################
raw_list = list()
########################################################################################
file_in_progress = pd.read_excel("test_material_kitchen.xlsx")
for row in file_in_progress.itertuples():
    row_as_list = list(row)
    raw_list.append(row_as_list)
for _ in raw_list:
    material_kitchen_list.append(_[1])

kitchen_material_markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)

options = tuple(material_kitchen_list)
buttons = [types.KeyboardButton(str(i)) for i in options]
kitchen_material_markup.add(*buttons)


for _ in material_kitchen_list:
    material_list.append(_)
########################################################################################
raw_list = list()
########################################################################################
file_in_progress = pd.read_excel("test_material_pastry.xlsx")
for row in file_in_progress.itertuples():
    row_as_list = list(row)
    raw_list.append(row_as_list)
for _ in raw_list:
    material_pastry_list.append(_[1])

pastry_material_markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)

options = tuple(material_pastry_list)
buttons = [types.KeyboardButton(str(i)) for i in options]
pastry_material_markup.add(*buttons)


for _ in material_pastry_list:
    material_list.append(_)
########################################################################################
raw_list = list()
########################################################################################
file_in_progress = pd.read_excel("test_material_shahrak_bar.xlsx")
for row in file_in_progress.itertuples():
    row_as_list = list(row)
    raw_list.append(row_as_list)
for _ in raw_list:
    material_shahrak_bar_list.append(_[1])

shahrak_bar_material_markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)

options = tuple(material_shahrak_bar_list)
buttons = [types.KeyboardButton(str(i)) for i in options]
shahrak_bar_material_markup.add(*buttons)


for _ in material_shahrak_bar_list:
    material_list.append(_)
########################################################################################
raw_list = list()
########################################################################################

year = 1402

def convert_to_excel_ordinal(year, month, day):
    offset = 693594
    mytime = JalaliDate(year, month, day).to_gregorian()
    n = mytime.toordinal()
    return (n - offset)
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
type_markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
type_markup.add("متریال", "آیتم")
types_list = ["متریال", "آیتم"]
########################################################################################
department_markup = types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True, resize_keyboard=True)
department_markup.add("بیکری", "پیستری", "بار شهرک", "بار فرشته", "آشپزخانه")
departments = ["بیکری", "پیستری", "بار شهرک", "بار فرشته", "آشپزخانه"]
########################################################################################
next_markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
next_markup.add("بعدی")
########################################################################################
back_markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
back_markup.add("بازگشت")

########################################################################################
shifts_markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
shifts_markup.add("صبح", "عصر")
shifts = ["صبح", "عصر"]
########################################################################################
materials = [] 
########################################################################################
items = []

########################################################################################


def is_known_username(username):
    '''
    Returns a boolean if the username is known in the user-list.
    '''
    # known_usernames = ["Fuadrn", "mahannemati", ]
    known_usernames = ["Fuadrn", "mahannemati", "Azerila101"]

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
@private_access()

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
########################################################################################
def month_validation(message):
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
                department_menu(message)
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
                department_menu(message)
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

########################################################################################

def department_menu(message):
    msg = bot.send_message(message.chat.id, "لطفا دپارتمان را انتخاب کنید", reply_markup=department_markup)
    bot.register_next_step_handler(msg, department_select)

def department_select(message):
    global department_selected
    if message.text.lower() in departments:
        department_selected = message.text.lower()
        shift_choose(message)
    else:
        msg = bot.reply_to(message, "ورودی غیر مجاز")
        bot.register_next_step_handler(msg, department_select)

########################################################################################

def shift_choose(message):
    msg = bot.send_message(message.chat.id, "انتخاب شیفت", reply_markup=shifts_markup)
    bot.register_next_step_handler(msg, shift_validation)


def shift_validation(message):
    if message.text.lower() in shifts:
        global shift
        shift = message.text
        type_menu(message)
    else:
        msg = bot.reply_to(message, "ورودی غیر مجاز")
        bot.register_next_step_handler(msg, shift_validation)

########################################################################################
def type_menu (message):
    msg = bot.send_message(message.chat.id, "لطفا انتخاب کنید", reply_markup=type_markup)
    bot.register_next_step_handler(msg, type_selected)

def type_selected (message):
    if message.text.lower() in types_list:
        global type_select
        type_select = message.text
        if type_select == "متریال":
            material_select(message)

        elif type_select == "آیتم":
            item_select(message)
        else:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            bot.register_next_step_handler(msg, type_selected)
        
    else:
        msg = bot.reply_to(message, "ورودی غیر مجاز")
        bot.register_next_step_handler(msg, type_selected)

########################################################################################

def material_select(message):

    if department_selected == "بیکری":
        msg = bot.send_message(message.chat.id, "لطفا متریال مورد نظر را انتخاب کنید", reply_markup=bakery_material_markup)

    elif department_selected == "پیستری":
        msg = bot.send_message(message.chat.id, "لطفا متریال مورد نظر را انتخاب کنید", reply_markup=pastry_material_markup)

    elif department_selected == "آشپزخانه":
        msg = bot.send_message(message.chat.id, "لطفا متریال مورد نظر را انتخاب کنید", reply_markup=kitchen_material_markup)

    elif department_selected == "بار شهرک":
        msg = bot.send_message(message.chat.id, "لطفا متریال مورد نظر را انتخاب کنید", reply_markup=shahrak_bar_material_markup)

    elif department_selected == "بار فرشته":
        msg = bot.send_message(message.chat.id, "لطفا متریال مورد نظر را انتخاب کنید", reply_markup=fereshteh_bar_material_markup)

    bot.register_next_step_handler(msg, material_input)
# ["بیکری", "پیستری", "بار شهرک", "بار فرشته", "آشپزخانه"]

def material_input(message):
    global material
    if message.text.lower() in material_list:
        material = message.text
        material_qty_input(message)
    else:
        msg = bot.reply_to(message, "ورودی غیر مجاز")
        bot.register_next_step_handler(msg, material_input)
########################################################################################
def item_select(message):
    if department_selected == "بیکری":
            msg = bot.send_message(message.chat.id, "لطفا آیتم مورد نظر را انتخاب کنید", reply_markup=bakery_item_markup)

    elif department_selected == "پیستری":
            msg = bot.send_message(message.chat.id, "لطفا آیتم مورد نظر را انتخاب کنید", reply_markup=pastry_item_markup)

    elif department_selected == "آشپزخانه":
            msg = bot.send_message(message.chat.id, "لطفا آیتم مورد نظر را انتخاب کنید", reply_markup=kitchen_item_markup)

    elif department_selected == "بار شهرک":
            msg = bot.send_message(message.chat.id, "لطفا آیتم مورد نظر را انتخاب کنید", reply_markup=shahrak_bar_item_markup)

    elif department_selected == "بار فرشته":
            msg = bot.send_message(message.chat.id, "لطفا آیتم مورد نظر را انتخاب کنید", reply_markup=fereshteh_bar_item_markup)

    bot.register_next_step_handler(msg, item_input)

def item_input(message):
    global item
    if message.text.lower() in item_list:
        item = message.text
        item_qty_input(message)
    else:
        msg = bot.reply_to(message, "ورودی غیر مجاز")
        bot.register_next_step_handler(msg, item_input)

########################################################################################
def material_qty_input (message):
    msg = bot.send_message(message.chat.id, "لطفا مقدار را بر حسب گرم وارد کنید", reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, material_qty_validation)

def material_qty_validation(message):
    global material_qty
    try:
        qty = float(message.text)
        if qty > 50_000 or qty < 0:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            bot.register_next_step_handler(msg, material_qty_validation)
        else:
            material_qty = message.text
            description(message)
    except ValueError:
        msg = bot.reply_to(message, "ورودی غیر مجاز")
        bot.register_next_step_handler(msg, material_qty_validation)



########################################################################################
def item_qty_input (message):
    msg = bot.send_message(message.chat.id, "لطفا تعداد را وارد کنید", reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, item_qty_validation)

def item_qty_validation(message):
    global item_qty
    try:
        qty = float(message.text)
        if qty > 100 or qty < 0:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            bot.register_next_step_handler(msg, item_qty_validation)
        else:
            item_qty = message.text
            item_qty = int(item_qty)

            description(message)

    except ValueError:
        msg = bot.reply_to(message, "ورودی غیر مجاز")
        bot.register_next_step_handler(msg, item_qty_validation)
########################################################################################
def description(message):
    msg = bot.send_message(message.chat.id, "لطفا توضیحات مورد نیاز را وارد کنید", reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, description_in)

def description_in(message):
    global description_input
    description_input = message.text
    to_db(message)

########################################################################################
def to_db(message):
    global edit_menu_message

    global day_selected    
    global month_selected
    global type_select
    global department_selected
    global material
    global item
    global material_qty
    global item_qty
    global shift
    global description_input




    day_selected = str(day_selected)
    month_selected = str(month_selected)
    type_select = str(type_select)
    department_selected = str(department_selected)
    material = str(material)
    item = str(item)
    material_qty = str(material_qty)
    item_qty = str(item_qty)
    shift =  str(shift)
    description_input = str(description_input)



    if type_select == "آیتم":
        cursor.execute('''CREATE TABLE IF NOT EXISTS item_waste (
        "id"    INTEGER NOT NULL PRIMARY KEY,
        "time_of_insert"  TEXT NOT NULL,
        "user_name"    TEXT NOT NULL,
        "user_id"    INT NOT NULL,
        "ordinal_date"    TEXT NOT NULL,
        "month_selected"   TEXT NOT NULL,
        "day_selected"    INTEGER NOT NULL,
        "department_selected"    TEXT NOT NULL,
        "shift"    TEXT NOT NULL,
        "item"    TEXT NOT NULL,
        "quantity"    INTEGER NOT NULL,
        "description_input"    TEXT NOT NULL
        );
        ''')

        final_check_message = "ماه: " + month_selected + "\n" + "روز: " + day_selected + "\n" + "دپارتمان: " + department_selected + "\n" + "شیفت: " + shift + "\n" + "آیتم: " + item + "\n" + "تعداد: " + item_qty + "\n" + "توضیحات: " + description_input + "\n" + "اگر از صحت اطلاعات وارد شده مطمئن هستید گزینه /submit را بزنید و در غیر این صورت برای بازگشت به مرحله اول از /restart استفاده کنید"

        agree_markup = InlineKeyboardMarkup()
        agree_markup.row_width = 3
        agree_markup.add(
        InlineKeyboardButton("دپارتمان", callback_data="cb_department"),
        InlineKeyboardButton("روز", callback_data="cb_day"),
        InlineKeyboardButton("ماه", callback_data = "cb_month"),
        InlineKeyboardButton("تعداد", callback_data="cb_qty"),
        InlineKeyboardButton("آیتم", callback_data="cb_item"),
        InlineKeyboardButton("شیفت", callback_data="cb_shift"),
        InlineKeyboardButton("توضیحات", callback_data = "cb_desc")
        )


        # item_to_db(message, time_now, user_name, user_id, ordinal_date, month_selected, day_selected, department_selected, shift, item, item_qty)
    elif type_select == "متریال":
        cursor.execute('''CREATE TABLE IF NOT EXISTS material_waste (
        "id"    INTEGER NOT NULL PRIMARY KEY,
        "time_of_insert"  TEXT NOT NULL,
        "user_name"    TEXT NOT NULL,
        "user_id"    INT NOT NULL,
        "ordinal_date"    TEXT NOT NULL,
        "month_selected"   TEXT NOT NULL,
        "day_selected"    INTEGER NOT NULL,
        "department_selected"    TEXT NOT NULL,
        "shift"    TEXT NOT NULL,
        "material"    TEXT NOT NULL,
        "quantity"    INTEGER NOT NULL,
        "description_input"    TEXT NOT NULL
        );
        ''')

        final_check_message = "ماه: " + month_selected + "\n" + "روز: " + day_selected + "\n" + "دپارتمان: " + department_selected + "\n" + "شیفت: " + shift + "\n" + "متریال: " + material + "\n" + "مقدار به گرم: " + material_qty + "\n" + "توضیحات: " + description_input + "\n" + "اگر از صحت اطلاعات وارد شده مطمئن هستید گزینه /submit را بزنید و در غیر این صورت برای بازگشت به مرحله اول از /restart استفاده کنید"


        agree_markup = InlineKeyboardMarkup()
        agree_markup.row_width = 3
        agree_markup.add(
        InlineKeyboardButton("دپارتمان", callback_data="cb_department"),
        InlineKeyboardButton("روز", callback_data="cb_day"),
        InlineKeyboardButton("ماه", callback_data = "cb_month"),
        InlineKeyboardButton("مقدار", callback_data="cb_qty"),
        InlineKeyboardButton("متریال", callback_data="cb_material"),
        InlineKeyboardButton("شیفت", callback_data="cb_shift"),
        InlineKeyboardButton("توضیحات", callback_data = "cb_desc")
        )

        # material_to_db(message, time_now, user_name, user_id, ordinal_date, month_selected, day_selected, department_selected, shift, material, material_qty)
        
    else:
        print("wrong type selected")
    edit_menu_message = bot.send_message(message.chat.id, final_check_message, reply_markup=agree_markup)
    # finale(message)


########################################################################################
def month_edit (message):
    msg = bot.send_message(message.chat.id, "انتخاب ماه", reply_markup=month_markup)
    bot.register_next_step_handler(msg, month_editing)

def month_editing(message):
    if message.text.lower() not in month:
        msg = bot.reply_to(message, "ورودی غیر مجاز")
        bot.register_next_step_handler(msg, month_edit)
    else:
        global month_selected

        month_selected = message.text
        
        month_edited (message)
def month_edited(message):
    to_db(message)
########################################################################################
def day_edit (message):
    msg = bot.send_message(message.chat.id, "روز را وارد کنید", reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, day_editing)

def day_editing(message):

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
    to_db(message)
########################################################################################
def department_edit (message):
    msg = bot.send_message(message.chat.id, "لطفا دپارتمان را انتخاب کنید", reply_markup=department_markup)
    bot.register_next_step_handler(msg, department_editing)

def department_editing(message):
    
    global department_selected
    if message.text.lower() in departments:
        department_selected = message.text.lower()
        department_edited(message)
    else:
        msg = bot.reply_to(message, "ورودی غیر مجاز")
        bot.register_next_step_handler(msg, department_edit)

def department_edited(message):
    global material
    global item
    global material_qty
    global item_qty

    material = "-"
    item = "-"
    item_qty = "-"
    material_qty = "-"
    to_db(message)

########################################################################################
def shift_edit (message):
    msg = bot.send_message(message.chat.id, "انتخاب شیفت", reply_markup=shifts_markup)
    bot.register_next_step_handler(msg, shift_editing)


def shift_editing(message):
    if message.text.lower() in shifts:
        global shift
        shift = message.text
        shift_edited(message)
    else:
        msg = bot.reply_to(message, "ورودی غیر مجاز")
        bot.register_next_step_handler(msg, shift_edited)
def shift_edited(message):
    to_db(message)

########################################################################################
def item_edit (message):
    if department_selected == "بیکری":
            msg = bot.send_message(message.chat.id, "لطفا آیتم مورد نظر را انتخاب کنید", reply_markup=bakery_item_markup)

    elif department_selected == "پیستری":
            msg = bot.send_message(message.chat.id, "لطفا آیتم مورد نظر را انتخاب کنید", reply_markup=pastry_item_markup)

    elif department_selected == "آشپزخانه":
            msg = bot.send_message(message.chat.id, "لطفا آیتم مورد نظر را انتخاب کنید", reply_markup=kitchen_item_markup)

    elif department_selected == "بار شهرک":
            msg = bot.send_message(message.chat.id, "لطفا آیتم مورد نظر را انتخاب کنید", reply_markup=shahrak_bar_item_markup)

    elif department_selected == "بار فرشته":
            msg = bot.send_message(message.chat.id, "لطفا آیتم مورد نظر را انتخاب کنید", reply_markup=fereshteh_bar_item_markup)

    bot.register_next_step_handler(msg, item_editing)

def item_editing(message):
    global item
    if message.text.lower() in item_list:
        item = message.text
        item_edited(message)
    else:
        msg = bot.reply_to(message, "ورودی غیر مجاز")
        bot.register_next_step_handler(msg, item_edit)

def item_edited(message):
    to_db(message)

########################################################################################
def material_edit_2 (message):
    if department_selected == "بیکری":
        msg = bot.send_message(message.chat.id, "لطفا متریال مورد نظر را انتخاب کنید", reply_markup=bakery_material_markup)

    elif department_selected == "پیستری":
        msg = bot.send_message(message.chat.id, "لطفا متریال مورد نظر را انتخاب کنید", reply_markup=pastry_material_markup)

    elif department_selected == "آشپزخانه":
        msg = bot.send_message(message.chat.id, "لطفا متریال مورد نظر را انتخاب کنید", reply_markup=kitchen_material_markup)

    elif department_selected == "بار شهرک":
        msg = bot.send_message(message.chat.id, "لطفا متریال مورد نظر را انتخاب کنید", reply_markup=shahrak_bar_material_markup)

    elif department_selected == "بار فرشته":
        msg = bot.send_message(message.chat.id, "لطفا متریال مورد نظر را انتخاب کنید", reply_markup=fereshteh_bar_material_markup)

    bot.register_next_step_handler(msg, material_editing)

def material_editing(message):
    global material
    if message.text.lower() in material_list:
        material = message.text
        material_edited(message)
    else:
        msg = bot.reply_to(message, "ورودی غیر مجاز")
        bot.register_next_step_handler(msg, material_edit_2)

def material_edited(message):
    global material_qty
    material_qty = "-"
    to_db(message)

########################################################################################

def material_qty_edit (message):
    msg = bot.send_message(message.chat.id, "لطفا مقدار را بر حسب گرم وارد کنید", reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, material_qty_editing)

def material_qty_editing(message):
    global material_qty
    try:
        qty = float(message.text)
        if qty > 50_000 or qty < 0:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            bot.register_next_step_handler(msg, material_qty_validation)
        else:
            material_qty = message.text
            to_db(message)
    except ValueError:
        msg = bot.reply_to(message, "ورودی غیر مجاز")
        bot.register_next_step_handler(msg, material_qty_validation)

def material_qty_edited(message):
    to_db(message)
########################################################################################

def item_qty_edit (message):
    msg = bot.send_message(message.chat.id, "لطفا تعداد را وارد کنید", reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, item_qty_editing)

def item_qty_editing(message):
    global item_qty
    try:
        qty = float(message.text)
        if qty > 100 or qty < 0:
            msg = bot.reply_to(message, "ورودی غیر مجاز")
            bot.register_next_step_handler(msg, item_qty_editing)
        else:
            item_qty = message.text
            item_qty = int(item_qty)
            to_db(message)
    except ValueError:
        msg = bot.reply_to(message, "ورودی غیر مجاز")
        bot.register_next_step_handler(msg, item_qty_editing)
########################################################################################

def desc_edit(message):
    msg = bot.send_message(message.chat.id, "لطفا توضیحات مورد نیاز را وارد کنید", reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, desc_editing)

def desc_editing(message):
    global description_input
    description_input = message.text
    to_db(message)

########################################################################################
@bot.callback_query_handler(func=lambda call: True)

def callback_query(call):

    if call.data == "cb_month":
        hide_menu(call.message)
        month_edit(call.message)

    elif call.data == "cb_day":
        hide_menu(call.message)
        day_edit(call.message)
        
    elif call.data == "cb_department":
        hide_menu(call.message)
        department_edit(call.message)
        
    elif call.data == "cb_shift":
        hide_menu(call.message)
        shift_edit(call.message)
        
    elif call.data == "cb_item":
        hide_menu(call.message)
        item_edit(call.message)
        
    elif call.data == "cb_material":
        hide_menu(call.message)
        material_edit_2(call.message)

    elif call.data == "cb_qty":
        if type_select == "آیتم":
            item_qty_edit(call.message)
        elif type_select == "متریال":
            material_qty_edit(call.message)
        hide_menu(call.message)
        # quantity_edit(call.message)
    elif call.data == "cb_desc":
        
        hide_menu(call.message)
        desc_edit(call.message)
    else:
        pass


def hide_menu(message):
    bot.delete_message(message.chat.id, edit_menu_message.message_id)


def finale(message):

    pass


@bot.message_handler(commands=["submit"])
def submit(message):
    global edit_menu_message

    time_now = jdatetime.datetime.now()
    time_now = str(time_now)

    to_ordinal_day = int(day_selected)
    to_ordinal_month = int(month_dict[month_selected])
    ordinal_date = convert_to_excel_ordinal(year, to_ordinal_month, to_ordinal_day)

    if type_select == "آیتم" and item_qty != "-" and item != "-":
        cursor.execute('INSERT INTO item_waste (time_of_insert, user_name, user_id, ordinal_date, month_selected, day_selected, department_selected, shift, item, quantity, description_input) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (time_now, user_name, user_id, ordinal_date, month_selected, unidecode(day_selected), department_selected, shift, item, unidecode(item_qty), description_input))
        hide_menu(message)
        bot.send_message(message.chat.id, "اطلاعات ذخیره شد، برای ورود رکورد جدید از /start استفاده کنید")

        conn.commit()
#     bot.send_message(message.chat.id, "اطلاعات ذخیره شد، برای ورود رکورد جدید از /start استفاده کنید")
    elif type_select == "متریال" and material_qty != "-" and material != "-":
        cursor.execute('INSERT INTO material_waste (time_of_insert, user_name, user_id, ordinal_date, month_selected, day_selected, department_selected, shift, material, quantity, description_input) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (time_now, user_name, user_id, ordinal_date, month_selected, unidecode(day_selected), department_selected, shift, material, unidecode(material_qty), description_input))
        hide_menu(message)
        bot.send_message(message.chat.id, "اطلاعات ذخیره شد، برای ورود رکورد جدید از /start استفاده کنید")
        conn.commit()
    else:
        bot.send_message(message.chat.id, "اطلاعات وارد شده صحیح نیست، لطفا مجددا تلاش کنید")
        start(message)

@bot.message_handler(commands=['restart'])
def restart(message):
    hide_menu(message)
    global day_selected    
    global month_selected
    global type_select
    global department_selected
    global material
    global item
    global material_qty
    global item_qty
    global shift
    global description_input

    day_selected = None
    month_selected = None
    type_select = None
    department_selected = None
    material = None
    item = None
    material_qty = None
    item_qty = None
    shift = None
    description_input = None
    bot.send_message(message.chat.id, " برای ورود رکورد جدید از /start استفاده کنید")


bot.infinity_polling()