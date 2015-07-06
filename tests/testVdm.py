import unittest
from tools.vdm import Vdm

class TestVdm(unittest.TestCase):
    N = 10

    def test_last(self):
        vdm = Vdm()
        for i in range(self.N):
            self.valid(vdm.last())

    def test_random(self):
        vdm = Vdm()
        for i in range(self.N):
            self.valid(vdm.random())

    def valid(self, text):
        self.assertTrue(text.startswith("Aujourd'hui"), text)
        self.assertTrue(text.endswith("VDM"), text)