from modules.module_base import ModuleBase
from tools.nsfw import Nsfw
from tools.limitator import Limitator, LimitatorLimitted, LimitatorMultiple

class ModuleNSFW(ModuleBase):
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "NSFW"
        self.nsfw = Nsfw(self.logger)
        self.limitator = LimitatorMultiple(
            Limitator(5, 60, True),
            Limitator(50, 600, False),
        )

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "bonjour":
            if commandStr == "":
                text = "Bonjours : %s" % ", ".join(self.nsfw.bonjours)
                self.bot.sendMessage(text, chat["id"])
                return
            parserResult = self.nsfw.parse(commandStr)
            if len(parserResult.unknown()) > 0:
                self.bot.sendMessage("bonjour '%s' not found" % "', '".join(parserResult.unknown()), chat["id"])
            try:
                for key in parserResult.known():
                    self.limitator.next(from_attr)
                    result = self.nsfw.image(key, parserResult.mode())
                    if result.ok():
                        self.bot.sendPhotoUrl(chat["id"], result.url(), result.message())
                    else:
                        self.bot.sendMessage(result.message(), chat["id"])
            except LimitatorLimitted:
                self.bot.sendMessage("N'abuse pas mon petit cochon !", chat["id"])


    def get_commands(self):
        return [
            ("bonjour", "Bonjour. Keywords: <%s> <last/random>" % "/".join(self.nsfw.bonjours)),
        ]
