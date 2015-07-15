from tools.fileList import FileList
import os.path

class AdminBase:
    def is_admin(self, user):
        raise NotImplementedError()


class AdminAll(AdminBase):
    def is_admin(self, user):
        return True

class Admin(AdminBase):
    FILE = os.path.join(os.path.dirname(__file__), "../modules/resources/admin.txt")

    def __init__(self):
        self.lines = FileList(self.FILE)

    def is_admin(self, user):
        return self.__get_id(user) in self.lines

    def add(self, current_user, user):
        if not self.is_admin(current_user):
            raise NotAdminException()
        self.lines.add(self.__get_id(user))

    def remove(self, current_user, user):
        if not self.is_admin(current_user):
            raise NotAdminException()
        self.lines.remove(self.__get_id(user))

    @classmethod
    def __get_id(cls, user):
        if isinstance(user, int):
            return str(user)
        if isinstance(user, str):
            return user
        elif isinstance(user, dict):
            return cls.__get_id(user["id"])
        else:
            print("%s is not valid user %s" % (user, type(user)))

class NotAdminException(Exception):
    pass
