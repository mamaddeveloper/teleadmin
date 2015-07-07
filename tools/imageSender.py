import requests
from lxml import html
from urllib.parse import urljoin
from urllib.request import urlopen, urlretrieve

class ImageSender:
    @staticmethod
    def send_image(bot, chat, url, xpath, name, name_xpath=None):
        response = requests.get(url)
        parsed_body = html.fromstring(response.text)
        print(response.text)
        print("xpath %s" % xpath)
        image = parsed_body.xpath(xpath)
        if name_xpath:
            name = parsed_body.xpath(name_xpath)
        image = urljoin(response.url, image[0])
        urlretrieve(image, "out.jpg")
        bot.sendPhoto(chat, "out.jpg", name)
