import unittest
from tools.commandParser import CommandParser

class TestCommandParser(unittest.TestCase):

    def test_main(self):
        cases = (
            ("/test", True, "test", None),
            ("/test aa", True, "test", "aa"),
            ("test", False, None, None),
            ("test aa", False, None, None),
            ("/test@", True, "test", None),
            ("/test@ aa", True, "test", "aa"),
            ("/test@toto", True, "test", None),
            ("/test@toto aa", True, "test", "aa"),
            ("/t", False, None, None),
            ("/t aa", False, None, None),
        )
        cmds = ("test")
        cmd = CommandParser(cmds)
        for case in cases:
            r = cmd.parse(case[0])
            self.assertEqual(r.isValid, case[1], case[0] + " IsValid")
            self.assertEqual(r.command, case[2], case[0] + " command")
            self.assertEqual(r.args, case[3], case[0] + " args")
