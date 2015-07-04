import requests
from lxml import html

class Vdm:
    URL_BASE = "https://www.viedemerde.fr/"

    def last(self):
        return self.get()

    def random(self):
        return self.get("aleatoire")

    def get(self, url=""):
        try:
            response = requests.get(self.URL_BASE + url)
            parsed_body = html.fromstring(response.text)
            xpath = '//div[@class="post article"]/p'
            return "".join([a.text for a in parsed_body.xpath(xpath)[0]])
        except:
            return "Fail to get VDM."
