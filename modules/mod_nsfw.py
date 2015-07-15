from modules.module_base import ModuleBase
import requests
from lxml import html
from urllib.parse import urljoin
from urllib.request import urlretrieve
import json

class ModuleNSFW(ModuleBase):
    
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "NSFW"

        with open("modules/resources/bonjours.json") as file:
            self.bonjours = json.load(file)
        self.keywords = (
            "random",
            "last"
        )


    def getBonjourImage(self, chatId, site, xpath_, message):
        try:
            response = requests.get(site)
            parsed_body = html.fromstring(response.text)

            image = parsed_body.xpath(xpath_)

            # Convert any relative urls to absolute urls
            image = urljoin(response.url, image[0])

            urlretrieve(image, "out.jpg") #works with static address

            self.bot.sendPhoto(chatId, "out.jpg", message)
        except:
            self.bot.sendMessage("Fucking random website crash", chatId)

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "bonjour":
            types = []
            mode = "random"
            if commandStr == "":
                text = "Bonjours : %s" % ", ".join(self.bonjours)
                self.bot.sendMessage(text, chat["id"])
                return
            for key in commandStr.split(" "):
                if key in self.keywords:
                    mode = key
                else:
                    types.append(key)

            for type in types:
                if type in self.bonjours:
                    bonjour = self.bonjours[type]
                    if isinstance(bonjour["xpath"], str):
                        xpath = bonjour["xpath"]
                    else:
                        xpath = bonjour["xpath"][mode]
                    self.getBonjourImage(chat["id"], bonjour["urls"][mode], xpath, bonjour["title"])
                else:
                    self.bot.sendMessage("bonjour %s not found" % key, chat["id"])