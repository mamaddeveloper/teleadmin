from modules.module_base import ModuleBase
from tools.nsfw import Nsfw
import random

class ModuleRandom(ModuleBase):
    RANDOM_MIN = 1
    RANDOM_MAX = 6
    CHALLENGE_MIN = 1
    CHALLENGE_MAX = 100
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleRandom"
        self.nsfw = Nsfw(self.logger)

    def random(self, a, b, commandStr, chat, from_attr):
        print("Raddnom a:%d b:%d cs:%s" % (a, b, commandStr))
        try:
            n = int(commandStr)
            if n > b or n < a:
                self.error_msg(chat, a, b)
            else:
                c = random.randint(a, b)
                print("b = %d" % c)
                if c == n:
                    image_type = random.choice(list(self.nsfw.bonjours.keys()))
                    self.bot.sendMessage("You win, getting %d %s\nYou are such a coquin" % (n, image_type), chat["id"])
                    for i in range(n):
                        result = self.nsfw.image(image_type, "random", "out.jpg")
                        if result.ok():
                            self.bot.sendPhoto(chat["id"], "out.jpg", result.message())
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
