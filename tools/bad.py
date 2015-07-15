from tools.lines import LinesAbstract
import re
import codecs

class Bad:
    def __init__(self, path):
        self.path = path
        self.lines = LinesAbstract(path).lines

    def bad(self, text):
        bads = []

        for word in re.findall("\w{2,}", text.lower(), re.UNICODE):
            if word in self.lines:
                bads.append(word)

        return bads

    @classmethod
    def __invalid(cls, word):
        return " " in word or len(word) <= 2

    def add(self, word):
        if self.__invalid(word):
            return
        word = word.lower()
        if word not in self.lines:
            self.lines.append(word)
            with codecs.open(self.path, "a", "UTF-8") as f:
                f.write(word + "\n")

    def remove(self, word):
        if self.__invalid(word):
            return
        word = word.lower()
        if word in self.lines:
            self.lines.remove(word)
            with codecs.open(self.path, "w", "UTF-8") as f:
                [f.write(w + "\n") for w in self.lines]