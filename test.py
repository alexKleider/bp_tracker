#!/usr/bin/env python3

# File tests.py

import unittest
import bp_tracker

test_data_file = "data/data4testing.txt"

data = bp_tracker.array_from_file(test_data_file)

class TestBpTracker(unittest.TestCase):

    def test_averaging(self):
        self.assertEqual((135, 67.5, 74), bp_tracker.averages(data))

if __name__ == '__main__':
    unittest.main()
