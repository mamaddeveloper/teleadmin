from modules.module_base import ModuleBase
import requests
from lxml import html
from urllib.parse import urljoin
from urllib.request import urlretrieve

class ModuleNSFW(ModuleBase):
    
    def __init__(self, bot):
        ModuleBase.__init__(self, bot)
        self.name = "NSFW"

    def getBonjourImage(self, chatId, site, xpath_, message):
        response = requests.get(site)
        parsed_body = html.fromstring(response.text)
        print(parsed_body)
        image = parsed_body.xpath(xpath_)
        
        # Convert any relative urls to absolute urls
        image = urljoin(response.url, image[0])
        
        urlretrieve(image, "out.jpg") #works with static address
        
        self.bot.sendPhoto(chatId, "out.jpg", message)

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
        if commandName == "bonjour":
            if "madame" in commandStr:
                message = "Bonjour madame."
                xpath_ = '//div[@class="photo post"]//img/@src'
                if "last" in commandStr:
                    self.getBonjourImage(chat["id"], 'http://www.bonjourmadame.fr/',xpath_, message)
                elif "random" in commandStr:
                    try:
                        self.getBonjourImage(chat["id"], 'http://www.bonjourmadame.fr/random',xpath_, message)
                    except:
                        self.bot.sendMessage("Fucking random website crash", chat["id"])
            if "monsieur" in commandStr:
                message = "Bonjour monsieur."
                xpath_ =  '//div[@class="img"]/h1/img/@src'
                if "last" in commandStr:
                    self.getBonjourImage(chat["id"], 'http://www.bonjourmonsieur.fr/', xpath_, message)
                elif "random" in commandStr:
                    self.getBonjourImage(chat["id"], 'http://www.bonjourmonsieur.fr/monsieur/random.html', xpath_, message)
