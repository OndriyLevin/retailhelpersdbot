import telebot
import functions
import env_utils
from UserModel import User
from telebot import types

bot = telebot.TeleBot(env_utils.get_tokken_value('TOKEN_BOT'))

functions.init()

@bot.message_handler(commands=['start'])
def start(message):

    CurrentUser = User(message.from_user.username, message.from_user.id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Сколько до конца рабочего дня?')
    btn2 = types.KeyboardButton('Сколько до зарплаты?')
    btn3 = types.KeyboardButton('Какая сегодня белая жижа?')
    btn4 = types.KeyboardButton('Случайная цитата')
    markup.add(btn1, btn2, btn3, btn4, row_width=1)
    if CurrentUser.admin:
        btn5 = types.KeyboardButton('Админка')
        markup.add(btn5)
    bot.send_message(CurrentUser.chat_id, "Здрасте", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def start(message):

    functions.update_today()

    CurrentUser = User(message.from_user.username, message.from_user.id)

    if message.text == 'Сколько до зарплаты?':
        payday_date = functions.get_next_pay_date()
        bot.send_message(CurrentUser.chat_id, "До зарплаты осталось {} д".format(functions.days_until_payday(payday_date)))
    elif message.text == 'Сколько до конца рабочего дня?':
        bot.send_message(CurrentUser.chat_id, functions.time_until_end_of_workday())
    elif message.text == 'Какая сегодня белая жижа?':
        bot.send_message(CurrentUser.chat_id, CurrentUser.what_white_jija())
    elif message.text == 'Случайная цитата':
        bot.send_message(CurrentUser.chat_id, functions.get_random_quote())

    elif message.text == 'На главный экран':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Сколько до конца рабочего дня?')
        btn2 = types.KeyboardButton('Сколько до зарплаты?')
        btn3 = types.KeyboardButton('Какая сегодня белая жижа?')
        btn4 = types.KeyboardButton('Случайная цитата')
        markup.add(btn1, btn2, btn3, btn4, row_width=1)
        if CurrentUser.admin:
            btn5 = types.KeyboardButton('Админка')
            markup.add(btn5)
        bot.send_message(CurrentUser.chat_id, "Главное меню", reply_markup=markup)
    elif message.text == 'Админка':
        if CurrentUser.admin:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('На главный экран')
            btn2 = types.KeyboardButton('Скинуть всем LESTAT GIF')
            btn3 = types.KeyboardButton('Вызвать члебобасов')
            btn4 = types.KeyboardButton('Вернуть бота')
            # btn5 = types.KeyboardButton('Написать всем')
            markup.add(btn1, btn2, btn3, btn4, row_width=1)
            bot.send_message(CurrentUser.chat_id, "Админка", reply_markup=markup)
    elif message.text == 'Скинуть всем LESTAT GIF':
        if CurrentUser.admin:
            users = functions.get_users()
            for user in users:
                try:
                    bot.send_animation(user[1], functions.get_lestat_gif())
                except:
                    print(user[0])
    elif message.text == 'Вызвать члебобасов':
        if CurrentUser.admin:
            users = functions.get_users()
            for user in users:
                try:
                    bot.send_photo(user[1], functions.get_ufo_photo(), 'Члебобасы забрали бота до завтра')
                except:
                    print(user[0])
    elif message.text == 'Вернуть бота':
        if CurrentUser.admin:
            users = functions.get_users()
            for user in users:
                try:
                    bot.send_message(user[1], 'Члебобасы вернули бота после процедуры зондирования')
                except:
                    print(user[0])

@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):

    results = []
    query_text = query.query.lower()

    quotes = functions.get_all_quotes()

    if quotes:
        for quote in quotes:
            if query_text in quote[1].lower():
                result = types.InlineQueryResultArticle(
                    id=quote[0],
                    title=quote[1],
                    input_message_content=types.InputTextMessageContent(quote[1])
                )
                results.append(result)

    bot.answer_inline_query(query.id, results, cache_time=1)

bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть
