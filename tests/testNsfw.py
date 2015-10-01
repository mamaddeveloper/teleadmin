import unittest
from tools.nsfw import Nsfw
import logging


class TestNsfw(unittest.TestCase):
    PARSE_ARGS = (
        ("madame monsieur test", "random", ["madame", "monsieur"], ["test"]),
        ("madame random monsieur test", "random", ["madame", "monsieur"], ["test"]),
        ("madame last test", "last", ["madame"], ["test"]),
    )
    def test_parse(self):
        nsfw = Nsfw(logging.getLogger("TestNsfw"))
        for arg in self.PARSE_ARGS:
            res = nsfw.parse(arg[0])
            self.assertEqual(res.mode(), arg[1], "mode for '%s'" % arg[0])
            self.assertEqual(res.known(), arg[2], "known for '%s'" % arg[0])
            self.assertEqual(res.unknown(), arg[3], "unknown for '%s'" % arg[0])

    def name_mode(self, name, mode):
        n = 5 if mode == "random" else 1
        nsfw = Nsfw(logging.getLogger("TestNsfw"))
        for i in range(n):
            res = nsfw.image(name, mode, "../out.jpg")
            self.assertTrue(res.ok())

    def test_madame_random(self):
        self.name_mode("madame", "random")

    def test_madame_last(self):
        self.name_mode("madame", "last")

    def test_monsieur_random(self):
        self.name_mode("monsieur", "random")

    def test_monsieur_last(self):
        self.name_mode("monsieur", "last")

    def test_mademoiselle_random(self):
        self.name_mode("mademoiselle", "random")

    def test_mademoiselle_last(self):
        self.name_mode("mademoiselle", "last")
