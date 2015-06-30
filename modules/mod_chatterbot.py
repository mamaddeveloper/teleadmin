from modules.module_base import ModuleBase
from bot import Bot
from chatterbot import ChatBot


class ModuleChatterBot(ModuleBase):

    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ChatterBot"
        self.chatbot = ChatBot("Ron Obvious", database='modules/resources/chatterbot.db')