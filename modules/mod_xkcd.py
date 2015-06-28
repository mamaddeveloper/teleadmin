from bot import Bot
from modules.module_base import ModuleBase
import requests
from lxml import html
import sys
from urllib.parse import urlparse
from urllib.parse import urljoin
from random import randint
from urllib.request import urlopen, urlretrieve


import io
#from StringIO import StringIO

class ModuleXKCD(ModuleBase):

    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "xkcd"

    def getXKCDImage(self, chat, stringNumber = ""):
        response = requests.get('http://xkcd.com/'+stringNumber)#+ str(randint(1,1500)))
        parsed_body = html.fromstring(response.text)
        
        image = parsed_body.xpath('//*[@id="comic"]/img/@src')
        imageAlt = parsed_body.xpath('//*[@id="comic"]/img/@alt')
        imageTitle = parsed_body.xpath('//*[@id="comic"]/img/@title')[0]

        # Convert any relative urls to absolute urls
        image = urljoin(response.url, image[0])
        
        urlretrieve(image, "out.jpg") #works with static address
        
        self.bot.sendPhoto(chat, "out.jpg", imageAlt)
        self.bot.sendMessage(imageTitle, chat)

    # Return image
    def getRandomImage(self, chat):
        self.getXKCDImage(chat, str(randint(1,1500)))

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "xkcd":
            #commandStr = commandStr[1:]
            print(commandStr)
            if commandStr == "last":
                self.getXKCDImage(chat["id"], "")
            elif commandStr == "random":
                self.getRandomImage(chat["id"])
            elif commandStr.isnumeric():
                if int(commandStr) <= 1542:
                    self.getXKCDImage(chat["id"], str(int(commandStr))+"/")


