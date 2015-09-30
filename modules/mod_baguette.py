from modules.module_base import ModuleBase

from tools import lines, userList
from tools.probability import Probability

class ModuleBaguette(ModuleBase):
    NUMBER_REPORT_MESSAGES = 5 + 1
    RATE_BAG = 3/4
    RATE_NOT_BAG = 2/100

    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleBaguette"
        self.users = userList.UserList()
        self.lines = lines.LinesSeqRnd("modules/resources/bag.txt")
        self.probabilityBag = Probability(self.RATE_BAG)
        self.probabilityNotBag = Probability(self.RATE_NOT_BAG)

    def notify_text(self, message_id, from_attr, date, chat, text):
        name = from_attr["first_name"]
        if (name in self.users and self.probabilityBag.next()) or self.probabilityNotBag.next():
            text = name + " " + next(self.lines)
            self.bot.sendMessage(text, chat["id"])

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        commandStr = commandStr.lower()
        if commandName == "bag":
            self.users.add(commandStr)
        elif commandName == "sbag":
            self.users.remove(commandStr)

    def get_commands(self):
        return [
            ("bag", "Add baguette"),
            ("sbag", "Remove baguette"),
        ]