from modules.module_base import ModuleBase

from tools import lines, userList

class ModuleSlogan(ModuleBase):
    NUMBER_REPORT_MESSAGES = 5 + 1
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleSlogan"
        self.lines = lines.LinesSeqRnd("modules/resources/slogans.txt")

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        commandStr = commandStr.lower()
        if commandName == "slogan":
            self.bot.sendMessage(next(self.lines), chat["id"])