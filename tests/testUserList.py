import unittest
from tools.userList import UserList

class TestUserList(unittest.TestCase):

    def test_main(self):
        list = UserList()
        self.assertFalse("toto" in list)
        list.add("toto")
        self.assertTrue("toto" in list)
        self.assertTrue("Toto" in list)
        self.assertEqual(list.set("toto"), None)
        list.set("toto", "faf")
        self.assertEqual(list.get("toto"), "faf")
        list.add("toto")
        self.assertEqual(list.get("toto"), "faf")
        list.add("toto", "dda")
        self.assertEqual(list.get("toto"), "dda")
        list.remove("toto")
        self.assertFalse("toto" in list)

