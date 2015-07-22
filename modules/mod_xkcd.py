from modules.module_base import ModuleBase
import requests
from lxml import html
from urllib.parse import urljoin
from urllib.request import urlretrieve

class ModuleXKCD(ModuleBase):
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "xkcd"

    def getXKCDImage(self, chat, path = "", prev=""):
        try:
            response = requests.get("http://%sxkcd.com/%s/" % (prev, path))
            parsed_body = html.fromstring(response.text)

            image = parsed_body.xpath('//*[@id="comic"]//img/@src')
            imageAlt = parsed_body.xpath('//*[@id="comic"]//img/@alt')
            imageTitle = parsed_body.xpath('//*[@id="comic"]//img/@title')[0]

            # Convert any relative urls to absolute urls
            image = urljoin(response.url, image[0])

            urlretrieve(image, "out.jpg") #works with static address

            self.bot.sendPhoto(chat, "out.jpg", imageAlt)
            self.bot.sendMessage(imageTitle, chat)
        except Exception as e:
            print(e)
            self.bot.sendMessage("xkcd error", chat)

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "xkcd":
            if commandStr == "last":
                self.getXKCDImage(chat["id"])
            elif commandStr == "random" or commandStr == "":
                self.getXKCDImage(chat["id"], "/random/comic", "c.")
            elif commandStr.isnumeric():
                self.getXKCDImage(chat["id"], int(commandStr))
            else:
                self.bot.sendMessage("Bad arguments for xkcd", chat["id"])
