from bot import Bot
from modules.module_base import ModuleBase
import requests
from lxml import html
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.request import urlopen, urlretrieve

class ModuleNSFW(ModuleBase):
    
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "NSFW"
        

    def getBonjourImage(self, chatId, site, xpath_):
        response = requests.get(site)
        parsed_body = html.fromstring(response.text)
        print(parsed_body)
        image = parsed_body.xpath(xpath_)
        
        # Convert any relative urls to absolute urls
        image = urljoin(response.url, image[0])
        
        urlretrieve(image, "out.jpg") #works with static address
        
        self.bot.sendPhoto(chatId, "out.jpg", "Bonjour madame")


    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "bonjour":
            if "madame" in commandStr:
                if "last" in commandStr:
                    self.getBonjourImage(chat["id"], 'http://www.bonjourmadame.fr/',       '//div[@class="photo post"]/a/img/@src')
                elif "random" in commandStr:
                    self.getBonjourImage(chat["id"], 'http://www.bonjourmadame.fr/random', '//div[@class="photo post"]/a/img/@src')

                    

