from modules.module_base import ModuleBase
from datetime import datetime
class ModuleTimeleft(ModuleBase):
    DATES = {
        "rendu": datetime(2015, 7, 14, 17, 00),
        "budapest": datetime(2015, 7, 16, 14, 00),
        "défences": datetime(2015, 8, 17, 00, 00),
        "diplome": datetime(2015, 10, 19, 18, 00),
    }

    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleTimeleft"

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "timeleft":
            if commandStr == "all":
                for date in self.DATES:
                    diff = self.DATES[date] - datetime.today()
                    text = "Il reste %s jusqu'à %s" % (diff, date)
                    self.bot.sendMessage(text, chat["id"])
                return
            elif commandStr in self.DATES:
                diff = self.DATES[commandStr] - datetime.today()
                text = "Il reste %s jusqu'à %s" % (diff, commandStr)
            else:
                text = "Echéance %s inconnue" % commandStr
            self.bot.sendMessage(text, chat["id"])
        elif commandName == "date":
            if commandStr == "all":
                for d in self.DATES:
                    date = self.DATES[d]
                    text = "Date %s : %s" % (d, date)
                    self.bot.sendMessage(text, chat["id"])
                return
            elif commandStr in self.DATES:
                date = self.DATES[commandStr]
                text = "Date %s : %s" % (commandStr, date)
            else:
                text = "Date %s inconnue" % commandStr
            self.bot.sendMessage(text, chat["id"])