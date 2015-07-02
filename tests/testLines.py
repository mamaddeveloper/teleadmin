from tools import lines
import unittest
import os.path

class TestLines(unittest.TestCase):
    FILE = os.path.join(os.path.dirname(__file__), "../modules/resources/bag.txt")
    N = 100

    def test_LinesRnd(self):
        self.do_test(lines.LinesRnd)

    def test_LinesSeq(self):
        self.do_test(lines.LinesSeq)

    def test_LinesSeqRnd(self):
        self.do_test(lines.LinesSeqRnd)

    def do_test(self, cl):
        l = cl(self.FILE)
        for i in range(self.N):
            next(l)