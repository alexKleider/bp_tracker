#!/usr/bin/env python3

# File tests.py

import unittest
import bp_tracker

infile = 'data/bp_numbers.txt'


def incriment_by3values(sums, values):
    """Note side effect on <sums>."""
    for n in range(len(values)):
        sums[n] += values[n]


def collect_averages(infile):
    """
    By collecting the same data in a different way we can
    continue testing inspite of data changing constantly.
    """
    with open(infile, 'r') as stream:
        denominator = 0
        totals = [0, 0, 0]
        for line in stream:
            if line:
                parts = [int(val) for val in line.split()[:3]]
                incriment_by3values(totals, parts)
                denominator += 1
    return [total/denominator for total in totals]  


class TestBpTracker(unittest.TestCase):

    def test_averaging(self):
        averages = collect_averages(infile)
        print(averages)
        self.assertEqual(tuple(averages),
                bp_tracker.averages(
                    bp_tracker.array_from_file(infile))
                )

if __name__ == '__main__':
    unittest.main()
