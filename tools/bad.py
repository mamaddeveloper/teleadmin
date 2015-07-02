from tools.lines import LinesAbstract
import re

class Bad:
    def __init__(self, path):
        self.lines = LinesAbstract(path).lines

    def bad(self, text):
        bads = []

        for word in re.findall("\w{2,}", text.lower(), re.UNICODE):
            if word in self.lines:
                bads.append(word)

        return bads
