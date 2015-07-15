from modules.module_base import ModuleBase

from tools import bad

class ModuleBadWords(ModuleBase):
    NUMBER_REPORT_MESSAGES = 5 + 1
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleBadWords"
        self.bad = bad.Bad("modules/resources/bad.txt")

    def notify_text(self, message_id, from_attr, date, chat, text):
        bads = self.bad.bad(text)

        if len(bads) > 0:
            text = "Surveille ton language, " + from_attr["first_name"] + "\n--> " + ", ".join(bads)
            self.bot.sendMessage(text, chat["id"])

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "bad":
            self.bad.add(commandStr)
        elif commandName == "notbad":
            self.bad.remove(commandStr)
