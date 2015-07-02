class UserList:
    def __init__(self):
        self.dict = {}

    def __contains__(self, item):
        return self.key(item) in self.dict

    def add(self, item, data=None):
        key = self.key(item)
        if not key in self.dict or data != None:
            self.dict[self.key(item)] = data

    def set(self, item, data=None):
        self.dict[self.key(item)] = data

    def remove(self, item):
        key = self.key(item)
        if key in self.dict:
            del self.dict[self.key(item)]

    def key(self, item):
        return item.lower()

    def get(self, item):
        return self.dict[self.key(item)]
