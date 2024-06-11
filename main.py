import telebot
import os
import time
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
bot = telebot.TeleBot(os.environ.get('TOKEN_BOT'))

from telebot import types

@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Сколько до конца рабочего дня?')
    btn2 = types.KeyboardButton('Сколько до зарплаты?')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, "Здрасте", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def start(message):
    
    if message.text == 'Сколько до конца рабочего дня?':
        bot.send_message(message.from_user.id, "Пока не ебу")
    elif message.text == 'Сколько до зарплаты?':
        bot.send_message(message.from_user.id, 'Пока не ебу')

bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть