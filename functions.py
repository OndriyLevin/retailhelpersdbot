import random
import datetime
import pytz
import json
import os
import DB
import UserModel

from datetime import datetime, timedelta

SdTz = pytz.timezone('Asia/Yekaterinburg')

def init():
    DB.init()
def get_next_pay_date():

    today = datetime.now(tz=SdTz).date()
    if today.day >= 5 and today.day < 21:
        pay_year = today.year
        pay_month = today.month
        pay_day = 21
    else:
        if today.month > 11:
            pay_year = today.year + 1
            pay_month = 1
        else:
            pay_year = today.year
            if today.day < 21:
                pay_month = today.month
            else:
                pay_month = today.month + 1
        pay_day = 5

    payday_date = datetime(pay_year, pay_month, pay_day, tzinfo=SdTz)

    weekday = payday_date.weekday()
    if weekday == 5:
        pay_day = pay_day - 1
    if weekday == 6:
        pay_day = pay_day + 1

    payday_date = datetime(pay_year, pay_month, pay_day, tzinfo=SdTz)
    return payday_date

def days_until_payday(payday_date):

    today = datetime.now(tz=SdTz).date()
    days_left = (payday_date.date() - today).days
    return max(days_left, 0)  # если зарплата уже сегодня, вернем 0, чтобы не было отрицательного значения

def time_until_end_of_workday():

    current_time = datetime.now(tz=SdTz)
    weekday = current_time.weekday()
    if weekday > 4:
        return "Выходной, спи"
    begin_of_workday = datetime.now(tz=SdTz).replace(hour=8, minute=0, second=0, microsecond=0)
    if weekday < 4:
        end_of_workday = datetime.now(tz=SdTz).replace(hour=17, minute=0, second=0, microsecond=0)  # рабочий день заканчивается в 17:00
    else:
        end_of_workday = datetime.now(tz=SdTz).replace(hour=16, minute=0, second=0, microsecond=0)  # рабочий день заканчивается в 16:00

    if current_time < begin_of_workday:
        return "Работа ещё не началась. Вставай!"
    if current_time > end_of_workday:
        return "Работа уже кончилась. Спи!"

    time_left = end_of_workday - current_time

    hours_left = int(time_left.total_seconds() // 3600)
    minutes_left = int((time_left.total_seconds() % 3600) // 60)
    seconds_left = int(time_left.total_seconds() % 60)

    # Сопоставим каждому временному интервалу его текстовое описание
    time_description = "До конца рабочего дня осталось: "
    if hours_left > 0:
        time_description += "{} ч ".format(hours_left)
        time_description += ' '
    if minutes_left > 0:
        time_description += "{} мин ".format(minutes_left)
        time_description += ' '
    if seconds_left > 0:
        time_description += "{} сек".format(seconds_left)
        time_description += ' '
    if time_description == "До конца рабочего дня осталось ":
        time_description = "Уже всё, иди домой"

    return time_description

def save_user(user, chat_id):
    new_user = UserModel.User(user, chat_id)
    new_user.save_to_db()
    
def get_users():
    
    return DB.get_users()

def is_admin(user):

    return DB.check_user_admin_rights(user)

def user_is_exist(user):

    return DB.is_saved_user(user)
    
def get_random_quote():
    
    quotes = DB.get_quotes()
    random_quote = quotes[random.randrange(len(quotes))]
    return random_quote[1]

def get_all_quotes():

    return DB.get_quotes()

def get_all_new_quotes():

    return DB.get_new_quotes()

def new_quote(quote):

    DB.new_quote(quote)

def offer_quote(quote):

    DB.offer_quote(quote)

def deny_quote(quote):

    DB.deny_quote(quote)

def get_lestat_gif():
    
    return open('lestat.gif.mp4', 'rb')

def get_ufo_photo():
    
    return open('ufo.jpg', 'rb')

def update_today():

    new_today = {
        'day': datetime.now(tz=SdTz).date().day
    }
    reset_users = False
    with open('today.json', 'r+') as file:

        today_json = json.load(file)
        if new_today != today_json:
            reset_users=True

    os.remove('today.json')

    with open('today.json', 'w') as file:
        json.dump(new_today, file, indent=4)

    if reset_users:
        DB.reset_jija()