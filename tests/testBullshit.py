import unittest
from tools.bullshit import *
from tools.isType import is_type


class TestBullshit(unittest.TestCase):
    N = 20

    def test_1(self):
        b = Bullshit()
        for i in range(self.N):
            s = next(b)
            is_type(str, s, "s")

    def test_2(self):
        b = Bullshit()
        for i in range(self.N):
            s = b.next()
            is_type(str, s, "s")

    def test_3(self):
        b = Bullshit()
        for i in range(self.N):
            s = b.__next__()
            is_type(str, s, "s")
