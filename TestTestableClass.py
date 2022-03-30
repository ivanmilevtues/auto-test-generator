import unittest

from TestableClass import TestableClass


class TestSum(unittest.TestCase):

    def test_sum(self):
        tc = TestableClass(4, 2)
        self.assertEqual(tc.sum(), 6, "Should be 6")

    def test_sum_tuple(self):
        tc = TestableClass(-2, 2)
        self.assertEqual(tc.sum(), 0, "Should be 0")

if __name__ == '__main__':
    unittest.main()
