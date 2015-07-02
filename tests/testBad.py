from tools.bad import Bad
import unittest
import os.path

class TestBad(unittest.TestCase):
    FILE = os.path.join(os.path.dirname(__file__), "../modules/resources/bad.txt")

    CASES = (
        ("tamer", False),
        ("tamere", True),
        ("a tamere", True),
        ("tamere a", True),
        ("a tamere a", True),
    )

    def test_main(self):
        b = Bad(self.FILE)
        for case in self.CASES:
            text, sup = case
            bad = b.bad(text)
            self.assertEqual(len(bad) > 0, sup, text + " / " + repr(bad))
