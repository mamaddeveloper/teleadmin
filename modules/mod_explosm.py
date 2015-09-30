from modules.module_base import ModuleBase
from tools.imageSender import ImageSender

class ModuleExplosm(ModuleBase):
    URL = "https://explosm.net/comics/"
    XPATH = '//img[@id="main-comic"]/@src'

    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleExplosm"

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "explosm":
            if commandStr == "" or commandStr == "random":
                ImageSender.send_image(self.bot, chat["id"], self.URL + "random", self.XPATH, "Cyanide and Happiness")
            elif commandStr == "last":
                ImageSender.send_image(self.bot, chat["id"], self.URL + "latest", self.XPATH, "Cyanide and Happiness")
            else:
                self.bot.sendMessage("Command /%s %s unknown !" % (commandName, commandStr), chat["id"])

    def get_commands(self):
        return [
            ("explosm", "Cyanide and Happiness. Keywords : <last/random>"),
        ]
