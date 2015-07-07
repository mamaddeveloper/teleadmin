from modules.module_base import ModuleBase
from datetime import datetime
class ModuleTimeleft(ModuleBase):
    DATES = {
        "rendu": datetime(2015, 7, 14, 17, 00),
        "budapest": datetime(2015, 7, 15, 14, 00),
        "défences": datetime(2015, 8, 17, 00, 00),
        "diplome": datetime(2015, 10, 19, 18, 00),
    }

    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleTimeleft"

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "timeleft":
            if commandStr in self.DATES:
                diff = self.DATES[commandStr] - datetime.today()
                text = "Il reste %s jusqu'à %s" % (diff, commandStr)
            else:
                text = "Echéance %s inconnue" % commandStr
            self.bot.sendMessage(text, chat["id"])
