from modules.module_base import ModuleBase

from tools import lines, userList

class ModuleBaguette(ModuleBase):
    NUMBER_REPORT_MESSAGES = 5 + 1
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleBaguette"
        self.users = userList.UserList()
        self.lines = lines.LinesSeqRnd("modules/resources/bag.txt")

    def notify_text(self, message_id, from_attr, date, chat, text):
        super().notify_text(message_id, from_attr, date, chat, text) #module will use both notify_text and notify_command functions
        name = from_attr["first_name"]
        if name in self.users:
            text = name + " " + next(self.lines)
            self.bot.sendMessage(text, chat["id"])

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        commandStr = commandStr.lower()
        if commandName == "bag":
            self.users.add(commandStr)
        elif commandName == "sbag":
            self.users.remove(commandStr)