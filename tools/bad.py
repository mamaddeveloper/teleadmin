from tools.fileList import FileList
import re

class Bad:
    def __init__(self, path):
        self.lines = FileList(path)

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
            self.lines.add(word)

    def remove(self, word):
        if self.__invalid(word):
            return
        word = word.lower()
        if word in self.lines:
            self.lines.remove(word)
