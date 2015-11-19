import requests
from lxml import html
from urllib.parse import urljoin

class ImageSender:
    @staticmethod
    def send_image(bot, chat, url, xpath, name, name_xpath=None):
        response = requests.get(url)
        parsed_body = html.fromstring(response.text)
        image = parsed_body.xpath(xpath)
        if name_xpath:
            name = parsed_body.xpath(name_xpath)
        image = urljoin(response.url, image[0])
        bot.sendPhotoUrl(chat, image, name)
