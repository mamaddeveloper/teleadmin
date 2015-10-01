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

    def image(self, key, mode, image_dest):
        parsed_body = None
        xpath = None
        site = None
        try:
            bonjour = self.bonjours[key]
            if isinstance(bonjour["xpath"], str):
                xpath = bonjour["xpath"]
            else:
                xpath = bonjour["xpath"][mode]
            site = bonjour["urls"][mode]
            message = bonjour["title"]

            response = requests.get(site)
            parsed_body = html.fromstring(response.text)

            image = parsed_body.xpath(xpath)

            # Convert any relative urls to absolute urls
            image = urljoin(response.url, image[0])

            urlretrieve(image, image_dest) #works with static address

            return NsfwDownloadResult(True, message)
        except:
            self.logger.exception("Bonjour fail %s %s %s", site, xpath, parsed_body, exc_info=True)
            return NsfwDownloadResult(False, "Fucking random website crash")

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
    def __init__(self, ok, message):
        self.__ok = ok
        self.__message = message

    def ok(self):
        return self.__ok

    def message(self):
        return self.__message
