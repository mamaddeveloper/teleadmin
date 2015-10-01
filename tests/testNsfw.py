import unittest
from tools.nsfw import Nsfw
import logging


class TestNsfw(unittest.TestCase):
    def test_parse(self):
        nsfw = Nsfw(logging.getLogger("TestNsfw"))
        res = nsfw.parse("madame monsieur test")
        self.assertEqual(res.mode(), "random")
        self.assertEqual(res.known(), ["madame", "monsieur"])
        self.assertEqual(res.unknown(), ["test"])

    def name_mode(self, name, mode):
        nsfw = Nsfw(logging.getLogger("TestNsfw"))
        res = nsfw.image(name, mode, "../%s_%s.jpg" % (name, mode))
        self.assertTrue(res.ok())

    def test_madame_random(self):
        self.name_mode("madame", "random")

    #def test_madame_Last(self):
    #    self.name_mode("madame", "last")

    #def test_monsieur_random(self):
    #    self.name_mode("monsieur", "random")

    #def test_monsieur_last(self):
    #    self.name_mode("monsieur", "last")

    #def test_mademoiselle_random(self):
    #    self.name_mode("mademoiselle", "random")

    #def test_mademoiselle_last(self):
    #    self.name_mode("mademoiselle", "last")
