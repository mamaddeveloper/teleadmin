import random
import codecs

class LinesAbstract:
    def __init__(self, path):
        self.lines = list([line.strip() for line in codecs.open(path, "r", "utf-8")])
        self.max = len(self.lines)

    def __next__(self):
        raise Exception("Abstract")

class LinesSeq(LinesAbstract):
    def __init__(self, path):
        super().__init__(path)
        self.__index = -1

    def __next__(self):
        self.__index += 1
        if self.__index >= self.max:
            self.__index = 0
        return self.lines[self.__index]

class LinesSeqRnd(LinesSeq):
    def __init__(self, path):
        super().__init__(path)
        random.shuffle(self.lines)

class LinesRnd(LinesAbstract):
    def __next__(self):
        return self.lines[random.randrange(self.max)]
