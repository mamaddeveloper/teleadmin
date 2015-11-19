import requests
from lxml import html


class Bullshit:
    URL = "http://www.randomyoutubecomment.com/"
    XPATH = '//div[@id="comment"]/a/span/text()'

    def __next__(self):
        response = requests.get(self.URL)
        parsed_body = html.fromstring(response.text)
        return parsed_body.xpath(self.XPATH)[0]

    def next(self):
        return self.__next__()
