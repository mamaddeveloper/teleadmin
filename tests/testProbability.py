import unittest
from tools.probability import Probability

class TestProbability(unittest.TestCase):
    N = 1000
    DIFF = 5 / 100

    def test_one(self):
        p = Probability(1)
        for i in range(self.N):
            self.assertTrue(p.next())

    def test_zero(self):
        p = Probability(0)
        for i in range(self.N):
            self.assertFalse(p.next())

    def test_proba(self):
        rates = (
            0.25,
            0.5,
            0.75,
        )
        for rate in rates:
            p = Probability(rate)
            cnt = 0
            for i in range(self.N):
                if p.next():
                    cnt += 1
            self.assertAlmostEqual(cnt, self.N * rate, delta=self.N * self.DIFF)

    def test_arg(self):
        cases = (
            "1",
            (),
            {},
            None,
        )
        for case in cases:
            try:
                p = Probability(case)
                self.fail(repr(case))
            except ValueError:
                pass