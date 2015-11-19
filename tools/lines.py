import random
import codecs

class LinesAbstract:
    def __init__(self, path_or_list):
        if isinstance(path_or_list, str):
            self.lines = list([line.strip() for line in codecs.open(path_or_list, "r", "utf-8")])
        else:
            self.lines = list(path_or_list)
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
