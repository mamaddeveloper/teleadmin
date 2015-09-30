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
        elif commandName == "fetchsandwich":
            if len(commandStr) > 0 :
                text = "%s offre un sandwich à %s" % (from_attr["first_name"], commandStr)
            else:
                text = "Bon appetit, %s" % from_attr["first_name"]
            self.bot.sendPhoto(chat["id"], "modules/resources/sandwich.jpg", text)

    def get_commands(self):
        return [
            ("fetchbeer", "Fetches some beer."),
            ("fetchsandwich", "Fetches some sandwich. Optional keyword name"),
        ]
