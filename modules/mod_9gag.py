from modules.module_base import ModuleBase
import requests
from lxml import html
from urllib.parse import urljoin

class Module9GAG(ModuleBase):
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "Module9GAG"

    def getImage(self, chat):
        try:
            response = requests.get("http://9gag.com/random/")
            parsed_body = html.fromstring(response.text)

            image = parsed_body.xpath('//img[@class="badge-item-img"]/@src')
            imageAlt = parsed_body.xpath('//img[@class="badge-item-img"]/@alt')

            # Convert any relative urls to absolute urls
            image = urljoin(response.url, image[0])

            self.bot.sendPhotoUrl(chat, image, imageAlt)
        except Exception as e:
            self.logger.exception("9gag error", exc_info=True)
            self.bot.sendMessage("9gag error", chat)

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "9gag":
            self.getImage(chat["id"])

    def get_commands(self):
        return [
            ("9gag", "Get 9gag random image"),
        ]
