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

    # Return image
    def getRandomImage(self, chat):
        response = requests.get('http://xkcd.com/')#+ str(randint(1,1500)))
        parsed_body = html.fromstring(response.text)
        
        image = parsed_body.xpath('//*[@id="comic"]/img/@src')
        imageAlt = parsed_body.xpath('//*[@id="comic"]/img/@alt')
        imageTitle = parsed_body.xpath('//*[@id="comic"]/img/@title')[0]

        # Convert any relative urls to absolute urls
        image = urljoin(response.url, image[0])
        # Image downloaded
        #r = requests.get(image)
        #i = Image.open(StringIO(r.content))

        #i = urllib.Request(StringIO(r.content))
        #urllib.urlretrieve(StringIO(r.content), "out.jpg")
        #print (str(r.content, 'utf-8'))
        
        urlretrieve(image, "out.jpg") #works with static address
        
        #i = cStringIO.StringIO(r.content)
        #img = Image.open(file)
        
        #print("image size: " + i.size)

        #import urllib, cStringIO
        self.bot.sendPhoto(chat, "out.jpg", imageAlt)
        self.bot.sendMessage(imageTitle, chat)

        return

    def notify_command(self, message_id, from_attr, date, chat, commandName, commandStr):
         if commandName == "xkcd":
            self.getRandomImage(chat["id"])


