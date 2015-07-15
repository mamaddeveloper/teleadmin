# -*- coding: utf-8 -*-
from tools.fileList import FileList
import unittest
import os.path
import uuid

class TestFileList(unittest.TestCase):
    FILE = os.path.join(os.path.dirname(__file__), "TestFileList.txt")

    def test_add_remove(self):
        word = str(uuid.uuid4()).replace("-", "")
        print(word)
        list = FileList(self.FILE)
        n = len(list)

        self.assertFalse(word in list)

        list.add(word)

        self.assertTrue(word in list)
        self.assertEqual(len(list), n + 1)

        list.remove(word)

        self.assertFalse(word in list)
        self.assertEqual(len(list), n)
