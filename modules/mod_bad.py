from modules.module_base import ModuleBase

from tools import bad

class ModuleBaguette(ModuleBase):
    NUMBER_REPORT_MESSAGES = 5 + 1
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleBaguette"
        self.bad = bad.Bad("modules/resources/bad.txt")

    def notify_text(self, message_id, from_attr, date, chat, text):
        bads = self.bad.bad(text)

        if len(bads) > 0:
            text = "Surveille ton language, " + from_attr["first_name"] + "\n--> " + ", ".join(bads)
            self.bot.sendMessage(text, chat["id"])
