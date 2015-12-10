import unittest
from tools.imageQueryParser import *


class TestImageQueryParser(unittest.TestCase):
    CASES = (
        ("bonjour salut", "bonjour salut", False, 0),
        ("bonjour salut -r", "bonjour salut", True, 0),
        ("bonjour salut -5", "bonjour salut", False, 5),
        ("bonjour salut -c", "bonjour salut -c", False, 0),
    )

    def test(self):
        p = ImageQueryParser()
        for case in self.CASES:
            r = p.parse(case[0])
            self.assertEqual(r.query(), case[1], case[0])
            self.assertEqual(r.is_random(), case[2], case[0])
            if not case[2]:
                self.assertEqual(r.next_index(), case[3], case[0])
