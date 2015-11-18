from tools.isType import is_type
from datetime import datetime
from datetime import timedelta


class ILimitator:
    def clear(self):
        raise NotImplementedError()

    def next(self, user, amout=1):
        raise NotImplementedError()

class Limitator(ILimitator):
    ALL_USER = {"id": -1}

    def __init__(self, per_time_unit, time_unit_seconds, per_user=False):
        is_type(int, per_time_unit, "per_time_unit")
        is_type(int, time_unit_seconds, "time_unit_seconds")
        is_type(int, per_user, "per_user")
        self.delta = timedelta(seconds=time_unit_seconds)
        self.per_time_unit = per_time_unit
        self.per_user = per_user
        self.users = None
        self.allUser = None
        self.clear()

    def clear(self):
        if self.per_user:
            self.users = []
        else:
            self.allUser = LimitatorUser(self.ALL_USER)

    def next(self, user, amount=1):
        is_type(dict, user, "user")
        is_type(int, amount, "amout")
        u = self.get_user(user)

        #clear old tiems
        now = datetime.now()
        u.items = list([i for i in u.items if now - i <= self.delta])

        if len(u.items) + amount > self.per_time_unit:
            raise LimitatorLimitted()
        else:
            for i in range(amount):
                u.items.append(now)


    def get_user(self, user):
        if self.per_user:
            users = [u for u in self.users if u.is_user(user)]
            if len(users) > 0:
                return users[0]
            else:
                u = LimitatorUser(user)
                self.users.append(u)
                return u
        else:
            return self.allUser


class LimitatorUser:
    def __init__(self, user):
        self.id = self.get_user_id(user)
        self.items = []

    def is_user(self, user):
        return self.id == self.get_user_id(user)

    @staticmethod
    def get_user_id(user):
        return user["id"]


class LimitatorMultiple(ILimitator):
    def __init__(self, *args):
        [is_type(ILimitator, a, "args") for a in args]
        self.limitators = list(args)

    def next(self, user, amout=1):
        error = False
        for limitator in self.limitators:
            try:
                limitator.next(user, amout)
            except LimitatorLimitted:
                error = True
        if error:
            raise LimitatorLimitted()

    def clear(self):
        for limitator in self.limitators:
            limitator.clear()


class LimitatorLimitted(Exception): pass
