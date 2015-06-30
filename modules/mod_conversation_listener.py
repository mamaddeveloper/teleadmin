from modules.module_base import ModuleBase
from bot import Bot
import sqlite3


class ModuleConversationListener(ModuleBase):
    NUM_MESSAGES_BEFORE_COMMIT = 10

    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ConversationListener"
        self.initConnection()
        self.listUserId = []
        self.counter = 0

    def initConnection(self):
        try:
            print("Opened database successfully")
            self.connexion = sqlite3.connect('modules/resources/conversations.db')
            self.cursor = self.connexion.cursor()
            self.listUserId = self.getListUserId()
        except:

            with open("modules/resources/conversations.db"):
                pass
            print("Created database successfully")

            self.connexion = sqlite3.connect('modules/resources/conversations.db')
            self.cursor = self.connexion.cursor()

            self.cursor.execute(
                "CREATE TABLE 'message' ( 'id_message'	INTEGER NOT NULL, 'id_user'	INTEGER NOT NULL, 'id_chat'	INTEGER NOT NULL, 'date' INTEGER, 'text' TEXT )")
            self.cursor.execute(
                "CREATE TABLE 'user' ('id_user'	INTEGER, 'first_name'	TEXT, 'last_name'	TEXT, 'username'	TEXT )")
            print("Table created successfully")

            self.connexion.commit()


    def getListUserId(self):
        self.cursor.execute('SELECT user.id_user FROM user')
        listrows = self.cursor.fetchall()
        print(listrows)
        return listrows

    def insertUser(self, from_attr):

        # Check if username and lastname are not set in Telegram
        if not ModuleBase.checkForAttribute(from_attr, 'username'):
            from_attr['username'] = from_attr['first_name']
        if not ModuleBase.checkForAttribute(from_attr, 'last_name'):
            from_attr['last_name'] = from_attr['first_name']

        # Insert user in DB
        self.cursor.execute('INSERT INTO user (id_user, first_name, last_name, username) VALUES (?,?,?,?)',
                            (from_attr['id'], from_attr['first_name'], from_attr['last_name'], from_attr['username']))

        self.connexion.commit()

        # Add user in listUserID
        self.listUserId.append(from_attr['id'])

    def insertMessage(self, message_id, from_attr, date, chat, text):
        if from_attr["id"] not in self.listUserId:
            self.insertUser(from_attr)

        self.cursor.execute('INSERT INTO message (id_message, id_user, id_chat, date, text) VALUES (?,?,?,?,?)',
                            (message_id, from_attr['id'], chat['id'], date, text))
        self.counter += 1
        self.counter %= ModuleConversationListener.NUM_MESSAGES_BEFORE_COMMIT

        if self.counter == 0:
            self.connexion.commit()

    # if you need both notify_text AND notify_command, don't forget to call super().notify_text(message_id, from_attr, date, chat, text) at the beginning of the inherited notify_text function
    def notify_text(self, message_id, from_attr, date, chat, text):
        self.insertMessage(message_id, from_attr, date, chat, text)
        pass

    def stop(self):
        self.connexion.commit()
        self.connexion.close()
