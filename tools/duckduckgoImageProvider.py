from tools.imageProvider import ImageProvider
from tools.imageQueryParser import ImageQuery
from tools.isType import is_type
import logging
import requests


class DuckDuckGoImagesProvider(ImageProvider):
    URL = "https://duckduckgo.com/i.js?q=%s&s=%d"

    def __init__(self):
        ImageProvider.__init__(self)
        self.logger = logging.getLogger("DuckDuckGoImagesProvider")

    def get_image(self, query_result):
        is_type(ImageQuery, query_result, query_result)
        try:
            i = query_result.next_index()
            search_url = self.URL % (query_result.query(), i)
            self.logger.info("search_url '%s'", search_url)
            response = requests.get(search_url)
            self.logger.debug("Response %s", response.text)
            obj_json = response.json()
            self.logger.debug("Json %s", obj_json)
            return obj_json["results"][0]["image"]
        except:
            self.logger.exception("Fail query '%s'", query_result.query(), exc_info=True)
            return False
