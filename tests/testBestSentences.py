import unittest
from tools.bestSentences import *

class TestBestSentences(unittest.TestCase):
    CASES = (
        ("piconche", 2),
        ("pocket", 5),
        (None, 2)
    )
    def test_main(self):
        b = BestSentences()

        try:
            b.get()
            self.fail("No error")
        except BestSentencesNotLoadedException:
            pass

        b.load()

        for c in self.CASES:
            for i in range(c[1]):
                b.get(c[0])

        try:
            b.get("yolo")
            self.fail("No error")
        except BestSentencesNotFoundException:
            pass
