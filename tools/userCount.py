from tools.userList import UserList

class UserCount(UserList):
    def __init__(self, count):
        super().__init__()
        self.count = count

    def add(self, item, data=None):
        key = self.key(item)
        if key in self.dict:
            self.dict[key] += self.count
        else:
            self.dict[key] = self.count

    def set(self, item, data=None):
        self.add(item, data)

    def has(self, item):
        key = self.key(item)
        if key in self.dict:
            self.dict[key] -= 1
            if self.dict[key] < 0:
                self.remove(item)
                return False
            else:
                return True
        else:
            return False
