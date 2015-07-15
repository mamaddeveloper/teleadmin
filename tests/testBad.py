# -*- coding: utf-8 -*-
from tools.bad import Bad
import unittest
import os.path
import uuid

class TestBad(unittest.TestCase):
    FILE = os.path.join(os.path.dirname(__file__), "../modules/resources/bad.txt")

    CASES = (
        ("tame", False),
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

    def test_add_remove(self):
        word = str(uuid.uuid4()).replace("-", "")
        print(word)
        b = Bad(self.FILE)
        bad = b.bad(word)
        self.assertEqual(len(bad), 0)
        print(len(b.lines))
        b.add(word)
        print(len(b.lines))
        bad = b.bad(word)
        self.assertEqual(len(bad), 1)
        b.remove(word)
        bad = b.bad(word)
        self.assertEqual(len(bad), 0)
