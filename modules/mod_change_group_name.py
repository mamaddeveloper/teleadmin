from bot import Bot
from modules.module_base import ModuleBase

class ModuleChangeGroupName(ModuleBase):
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ChangeGroupName"
        
    def notify_new_chat_title(self, message_id, from_attr, date, chat, new_chat_title):
        self.bot.sendMessage("Quel nom de merde: " + new_chat_title, chat["id"])
        
    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "fetchbeer":
            self.bot.sendMessage( "C'est pas l'heure de boire mon ptit choupinet.\nRetourne coder.", chat["id"])
