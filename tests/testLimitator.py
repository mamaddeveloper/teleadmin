# -*- coding: utf-8 -*-
from tools.limitator import *
import unittest
import time


class TestLimitator(unittest.TestCase):

    USER1 = {"id":1}
    USER2 = {"id":2}

    def test_1(self):
        l = Limitator(5, 2)
        for i in range(5):
            l.next(self.USER1)
        try:
            l.next(self.USER1)
            self.fail("must crash")
        except LimitatorLimitted:
            pass
        time.sleep(3)
        for i in range(2):
            l.next(self.USER1)
        time.sleep(1)
        for i in range(2):
            l.next(self.USER1)
        time.sleep(3)
        for i in range(5):
            l.next(self.USER1)
        try:
            l.next(self.USER1)
            self.fail("must crash")
        except LimitatorLimitted:
            pass

    def test_2(self):
        l = Limitator(5, 2, True)
        for i in range(5):
            l.next(self.USER1)
        for i in range(5):
            l.next(self.USER2)
        try:
            l.next(self.USER1)
            self.fail("must crash")
        except LimitatorLimitted:
            pass
        try:
            l.next(self.USER2)
            self.fail("must crash")
        except LimitatorLimitted:
            pass
        
    def test_3(self):
        l = Limitator(5, 2)
        l.next(self.USER1, 5)
        try:
            l.next(self.USER1)
            self.fail("must crash")
        except LimitatorLimitted:
            pass

    def test_4(self):
        l = Limitator(5, 2, True)
        l.next(self.USER1, 5)
        try:
            l.next(self.USER1)
            self.fail("must crash")
        except LimitatorLimitted:
            pass

    def test_5(self):
        l = Limitator(1, 61, True)
        l.next(self.USER1)
        try:
            l.next(self.USER1)
            self.fail("must crash")
        except LimitatorLimitted:
            pass
        time.sleep(62)
        l.next(self.USER1)
        try:
            l.next(self.USER1)
            self.fail("must crash")
        except LimitatorLimitted:
            pass

    def test_6(self):
        l = Limitator(5, 2, True)
        l.next(self.USER1, 3)
        try:
            l.next(self.USER1, 3)
            self.fail("must crash")
        except LimitatorLimitted:
            pass
        l.next(self.USER1, 2)

    def test_7(self):
        l1 = Limitator(5, 2, False)
        l2 = Limitator(5, 2, True)
        l = LimitatorMultiple(l1, l2)
        l.next(self.USER1, 3)
        l.next(self.USER2, 2)
        try:
            l.next(self.USER1, 1)
            self.fail("must crash")
        except LimitatorLimitted:
            pass

    def test_8(self):
        l1 = Limitator(5, 2, False)
        l2 = Limitator(3, 2, True)
        l = LimitatorMultiple(l1, l2)
        l.next(self.USER1, 3)
        l.next(self.USER2, 2)
        try:
            l.next(self.USER1, 1)
            self.fail("must crash")
        except LimitatorLimitted:
            pass

    def test_9(self):
        l1 = Limitator(5, 2, False)
        l2 = Limitator(3, 2, True)
        try:
            l = LimitatorMultiple(l1, l2, 1)
            self.fail("must crash")
        except ValueError:
            pass
