import unittest
from tools.userCount import UserCount

class TestUserCount(unittest.TestCase):
    def test_main(self):
        nb = 3
        cnt = UserCount(nb)
        user = "toto"
        self.assertFalse(cnt.has(user))
        cnt.add(user)
        for i in range(nb):
            self.assertTrue(cnt.has(user))
        self.assertFalse(cnt.has(user))
        cnt.add(user)
        cnt.add(user)
        for i in range(nb * 2):
            self.assertTrue(cnt.has(user))
        self.assertFalse(cnt.has(user))
