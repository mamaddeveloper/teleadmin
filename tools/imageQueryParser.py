import random


class ImageQueryParser:
    def __init__(self):
        pass

    def parse(self, query_string):
        tab = query_string.split(" ")
        last = tab[-1].lower()
        is_random = False
        index = 0
        if last.startswith("-"):
            if last == "-r":
                is_random = True
                tab.pop()
            else:
                try:
                    index = int(last[1:])
                    tab.pop()
                except ValueError:
                    pass
        query_string = " ".join(tab)
        return ImageQuery(query_string, is_random, index)


class ImageQuery:
    def __init__(self, query, is_random, index):
        self.__query = query
        self.__is_random = is_random
        self.__index = index

    def query(self):
        return self.__query

    def is_random(self):
        return self.__is_random

    def next_index(self):
        if self.is_random():
            return random.randrange(0, 100)
        else:
            i = self.__index
            self.__index += 1
            return i
