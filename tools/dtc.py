import requests
from lxml import html

class Dtc:
    URL_BASE = "http://danstonchat.com/"

    def last(self):
        return self.get("latest.html")

    def random(self):
        return self.get("random0.html")

    def get(self, url=""):
        try:
            response = requests.get(self.URL_BASE + url)
            parsed_body = html.fromstring(response.text.replace("<br />", "\n"))
            xpath = '//div[@class="item-listing"]/div[1]/p/a'
            items = parsed_body.xpath(xpath)[0]
            return items.text_content()
        except ArithmeticError:
            return "Fail to get DTC."
