import random

class Probability:
    def __init__(self, rate):
        random.seed()
        self.rate = rate
        if isinstance(self.rate, int):
            self.rate = int(self.rate)
        elif not isinstance(self.rate, float):
            raise ValueError("rate is not a int")

    def next(self):
        return random.random() < self.rate
