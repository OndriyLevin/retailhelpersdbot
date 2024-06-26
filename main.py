import telebot
import os

import functions
import time_to_string
# import torch

from dotenv import load_dotenv
from telebot import types

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
bot = telebot.TeleBot(os.environ.get('TOKEN_BOT'))

@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Сколько до конца рабочего дня?')
    btn2 = types.KeyboardButton('Сколько до зарплаты?')
    btn3 = types.KeyboardButton('Какая сегодня белая жижа?')
    btn4 = types.KeyboardButton('Случайная цитата')
    markup.add(btn1, btn2, btn3, btn4, row_width=1)
    if message.from_user.username == 'LevinAndrey':
        btn5 = types.KeyboardButton('Скинуть всем LESTAT GIF')
        btn6 = types.KeyboardButton('Вызвать члебобасов')
        btn7 = types.KeyboardButton('Вернуть бота')
        markup.add(btn5, btn6, btn7, row_width=2)
    bot.send_message(message.from_user.id, "Здрасте", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def start(message):

    functions.save_user(user=message.from_user.username, chat_id=message.from_user.id)

    if message.from_user.username == 'riz4besu':
        "Кто не доволен гифкой, не получает ответы"

    if message.text == 'Сколько до зарплаты?':
        payday_date = functions.get_next_pay_date()
        bot.send_message(message.from_user.id, "До зарплаты осталось {} д".format(functions.days_until_payday(payday_date)))
    elif message.text == 'Сколько до конца рабочего дня?':
        bot.send_message(message.from_user.id, functions.time_until_end_of_workday())
    elif message.text == 'Какая сегодня белая жижа?':
        bot.send_message(message.from_user.id, functions.what_white_jija())
    elif message.text == 'Случайная цитата':
        bot.send_message(message.from_user.id, functions.get_random_quote())

    elif message.text == 'На главный экран':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Сколько до конца рабочего дня?')
        btn2 = types.KeyboardButton('Сколько до зарплаты?')
        btn3 = types.KeyboardButton('Какая сегодня белая жижа?')
        btn4 = types.KeyboardButton('Случайная цитата')
        markup.add(btn1, btn2, btn3, btn4, row_width=1)
        if message.from_user.username == 'LevinAndrey':
            btn5 = types.KeyboardButton('Админка')
            markup.add(btn5)
    elif message.text == 'Админка':
        print(message.from_user.username)
        if message.from_user.username == 'LevinAndrey':
            markup = types.ReplyKeyboardRemove()
            btn1 = types.KeyboardButton('На главный экран')
            btn2 = types.KeyboardButton('Скинуть всем LESTAT GIF')
            markup.add(btn1, btn2, row_width=1)

    elif message.text == 'Скинуть всем LESTAT GIF':
        if message.from_user.username == 'LevinAndrey':
            users = functions.get_users()
            for user in users['users']:
                bot.send_animation(user['chat_id'], functions.get_lestat_gif())
    elif message.text == 'Вызвать члебобасов':
        if message.from_user.username == 'LevinAndrey':
            users = functions.get_users()
            for user in users['users']:
                bot.send_photo(user['chat_id'], functions.get_ufo_photo(), 'Члебобасы забрали бота до завтра')
    elif message.text == 'Вернуть бота':
        if message.from_user.username == 'LevinAndrey':
            users = functions.get_users()
            for user in users['users']:
                bot.send_message(user['chat_id'], 'Члебобасы вернули бота после процедуры зондирования')

bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть
