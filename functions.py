import random
import datetime
import pytz
import json
import time_to_string

from datetime import datetime, timedelta

SdTz = pytz.timezone('Asia/Yekaterinburg')

def get_next_pay_date():

    today = datetime.now(tz=SdTz).date()
    if today.day > 5 and today.day < 21:
        pay_year = today.year
        pay_month = today.month
        pay_day = 21
    else:
        if today.month > 11:
            pay_year = today.year + 1
            pay_month = 1
        else:
            pay_year = today.year
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
        # time_description += time_to_string.get_string_hour(hours_left)
        time_description += ' '
    if minutes_left > 0:
        time_description += "{} мин ".format(minutes_left)
        # time_description += time_to_string.get_string_minute(minutes_left)
        time_description += ' '
    if seconds_left > 0:
        time_description += "{} сек".format(seconds_left)
        # time_description += time_to_string.get_string_second(seconds_left)
        time_description += ' '
    if time_description == "До конца рабочего дня осталось ":
        time_description = "Уже всё, иди домой"

    return time_description

def what_white_jija():
    
    random_value = random.random() * 100
    if random_value < 10:
        return 'Стакан выскальнул из рук и упал. Теперь неизвестно какая белая жижа была у тебя'
    if random_value > 10 and random_value < 50:
        return 'В стакане ты чувствуешь кисловатый привкус. Жижа рабочая'
    if random_value > 50 and random_value < 95:
        return 'В стакане ты чувствуешь сладкий привкус. Жижа не рабочая'
    if random_value > 95:
        return '😏🍆💦'

def save_user(user, chat_id):
    
    with open('users.json', 'r+') as file:
        new_user = {
            'user': user,
            'chat_id': chat_id
        }
        users = json.load(file)
        if new_user not in users['users']:
            users['users'].append(new_user)
            file.seek(0)
            json.dump(users, file, indent=4)

def get_random_chat_id():
    
    with open('users.json', 'r+') as file:
        users = json.load(file)
        random_user = users['users'][random.randrange(len(users['users']))]
        print(random_user['user'])
        return random_user['chat_id']
    
def get_users():
    
    with open('users.json', 'r+') as file:
        return json.load(file)    
    
def get_random_quote():
    
    with open('quote.json', encoding='utf-8') as file:
        quotes = json.load(file)
        random_quote = quotes['quotes'][random.randrange(len(quotes['quotes']))]
        return random_quote['quote']

def get_lestat_gif():
    
    return open('lestat.gif.mp4', 'rb')

def get_ufo_photo():
    
    return open('ufo.jpg', 'rb')