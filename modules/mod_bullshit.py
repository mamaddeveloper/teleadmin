from modules.module_base import ModuleBase
import requests
from lxml import html

class ModuleBullshit(ModuleBase):
    URL = "http://www.randomyoutubecomment.com/"
    XPATH = '//div[@id="comment"]/a/span/text()'
    MAX = 10

    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "ModuleRandShit"

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "randshit":
            args = commandStr.split(" ")
            n = 0
            if args[0] != '':
                try:
                    n = int(args[0])
                    n = abs(n)
                except ValueError:
                    self.bot.sendMessage("/randshit : Argument must be an integer, %s is not !"%args[0], chat['id'])
            else:
                n = 1

            if n > self.MAX:
                n = self.MAX
                self.bot.sendMessage("Max randshit messages limited to %d"%self.MAX, chat['id'])

            for i in range(0, n):
                response = requests.get(self.URL)
                parsed_body = html.fromstring(response.text)

                randshit = parsed_body.xpath(self.XPATH)
                self.bot.sendMessage(randshit, chat['id'])

    def get_commands(self):
        return [
            ("randshit", "Random youtube comments. Optional argument 'N' Number of randshit to return (limited to 10)"),
        ]

