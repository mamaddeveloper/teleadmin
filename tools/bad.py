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

    def add(self, word):
        if " " in word or len(word) <= 2:
            return
        word = word.lower()
        if word not in self.lines:
            self.lines.append(word)
            with codecs.open(self.path, "a", "UTF-8") as f:
                f.write(word + "\n")
