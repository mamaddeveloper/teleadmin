from modules.module_base import ModuleBase
from tools.nsfw import Nsfw


class ModuleNSFW(ModuleBase):
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "NSFW"
        self.nsfw = Nsfw(self.logger)

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "bonjour":
            if commandStr == "":
                text = "Bonjours : %s" % ", ".join(self.nsfw.bonjours)
                self.bot.sendMessage(text, chat["id"])
                return
            parserResult = self.nsfw.parse(commandStr)
            if len(parserResult.unknown()) > 0:
                self.bot.sendMessage("bonjour '%s' not found" % "', '".join(parserResult.unknown()), chat["id"])
            for key in parserResult.known():
                result = self.nsfw.image(key, parserResult.mode(), "out.jpg")
                if result.ok():
                    self.bot.sendPhoto(chat["id"], "out.jpg", result.message())
                else:
                    self.bot.sendMessage(result.message(), chat["id"])

    def get_commands(self):
        return [
            ("bonjour", "Bonjour. Keywords: <%s> <last/random>" % "/".join(self.nsfw.bonjours)),
        ]
