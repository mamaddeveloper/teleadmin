import unittest
from tools.dtc import Dtc

class TestDtc(unittest.TestCase):
    N = 10

    def test_last(self):
        dtc = Dtc()
        for i in range(self.N):
            self.valid(dtc.last())

    def test_random(self):
        dtc = Dtc()
        for i in range(self.N):
            self.valid(dtc.random())

    def valid(self, text):
        self.assertTrue(len(text) > 10, text)
