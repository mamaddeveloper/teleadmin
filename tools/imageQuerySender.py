from tools.imageQueryParser import ImageQueryParser
import logging


class ImageQuerySender:
    MAX = 3

    def __init__(self, bot, provider):
        self.bot = bot
        self.provider = provider
        self.parser = ImageQueryParser()
        self.logger = logging.getLogger("ImageQuerySender")

    def send_next(self, query_string, chat_id):
        query = self.parser.parse(query_string)

        n = 0

        while n < self.MAX:
            image = self.provider.get_image(query)
            if image:
                if self.bot.sendPhotoUrl(chat_id, image, query.query()):
                    return
            n += 1
        self.bot.sendMessage("No result for %s" % query.query(), chat_id)
        self.logger.error("To many loop for %s", query_string)
