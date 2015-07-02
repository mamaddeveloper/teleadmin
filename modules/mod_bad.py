from modules.module_base import ModuleBase

from tools import lines, userList

class ModuleBaguette(ModuleBase):
    NUMBER_REPORT_MESSAGES = 5 + 1
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleBaguette"
        self.lines = userList.UserList()
        for l in lines.LinesAbstract("modules/resources/bad.txt").lines:
            self.lines.add(l)

    def notify_text(self, message_id, from_attr, date, chat, text):
        bads = []
        for word in text.split(" "):
            if word in self.lines:
                bads.append(word)
        if len(bads) > 0:
            text = "Surveille ton language, " + from_attr["first_name"] + "\n--> " + ", ".join(bads)
            self.bot.sendMessage(text, chat["id"])


