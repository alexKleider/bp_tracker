#!/usr/bin/env python3

# File test/tests.py

import os
import unittest

import bp_tracker

infile = 'data/bp_numbers.txt'
# We assume there is such a data file, the more entries the better.
non_existent_file = "ghostfile"  # our nonexistent file
empty_file = "empty"  # our empty file

# Begin with two helper functions:

def increment_sums_by_values(sums, values):
    """
    <sums> is an iterable of running totals.
    <values> is a same length iterable of values to be added to the
    corresponding values in <sums>.
    Note side effect on <sums>.
    """
    assert(len(sums) == len(values))
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
            if line and not line.startswith('#') :
                parts = [int(val) for val in line.split()[:3]]
                increment_sums_by_values(totals, parts)
                denominator += 1
    return [total/denominator for total in totals]  


class TestBpTracker(unittest.TestCase):

    def test_averaging(self):
        averages = collect_averages(infile)
#       print(averages)
        self.assertEqual(tuple(averages),
                bp_tracker.averages(
                    bp_tracker.array_from_file(infile))
                )


    def test_averaging_only_last_few(self):
        for n in range(7):
            averages = collect_averages(infile)[-7:]
#           print(averages)
            self.assertEqual(tuple(averages),
                bp_tracker.averages(
                    bp_tracker.array_from_file(infile)), n
                )


    # write tests for no, empty, good data & bad data files:

    def test_no_file(self):
        pass

    def test_empty_file(self):
        pass

    def test_good_data_file(self):
        pass

    def test_bad_data_file(self):
        pass

if __name__ == '__main__':
    unittest.main()
