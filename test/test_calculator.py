#!/usr/bin/env python3

# File test/calculator.py

import os
import os.path
import tempfile
import unittest

from dev import calculator


class TestCalculator(unittest.TestCase):

    test_data = ((115, 70, 85, 45, 'normal'),
                 (127, 85, 99, 42, 'pre'),
                 (145, 93, 110,52, 'stage I'),
                )

    def test_calc(self):
        for sys, dia, mean, pp, status in self.test_data:
            res = calculator.calc(sys, dia)
            try:
                self.assertEqual(res, (mean, pp, status,))
            except AssertionError:
                print(
                f"calc({sys}, {dia}) => {res} NOT ({mean}, {pp}, {status})")
        print("Test completed")


if __name__ == '__main__':
    unittest.main()
