from bot import Bot
from modules.module_base import ModuleBase
import requests
from lxml import html
from urllib.parse import urlparse
from urllib.parse import urljoin
from random import randint
from urllib.request import urlopen, urlretrieve


class ModuleXKCD(ModuleBase):
    
    FILE_NAME = "modules/resources/xkcd.last"
    
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "xkcd"
        with open(ModuleXKCD.FILE_NAME, "r") as f:
            self.lastComic = int(f.readline())
        

    def getXKCDImage(self, chat, stringNumber = ""):
        response = requests.get('http://xkcd.com/'+stringNumber)#+ str(randint(1,1500)))
        parsed_body = html.fromstring(response.text)
        
        image = parsed_body.xpath('//*[@id="comic"]/img/@src')
        imageAlt = parsed_body.xpath('//*[@id="comic"]/img/@alt')
        imageTitle = parsed_body.xpath('//*[@id="comic"]/img/@title')[0]
        if(stringNumber == ""):
            ref = parsed_body.xpath("/html/body/div[2]/ul[2]/li[2]/a/@href")[0]
            if ref != "#":
                self.lastComic = int(ref[1:-1])+1
        # Convert any relative urls to absolute urls
        image = urljoin(response.url, image[0])
        
        urlretrieve(image, "out.jpg") #works with static address
        
        self.bot.sendPhoto(chat, "out.jpg", imageAlt)
        self.bot.sendMessage(imageTitle, chat)

    # Return image
    def getRandomImage(self, chat):
        self.getXKCDImage(chat, str(randint(1,self.lastComic)))

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "xkcd":
            if commandStr == "last":
                self.getXKCDImage(chat["id"], "")
            elif commandStr == "random":
                self.getRandomImage(chat["id"])
            elif commandStr.isnumeric():
                if int(commandStr) <= self.lastComic:
                    self.getXKCDImage(chat["id"], str(int(commandStr))+"/")
                    
    def stop(self):
        with open(ModuleXKCD.FILE_NAME, "w") as f:
            f.write(str(self.lastComic))

