import random
import codecs

def loadLines(path):
    return list([line.rstrip('\n') for line in codecs.open(path, "r", "utf-8")])

class LinesAbstract:
    def __init__(self, path):
        self.sentences = loadLines(path)
        self.max = len(self.sentences)
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
        return self.sentences[self.__index]

class LinesSeqRnd(LinesSeq):
    def __init__(self, path):
        super().__init__(path)
        random.shuffle(self.sentences)

class LinesRnd(LinesAbstract):
    def __next__(self):
        return self.sentences[random.randrange(self.max)]

if __name__ == '__main__':
    path = "../modules/resources/bag.txt"
    seq = LinesSeq(path)
    seqRnd  = LinesSeqRnd(path)
    rnd  = LinesRnd(path)
    for i in range(30):
        print(next(seq))
    print("############")
    for i in range(30):
        print(next(seqRnd))
    print("############")
    for i in range(30):
        print(next(rnd))