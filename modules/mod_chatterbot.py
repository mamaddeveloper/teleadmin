from modules.module_base import ModuleBase
from bot import Bot
from chatterbot import ChatBot
from random import randint



class ModuleChatterBot(ModuleBase):
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ChatterBot"
        self.chatbot = ChatBot("Ron Obvious", database='modules/resources/chatterbot.db')

    def notify_text(self, message_id, from_attr, date, chat, text):
        if from_attr['first_name'] != 'DLMBot':
            print(text + from_attr['first_name'])
            response = self.chatbot.get_response(text, from_attr['first_name'])
            if randint(100) > 50:
                self.bot.sendMessage(response, chat['id'])
