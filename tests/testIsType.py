# -*- coding: utf-8 -*-
from tools.isType import is_type
import unittest

class TestIsType(unittest.TestCase):
    def test_1(self):
        is_type(str, "asf", "test_1")
        try:
            is_type(str, 1, "test_1")
            self.fail("No error")
        except ValueError:
            pass

    def test_2(self):
        is_type(int, 1, "test_2")
        try:
            is_type(int, "a", "test_2")
            self.fail("No error")
        except ValueError:
            pass

