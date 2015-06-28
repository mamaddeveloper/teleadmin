from bot import Bot
from modules.module_base import ModuleBase

class ModuleTroll(ModuleBase):
    NUMBER_REPORT_MESSAGES = 5 + 1
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleTroll"
        self.reportedPeople = {}
    
    def notify_text(self, message_id, from_attr, date, chat, text):
        super().notify_text(message_id, from_attr, date, chat, text) #module will use both notify_text and notify_command functions
        name = from_attr["first_name"]
        if name in self.reportedPeople.keys():
            self.reportedPeople[name] = self.reportedPeople[name] - 1
            if self.reportedPeople[name] == -1:
                del self.reportedPeople[name]
            elif self.reportedPeople[name] != ModuleTroll.NUMBER_REPORT_MESSAGES -1:
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
            if commandStr in self.reportedPeople.keys():
                self.reportedPeople[commandStr] = self.reportedPeople[commandStr] + ModuleTroll.NUMBER_REPORT_MESSAGES
            else:
                self.reportedPeople[commandStr] = ModuleTroll.NUMBER_REPORT_MESSAGES