from bot import Bot
from modules.module_base import ModuleBase
from tools.userCount import UserCount

class ModuleTroll(ModuleBase):
    NUMBER_REPORT_MESSAGES = 5
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleTroll"
        self.reportedPeople = UserCount(self.NUMBER_REPORT_MESSAGES)

    def notify_text(self, message_id, from_attr, date, chat, text):
        name = from_attr["first_name"]
        if self.reportedPeople.has(name):
            text = name + ", t'es un vieux zgeg. HUEHUEHUEHUEHUE"
            self.bot.sendMessage(text, chat["id"])
                
    def notify_new_chat_participant(self, message_id, from_attr, date, chat, new_chat_participant):
        text = "Tiens, un nouveau zgeg, bienvenue "+ new_chat_participant["first_name"] + "!"
        self.bot.sendMessage(text, chat["id"])
        
    def notify_left_chat_participant(self, message_id, from_attr, date, chat, left_chat_participant):
        text = left_chat_participant["first_name"] + " qui s'en va, bon débarras!"
        self.bot.sendMessage(text, chat["id"])
        
    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "report":
            text = commandStr + " me report u\nHUEHUEHUEHUEHUE\nHUEHUEHUEHUEHUE\nHUEHUEHUEHUEHUE"        
            self.bot.sendMessage(text, chat["id"])
            self.reportedPeople.add(commandStr)
