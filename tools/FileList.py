import codecs
import os.path

class FileList:
    def __init__(self, path):
        self.path = path
        if os.path.exists(path):
            self.list = list([line.strip() for line in codecs.open(path, "r", "utf-8")])
        else:
            self.list = []

    def __contains__(self, item):
        return self.key(item) in self.list

    def add(self, item):
        key = self.key(item)
        if not key in self.list:
            self.list.append(key)
            with codecs.open(self.path, "a", "UTF-8") as f:
                f.write(key + "\n")

    def remove(self, item):
        key = self.key(item)
        if key in self.list:
            self.list.remove(key)
            with codecs.open(self.path, "w", "UTF-8") as f:
                [f.write(w + "\n") for w in self.list]

    def __len__(self):
        return len(self.list)

    @classmethod
    def key(cls, item):
        return item.lower()

