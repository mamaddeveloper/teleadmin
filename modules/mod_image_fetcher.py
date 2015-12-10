from modules.module_base import ModuleBase
from tools.imageQuerySender import ImageQuerySender
from tools.duckduckgoImageProvider import DuckDuckGoImagesProvider
from tools.limitator import Limitator, LimitatorLimitted, LimitatorMultiple

#Module for fecthing an image on Google Image
class ModuleImageFetcher(ModuleBase):

    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleImageFetcher"
        self.limitator = LimitatorMultiple(
            Limitator(10, 900, True),
            Limitator(120, 60*60, False),
        )
        provider = DuckDuckGoImagesProvider()
        self.sender = ImageQuerySender(self.bot, provider)

    #Usage : /img query [--index | --random]
    #Example : /img cara -2
    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "img":
            if commandStr == "":
                self.bot.sendMessage("Not enough argument, usage : /img query [-index | -random]", chat["id"])
            else:
                try:
                    self.limitator.next(from_attr)
                except LimitatorLimitted:
                    self.bot.sendMessage("Tu as abusé, réssaye plus tard !", chat["id"])
                    return
                self.sender.send_next(commandStr, chat["id"])

    def get_commands(self):
        return [
            ("img", "Fetch an image on Google Image"),
        ]

