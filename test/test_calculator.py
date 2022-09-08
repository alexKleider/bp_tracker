#!/usr/bin/env python3

# File test/calculator.py

import os
import os.path
import tempfile
import unittest

from dev import aha


class TestCalculator(unittest.TestCase):

    test_data = ((115, 70, 85, 45, 'Normal BP'),
                 (127, 85, 99, 42, 'Pre-hypertension'),
                 (145, 93, 110,52, 'Stage I hypertension'),
                )

    def test_calc(self):
        for sys, dia, mean, pp, status in self.test_data:
            res = aha.calc(sys, dia)
            try:
                self.assertEqual(res, (mean, pp, status,))
            except AssertionError:
                print(
                f"calc({sys}, {dia}) => {res} NOT ({mean}, {pp}, {status})")
        print("Test completed")


if __name__ == '__main__':
    unittest.main()
