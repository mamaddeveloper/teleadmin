from modules.module_base import ModuleBase
from tools.nsfw import Nsfw
import random
from tools.lines import LinesSeqRnd


class ModuleRandom(ModuleBase):
    RANDOM_MIN = 1
    RANDOM_MAX = 6
    CHALLENGE_MIN = 1
    CHALLENGE_MAX = 100
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleRandom"
        self.nsfw = Nsfw(self.logger)
        self.images_type = list([i for i in self.nsfw.bonjours.keys() if i != "monsieur"])

    def random(self, a, b, commandStr, chat, from_attr):
        try:
            n = int(commandStr)
            if n > b or n < a:
                self.error_msg(chat, a, b)
            else:
                c = random.randint(a, b)
                if c == n:
                    self.bot.sendMessage("%s win\nYou are such a coquin" % from_attr["first_name"], chat["id"])
                    for i in range(n):
                        image_type = random.choice(self.images_type)
                        result = self.nsfw.image(image_type, "random")
                        if result.ok():
                            self.bot.sendPhotoUrl(chat["id"], result.url(), result.message())
                        else:
                            self.bot.sendMessage(result.message(), chat["id"])
                else:
                    self.bot.sendMessage("%s : %d\nBot : %d\nYou loose !" % (from_attr["first_name"], n, c), chat["id"])
        except ValueError:
            self.error_msg(chat, a, b)

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "random":
            self.random(self.RANDOM_MIN, self.RANDOM_MAX, commandStr, chat, from_attr)
        elif commandName == "randomchallenger":
            self.random(self.CHALLENGE_MIN, self.CHALLENGE_MAX, commandStr, chat, from_attr)

    def error_msg(self, chat, a, b):
        self.bot.sendMessage("Value must be a int between %d and %d !" % (a, b), chat["id"])

    def get_commands(self):
        return [
            ("random", "Random [%d %d]" % (self.RANDOM_MIN, self.RANDOM_MAX)),
            ("randomchallenger", "Random [%d %d]" % (self.CHALLENGE_MIN, self.CHALLENGE_MAX)),
        ]
