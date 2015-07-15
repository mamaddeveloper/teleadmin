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
            if self.bot.admin.is_admin(from_attr):
                self.bad.add(commandStr)
                self.bot.sendMessage("Word added !")
            else:
                self.bot.sendMessage("You are not admin !", chat["id"])
        elif commandName == "notbad":
            if self.bot.admin.is_admin(from_attr):
                self.bad.remove(commandStr)
                self.bot.sendMessage("Word removed !")
            else:
                self.bot.sendMessage("You are not admin !", chat["id"])
