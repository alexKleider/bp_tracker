#!/usr/bin/env python3

# File tests.py

import os
import os.path
import tempfile
import unittest

import bp_tracker

# Need to use specific files in each test, not an actual data file.
# That will let us do the averages.
infile = 'data/bp_numbers.txt'
# We assume there is such a data file, the more entries the better.
#non_existent_file = "ghostfile"  # our nonexistent file
#empty_file = "empty"  # our empty file

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

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.test_dir.cleanup()

    def test_averaging(self):
        averages = collect_averages(infile)
        self.assertEqual(tuple(averages),
                bp_tracker.averages(
                    bp_tracker.array_from_file(infile))
                )


    def test_averaging_only_last_few(self):
        for n in range(7):
            averages = collect_averages(infile)[-7:]
            self.assertEqual(tuple(averages),
                bp_tracker.averages(
                    bp_tracker.array_from_file(infile)), n
                )


    def test_check_file_readable_file(self):
        test_file = os.path.join(self.test_dir.name, 'readable.file')
        with open(test_file, 'w') as f:
          f.write("howdy\n")
        self.assertTrue(bp_tracker.check_file(test_file, 'r'))


    def test_check_file_writeable_file(self):
        test_file = os.path.join(self.test_dir.name, 'writeable.file')
        with open(test_file, 'w') as f:
          f.write("howdy\n")
        self.assertTrue(bp_tracker.check_file(test_file, 'w'))

    def test_check_file_writeable_dir(self):
        test_dir_writeable = os.path.join(self.test_dir.name, 'writeable')
        os.mkdir(test_dir_writeable)
        os.chmod(test_dir_writeable, 0o777)
        test_file = os.path.join(test_dir_writeable, 'missing.file')
        self.assertTrue(bp_tracker.check_file(test_file, 'w'))

    def test_check_file_read_missing_file(self):
        test_dir_unwriteable = os.path.join(self.test_dir.name, 'unwriteable')
        os.mkdir(test_dir_unwriteable)
        os.chmod(test_dir_unwriteable, 0o000)
        test_file = os.path.join(test_dir_unwriteable, 'missing.file')
        self.assertFalse(bp_tracker.check_file(test_file, 'w'))
  
    def test_check_file_write_unwriteable_file(self):
        test_file = os.path.join(self.test_dir.name, 'bad_file.txt')
        with open(test_file, 'w') as f:
            f.write("bleagh")
        os.chmod(test_file, 0o000) 
        self.assertFalse(bp_tracker.check_file(test_file, 'w'))

    def test_check_file_write_unwriteable_dir(self):
        test_dir_unwriteable = os.path.join(self.test_dir.name, 'unwriteable')
        os.mkdir(test_dir_unwriteable)
        os.chmod(test_dir_unwriteable, 0o00)
        test_file = os.path.join(test_dir_unwriteable, 'bad_dir.file')
        self.assertFalse(bp_tracker.check_file(test_file, 'w'))


if __name__ == '__main__':
    unittest.main()
