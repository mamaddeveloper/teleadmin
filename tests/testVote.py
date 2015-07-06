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

    def test_no_vote_State(self):
        v = VoteManager()
        try:
            v.state()
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

    def test_change_count(self):
        v = VoteManager()
        v.start({"id" : 123}, "test")
        v.vote({"id" : 123}, True)
        r = v.state()
        r.votesAgainst += 10
        r.voteCount += 10
        r = v.close({"id" : 123})
        self.assertEqual(r.voteCount, 1)
        self.assertEqual(r.votesFor, 1)
        self.assertEqual(r.votesAgainst, 0)
        self.assertEqual(r.rate, 1)

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
            result = v.state()
            self.assertEqual(result.name, name)
            self.assertEqual(result.votesFor, 2)
            self.assertEqual(result.votesAgainst, 4)
            self.assertEqual(result.voteCount, 6)
            self.assertFalse(result.end)
            self.assertEqual(result.rate, 2/6)
            result = v.close({"id" : 123})
            self.assertEqual(result.name, name)
            self.assertEqual(result.votesFor, 2)
            self.assertEqual(result.votesAgainst, 4)
            self.assertEqual(result.voteCount, 6)
            self.assertTrue(result.end)
            self.assertEqual(result.rate, 2/6)
