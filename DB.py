import sqlite3
import json
import env_utils
def get_connection():
        
    current_tokken = env_utils.get_tokken_value('TOKEN_BOT')
    test_tokken = env_utils.get_tokken_value('TOKEN_BOT_TEST')
    
    if current_tokken == test_tokken:
        return sqlite3.connect('Test.db')
    else:
        return sqlite3.connect('Prod.db')

def init():
    
    with open('quote.json', 'r+', encoding='utf-8') as file:
        quotes = json.load(file)
    
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Quotes (
    id INTEGER PRIMARY KEY,
    quote TEXT NOT NULL
    )
    ''')
    
    for quote in quotes['quotes']:
        cursor.execute( 'SELECT * FROM Quotes WHERE quote = ?',(quote['quote'],))
        result = cursor.fetchone()
        if result == None or result[1] != quote['quote']:
            cursor.execute('INSERT INTO Quotes (id, quote) VALUES (?, ?)', (quote['id'],quote['quote']))
        
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    user TEXT PRIMARY KEY,
    chat_id INTEGER NOT NULL,
    jija_today INTEGER NOT NULL,
    admin INTEGER NOT NULL
    )
    ''')
    
    connection.commit()
    connection.close()
    

def get_user_info(username):
    
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute( 'SELECT * FROM Users WHERE user = ?', (username,))
    result = cursor.fetchone()
    
    connection.close()
    
    return result

def get_admins():
    
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute( 'SELECT user FROM Users WHERE admin = ?', (1,))
    result = cursor.fetchall()
    
    connection.close()
    
    return result

def get_users():
    
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute( 'SELECT user, chat_id FROM Users' )
    result = cursor.fetchall()
    
    connection.close()
    
    return result

def new_user(username, chat_id, jija_today, admin):
    
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute('INSERT INTO Users (user, chat_id, jija_today, admin) VALUES (?, ?, ?, ?)', (username, chat_id, jija_today,admin))
    connection.commit()
    
    connection.close()

def check_user_admin_rights(username):
    
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute( 'SELECT user FROM Users WHERE user = ? and admin = 1', (username,))
    result = cursor.fetchone()
    
    connection.close()
    
    return result

def is_saved_user(username):
    
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute( 'SELECT user FROM Users WHERE user = ?', (username,))
    result = cursor.fetchone()
    
    connection.close()
    
    return result

def get_quotes():
    
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute( 'SELECT * FROM Quotes')
    result = cursor.fetchall()
    
    connection.close()
    
    return result

def check_and_toggle_user_jija(username):
    
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute( 'SELECT jija_today FROM Users WHERE user = ?', (username,))
    result = cursor.fetchone()
    
    if result[0] == 0:
        cursor.execute('UPDATE Users SET jija_today = 1 WHERE user = ?', (username,))
        connection.commit()
        
    connection.close()
    
    return result

def reset_jija():
    
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute('UPDATE Users SET jija_today = 0 WHERE jija_today = 1')
    connection.commit()
    
    connection.close()
    
    

    