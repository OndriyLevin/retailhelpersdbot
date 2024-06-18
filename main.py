import telebot
import os
import datetime
from datetime import datetime, timedelta
import pytz
import time_to_string
import torch

from dotenv import load_dotenv
from telebot import types

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
bot = telebot.TeleBot(os.environ.get('TOKEN_BOT'))

SdTz = pytz.timezone('Asia/Yekaterinburg')

device = torch.device('cpu')
torch.set_num_threads(4)
local_file = 'model.pt'

if not os.path.isfile(local_file):
    torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v4_ru.pt',
                                   local_file)

model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
model.to(device)

sample_rate = 48000
speaker='baya'

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
    print(weekday)
    begin_of_workday = datetime.now(tz=SdTz).replace(hour=8, minute=0, second=0, microsecond=0)
    if weekday < 4:
        end_of_workday = datetime.now(tz=SdTz).replace(hour=23, minute=0, second=0, microsecond=0)  # рабочий день заканчивается в 17:00
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
        # time_description += "{} ч ".format(hours_left)
        time_description += time_to_string.get_string_hour(hours_left)
        time_description += ' '
    if minutes_left > 0:
        # time_description += "{} мин ".format(minutes_left)
        time_description += time_to_string.get_string_minute(minutes_left)
        time_description += ' '
    if seconds_left > 0:
        # time_description += "{} сек".format(seconds_left)
        time_description += time_to_string.get_string_second(seconds_left)
        time_description += ' '
    if time_description == "До конца рабочего дня осталось ":
        time_description = "Уже всё, иди домой"

    return time_description

@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Сколько до конца рабочего дня?')
    btn2 = types.KeyboardButton('Сколько до зарплаты?')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, "Здрасте", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def start(message):

    if message.text == 'Сколько до зарплаты?':
        payday_date = get_next_pay_date()
        # bot.send_message(message.from_user.id, "До зарплаты осталось {} ".format(time_to_string.get_string_day(days_until_payday(payday_date))))
        string_message = "До зарплаты осталось {} ".format(time_to_string.get_string_day(days_until_payday(payday_date)))
        audio_paths = model.save_wav(text=string_message,
                                     speaker=speaker,
                                     sample_rate=sample_rate)
        print(audio_paths)
        voice = open(audio_paths, 'rb')
        print(voice)
        bot.send_voice(message.from_user.id, voice)
        bot.send_voice(message.from_user.id, "FILEID")
    elif message.text == 'Сколько до конца рабочего дня?':
        string_message = time_until_end_of_workday()
        audio_paths = model.save_wav(text=string_message,
                                     speaker=speaker,
                                     sample_rate=sample_rate)
        print(audio_paths)
        voice = open(audio_paths, 'rb')
        print(voice)
        bot.send_voice(message.from_user.id, voice)
        bot.send_voice(message.from_user.id, "FILEID")
        # bot.send_message(message.from_user.id, time_until_end_of_workday())

bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть
