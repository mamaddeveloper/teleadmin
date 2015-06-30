from modules.module_base import ModuleBase
from bot import Bot
import sqlite3


class ModuleConversationListener(ModuleBase):
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ConversationListener"
        self.connexion = sqlite3.connect('modules/resources/conversations.db')
        self.cursor = self.connexion.cursor()
        self.listUserId = self.getListUserId()

    def getListUserId(self):
        self.cursor.execute('SELECT user.id_user FROM user')
        listrows = self.cursor.fetchall()
        print(listrows)
        return listrows

    def insertUser(self, from_attr):
        self.cursor.execute('INSERT INTO user (id_user, first_name, last_name, username) VALUES (?,?,?,?)',
                            (from_attr['id'], from_attr['first_name'], from_attr['last_name'], from_attr['username']))
        pass

    def insertMessage(self, message_id, from_attr, date, chat, text):
        if from_attr["id"] not in self.listUserId:
            self.insertUser(from_attr)

        self.cursor.execute('INSERT INTO message (id_message, id_user, id_chat, date, text) VALUES (?,?,?,?,?)',
                            (message_id, from_attr['id'], chat['id'], date, text))

        pass

    # if you need both notify_text AND notify_command, don't forget to call super().notify_text(message_id, from_attr, date, chat, text) at the beginning of the inherited notify_text function
    def notify_text(self, message_id, from_attr, date, chat, text):
        self.insertMessage(message_id, from_attr, date, chat, text)
        pass

    def stop(self):
        self.connexion.commit()
        self.connexion.close()