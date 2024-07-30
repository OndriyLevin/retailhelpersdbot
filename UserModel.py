import env_utils
import DB
import random

class User:
    def __init__(self, username, chat_id):
        if DB.is_saved_user(username):
            saved_user = DB.get_user_info(username)
            self.username = saved_user[0]
            self.chat_id = saved_user[1]
            self.jija_today = False
            self.admin = False
            if saved_user[2] == 1:
                self.jija_today = True
            if saved_user[3] == 1:
                self.admin = True
        else:
            self.username = username
            if username == env_utils.get_tokken_value('DEFAULT_ADMIN'):
                self.admin = True
            else:
                self.admin = False
            self.jija_today = False
            self.chat_id = chat_id
            
            self.save_to_db()
        
    def save_to_db(self):
        DB.new_user(self.username, self.chat_id, self.jija_today, self.admin)
    
    def jija_drinked(self):
        if DB.check_and_toggle_user_jija(self.username)[0] == 1:
            return True
        else:
            self.jija_today = True
            return False
        
    def what_white_jija(self):
        if self.jija_drinked():
            message = 'Ты уже запрашивал жижу, приходи завтра за новой'
        else:
            random_value = random.random() * 100
            if random_value < 10:
                message = 'Стакан выскальнул из рук и упал. Теперь неизвестно какая белая жижа была у тебя'
            if random_value > 10 and random_value < 50:
                message = 'В стакане ты чувствуешь кисловатый привкус. Жижа рабочая'
            if random_value > 50 and random_value < 95:
                message = 'В стакане ты чувствуешь сладкий привкус. Жижа не рабочая'
            if random_value > 95:
                message = '😏🍆💦'
    
        return message
            
        