from tools.vote import *
import unittest

class TestVote(unittest.TestCase):

    def test_double_start(self):
        v = VoteManager()
        v.start({"id" : 123}, "a")
        try:
            v.start({"id" : 123}, "b")
            self.fail()
        except OngoingVoteException:
            pass

    def test_no_vote(self):
        v = VoteManager()
        try:
            v.vote({"id":123}, False)
            self.fail()
        except NoVoteException:
            pass

    def test_no_vote_close(self):
        v = VoteManager()
        try:
            v.close({"id" : 123})
            self.fail()
        except NoVoteException:
            pass

    def test_double_vote(self):
        user = {"id": 123}
        v = VoteManager()
        v.start(user, "test")
        v.vote(user, True)
        try:
            v.vote(user, True)
            self.fail()
        except AlreadyVoteException:
            pass

    def test_global(self):
        name = "test"
        v = VoteManager()
        for i in range(2):
            v.start({"id" : 123}, name)
            v.vote({"id": 1}, False)
            v.vote({"id": 2}, False)
            v.vote({"id": 3}, True)
            v.vote({"id": 4}, True)
            v.vote({"id": 5}, False)
            v.vote({"id": 6}, False)
            result = v.close({"id" : 123})
            self.assertEqual(result.name, name)
            self.assertEqual(result.votesFor, 2)
            self.assertEqual(result.votesAgainst, 4)
