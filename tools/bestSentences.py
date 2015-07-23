import json
import os.path
import random
import requests

class BestSentences:
    FILE = os.path.join(os.path.dirname(__file__), "../botTest/sentences")

    def __init__(self):
        self.sentences = ()

    def load(self):
        try:
            url = open(self.FILE).read()
            r = requests.get(url).content.decode("UTF-8")
            self.sentences = json.loads(r)
        except:
            raise BestSentencesLoadException()

    def get(self, key=None):
        if len(self.sentences) == 0:
            raise BestSentencesNotLoadedException()
        if key:
            key = key.lower()
            source = list([s for s in self.sentences if s["who"].lower() == key])
            if len(source) == 0:
                raise BestSentencesNotFoundException()
        else:
            source = self.sentences
        return random.choice(source)

class BestSentencesException(Exception): pass
class BestSentencesLoadException(Exception): pass
class BestSentencesNotLoadedException(Exception): pass
class BestSentencesNotFoundException(Exception): pass
