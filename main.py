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
    btn5 = types.KeyboardButton('Предложить цитату')
    markup.add(btn1, btn2, btn3, btn4, btn5, row_width=1)
    if CurrentUser.admin:
        btn6 = types.KeyboardButton('Админка')
        markup.add(btn6)
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
        bot.send_message(CurrentUser.chat_id, functions.get_random_quote(), reply_markup = create_inline_buttons_random_quote())
    elif message.text == 'Предложить цитату':
        bot.send_message(CurrentUser.chat_id, 'Какая цитата?')
        bot.register_next_step_handler(message, offer_new_quota)

    elif message.text == 'На главный экран':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Сколько до конца рабочего дня?')
        btn2 = types.KeyboardButton('Сколько до зарплаты?')
        btn3 = types.KeyboardButton('Какая сегодня белая жижа?')
        btn4 = types.KeyboardButton('Случайная цитата')
        btn5 = types.KeyboardButton('Предложить цитату')
        markup.add(btn1, btn2, btn3, btn4, btn5, row_width=1)
        if CurrentUser.admin:
            btn6 = types.KeyboardButton('Админка')
            markup.add(btn6)
        bot.send_message(CurrentUser.chat_id, "Главное меню", reply_markup=markup)
    elif message.text == 'Админка':
        if CurrentUser.admin:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('На главный экран')
            btn2 = types.KeyboardButton('Скинуть всем LESTAT GIF')
            btn3 = types.KeyboardButton('Вызвать члебобасов')
            btn4 = types.KeyboardButton('Вернуть бота')
            btn5 = types.KeyboardButton('Написать всем')
            btn6 = types.KeyboardButton('Новая цитата')
            btn7 = types.KeyboardButton('Согласовать цитаты')
            markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, row_width=1)
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
    elif message.text == 'Написать всем':
        if CurrentUser.admin:
            bot.send_message(CurrentUser.chat_id, 'Что написать?')
            bot.register_next_step_handler(message, text_to_all)
    elif message.text == 'Новая цитата':
        if CurrentUser.admin:
            bot.send_message(CurrentUser.chat_id, 'Какая цитата?')
            bot.register_next_step_handler(message, new_quota)
    elif message.text == 'Согласовать цитаты':
        if CurrentUser.admin:
            new_quotes = functions.get_all_new_quotes()
            if new_quotes:
                bot.send_message(CurrentUser.chat_id, new_quotes[0][1], reply_markup = create_quote_inline_buttons(0, len(new_quotes)))
            else:
                bot.send_message(CurrentUser.chat_id, 'Нет предложенных цитат')
def text_to_all(message):
    users = functions.get_users()
    for user in users:
        try:
            bot.send_message(user[1], message.text)
        except:
            print(user[0])
def new_quota(message):

    CurrentUser = User(message.from_user.username, message.from_user.id)

    try:
        functions.new_quote( message.text )
        bot.send_message( CurrentUser.chat_id, 'Готово')
    except:
        bot.send_message( CurrentUser.chat_id, 'Омшимбка(')

def offer_new_quota(message):

    CurrentUser = User(message.from_user.username, message.from_user.id)

    try:
        functions.offer_quote( message.text )
        bot.send_message( CurrentUser.chat_id, 'Готово')
    except:
        bot.send_message( CurrentUser.chat_id, 'Омшимбка(')

def create_quote_inline_buttons(index, max_len):

    prev_button = types.InlineKeyboardButton("⬅️",callback_data=f"quote_prev_{index-1}")
    next_button = types.InlineKeyboardButton("➡️",callback_data=f"quote_next_{index+1}")
    no_button= types.InlineKeyboardButton("❌",callback_data=f"quote_no_{index+1}")
    ok_button = types.InlineKeyboardButton("✅",callback_data=f"quote_ok_{index+1}")
    markup = types.InlineKeyboardMarkup()
    if index > 0 and index < max_len:
        markup.row( prev_button, next_button )
    elif index > 0:
        markup.add( prev_button )
    elif index < max_len:
        markup.add( next_button )
    markup.row( no_button, ok_button )

    return markup

def create_inline_buttons_random_quote():

    random_button = types.InlineKeyboardButton("🆕",callback_data="random_quote")
    markup = types.InlineKeyboardMarkup()
    markup.add( random_button )

    return markup

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

@bot.callback_query_handler(func=lambda call: call.data.startswith("quote_next"))
def callback_next(call):
    new_quotes = functions.get_all_new_quotes()
    # Получаем индекс следующего элемента
    index = int(call.data.split("_")[2])
    if index < len(new_quotes):
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text = new_quotes[index][1],
                              reply_markup = create_quote_inline_buttons(index, len(new_quotes)))

@bot.callback_query_handler(func=lambda call: call.data.startswith("quote_no"))
def callback_next(call):

    functions.deny_quote(call.message.text)

    new_quotes = functions.get_all_new_quotes()
    # Получаем индекс следующего элемента
    index = int(call.data.split("_")[2])
    if index < len(new_quotes):
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text = new_quotes[index][1],
                              reply_markup = create_quote_inline_buttons(index, len(new_quotes)))
    else:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text = 'Предложений больше нет')

@bot.callback_query_handler(func=lambda call: call.data.startswith("quote_ok"))
def callback_next(call):

    functions.new_quote(call.message.text)
    functions.deny_quote(call.message.text)

    new_quotes = functions.get_all_new_quotes()
    # Получаем индекс следующего элемента
    index = int(call.data.split("_")[2])
    if index < len(new_quotes):
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text = new_quotes[index][1],
                              reply_markup = create_quote_inline_buttons(index, len(new_quotes)))
    else:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text = 'Предложений больше нет')

@bot.callback_query_handler(func=lambda call: call.data.startswith("quote_next"))
def callback_next(call):
    new_quotes = functions.get_all_new_quotes()
    # Получаем индекс следующего элемента
    index = int(call.data.split("_")[2])
    if index < len(new_quotes):
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text = new_quotes[index][1],
                              reply_markup = create_quote_inline_buttons(index, len(new_quotes)))

@bot.callback_query_handler(func=lambda call: call.data.startswith("quote_prev"))
def callback_prev(call):
    new_quotes = functions.get_all_new_quotes()
    # Получаем индекс следующего элемента
    index = int(call.data.split("_")[2])
    if index > 0:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = new_quotes[index][1], reply_markup = create_quote_inline_buttons(index, len(new_quotes)))

@bot.callback_query_handler(func=lambda call: call.data.startswith("random_quote"))
def callback_random_quote(call):

    bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text = functions.get_random_quote(),
                              reply_markup = create_inline_buttons_random_quote())

bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть
