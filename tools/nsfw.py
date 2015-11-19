import json
import requests
from lxml import html
from urllib.parse import urljoin
from urllib.request import urlretrieve
import os.path

class Nsfw:
    def __init__(self, logger):
        self.logger = logger
        with open(os.path.join(os.path.dirname(__file__), "../modules/resources/bonjours.json")) as file:
            self.bonjours = json.load(file)
        self.keywords = (
            "random",
            "last"
        )

    def image(self, key, mode):
        parsed_body = None
        xpath = None
        url = None
        try:
            bonjour = self.bonjours[key]
            if isinstance(bonjour["xpath"], str):
                xpath = bonjour["xpath"]
            else:
                xpath = bonjour["xpath"][mode]
            url = bonjour["urls"][mode]
            message = bonjour["title"]

            response = None
            loop = 5
            while loop > 0:
                response = requests.get(url, allow_redirects=False)
                redirect = response.headers.get("location")
                if redirect:
                    url = urljoin(url, redirect)
                    url = url.encode("Latin-1")
                    url = url.decode("UTF-8")
                    loop -= 1
                else:
                    loop = 0
            parsed_body = html.fromstring(response.text)

            image = parsed_body.xpath(xpath)

            # Convert any relative urls to absolute urls
            url = urljoin(response.url, image[0])

            return NsfwDownloadResult(True, message, url)
        except:
            self.logger.exception("Bonjour fail %s %s %s", url, xpath, parsed_body, exc_info=True)
            return NsfwDownloadResult(False, "Fucking random website crash", None)

    def parse(self, commandStr):
        if commandStr == "":
            return None
        mode = "random"
        known = []
        unknown = []
        for key in commandStr.split(" "):
            if key in self.keywords:
                mode = key
            elif key in self.bonjours:
                known.append(key)
            else:
                unknown.append(key)
        return NsfwParserResult(mode, known, unknown)


class NsfwParserResult:
    def __init__(self, mode, known, unknown):
        self.__mode = mode
        self.__known = known
        self.__unknown = unknown

    def mode(self):
        return self.__mode

    def known(self):
        return self.__known

    def unknown(self):
        return self.__unknown


class NsfwDownloadResult:
    def __init__(self, ok, message, url):
        self.__ok = ok
        self.__message = message
        self.__url = url

    def ok(self):
        return self.__ok

    def message(self):
        return self.__message

    def url(self):
        return self.__url
