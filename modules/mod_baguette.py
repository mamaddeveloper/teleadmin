from bot import Bot
from modules.module_base import ModuleBase
from random import randrange

class ModuleBaguette(ModuleBase):
    NUMBER_REPORT_MESSAGES = 5 + 1
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleBaguette"
        self.people = []
        self.sentences = list([line.rstrip('\n') for line in open("modules/resources/bag.txt")])

    def notify_text(self, message_id, from_attr, date, chat, text):
        super().notify_text(message_id, from_attr, date, chat, text) #module will use both notify_text and notify_command functions
        name = from_attr["first_name"].lower()
        if name in self.people:
            text = name + " " + self.sentences[randrange(len(self.sentences))]
            self.bot.sendMessage(text, chat["id"])

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        commandStr = commandStr.lower()
        if commandName == "bag":
            if not commandStr in self.people:
                self.people.append(commandStr)
        elif commandName == "sbag":
            if commandStr in self.people:
                self.people.remove(commandStr)