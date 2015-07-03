import unittest
from tools.commandParser import CommandParser

class TestCommandParser(unittest.TestCase):

    def test_main(self):
        cases = (
            ("/test"            , True  , True  , "test"    , ""        ),
            ("/test aa"         , True  , True  , "test"    , "aa"      ),
            ("/test aa bb"      , True  , True  , "test"    , "aa bb"   ),
            ("atest"            , False , False , ""        , ""        ),
            ("#test"            , False , False , ""        , ""        ),
            ("test"             , False , False , ""        , ""        ),
            ("test aa"          , False , False , ""        , ""        ),
            ("/test@"           , True  , True  , "test"    , ""        ),
            ("/test@ aa"        , True  , True  , "test"    , "aa"      ),
            ("/test@toto"       , True  , True  , "test"    , ""        ),
            ("/test@toto aa"    , True  , True  , "test"    , "aa"      ),
            ("/t"               , False , False , ""        , ""        ),
            ("/t aa"            , False , False , ""        , ""        ),
            ("/toto"            , True  , False , "toto"    , ""        ),
            ("/toto aa"         , True  , False , "toto"    , "aa"      ),
        )
        cmds = ("test")
        cmd = CommandParser(cmds)
        for case in cases:
            r = cmd.parse(case[0])
            self.assertEqual(r.isValid  , case[1], case[0] + " isValid")
            self.assertEqual(r.isKnown  , case[2], case[0] + " isKnown")
            self.assertEqual(r.command  , case[3], case[0] + " command")
            self.assertEqual(r.args     , case[4], case[0] + " args")
