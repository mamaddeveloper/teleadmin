from modules.module_base import ModuleBase
from tools.nsfw import Nsfw
import random

class ModuleRandom(ModuleBase):
    RANDOM_MIN = 1
    RANDOM_MAX = 6
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleRandom"
        self.nsfw = Nsfw(self.logger);

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        commandStr = commandStr.lower()
        if commandName == "random":
            try:
                n = int(commandStr)
                if n > self.RANDOM_MAX or n < self.RANDOM_MIN:
                    self.error_msg(chat)
                else:
                    b = random.randint(self.RANDOM_MIN, self.RANDOM_MAX)
                    if b == n:
                        type = random.choice(list(self.nsfw.bonjours.keys()))
                        self.bot.sendMessage("You win, getting %d %s" % (b, type), chat["id"])
                        for i in range(n):
                            result = self.nsfw.image(type, "random", "out.jpg")
                            if result.ok():
                                self.bot.sendPhoto(chat["id"], "out.jpg", result.message())
                            else:
                                self.bot.sendMessage(result.message(), chat["id"])
                    else:
                        self.bot.sendMessage("You loose ! (%d)" % b, chat["id"])
            except ValueError:
                self.error_msg(chat)

    def error_msg(self, chat):
        self.bot.sendMessage("Value must be a int between %d and %d !" % (self.RANDOM_MIN, self.RANDOM_MAX), chat["id"])


    def get_commands(self):
        return [
            ("random", "Random [%d %d]" % (self.RANDOM_MIN, self.RANDOM_MAX)),
        ]