#!/usr/bin/env python3

# File tests.py

import os
import os.path
import tempfile
import unittest

import bp_tracker

# Need to use specific files in each test, not an actual data file.
# That will let us do the averages.
infile = 'bp_numbers.txt'
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


# It is generally easier to put the data into the test. Relying on an 
# actual data file is fragile, it changes data and location.
# Try to keep the test as self-contained as possible. 
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

    stream = [
        "The quick brown fox",
        "   jumped over the moon",
        "    "
        "# but of course this is rediculous!",
        " # as is this.",
        "        indented => unindented line",
        ]

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.test_dir.cleanup()

    #def test_averaging(self):
    def test_averaging_from_file_with_good_data(self):
        # Using the below as a starting point, write two lines to the file.
        # You can hard code the 'averages' and not need the methods above.

        #test_file = os.path.join(self.test_dir.name, 'readable.file')
        #with open(test_file, 'w') as f:
        #  f.write("howdy\n")
        #self.assertTrue(bp_tracker.check_file(test_file, 'r'))

        averages = collect_averages(infile)
        self.assertEqual(tuple(averages),
                bp_tracker.averages(
                    bp_tracker.array_from_file(infile))
                )

    def test_averaging_from_file_with_comments(self):
        # Using the below as a starting point, write two good data  lines 
        # to the file, and two comment lines.
        # You can hard code the 'averages' and not need the methods above.

        #test_file = os.path.join(self.test_dir.name, 'readable.file')
        #with open(test_file, 'w') as f:
        #  f.write("howdy\n")
        #self.assertTrue(bp_tracker.check_file(test_file, 'r'))
        print("running test_averaging_from_file_with_comments")

        averages = collect_averages(infile)
        self.assertEqual(tuple(averages),
                bp_tracker.averages(
                    bp_tracker.array_from_file(infile)))


#   def test_average(self):
#       #!!! there is no 'def average()' function.
#       #!!! I assume you mean 'def list_average(l)' function.

    def test_list_average(self):
        # Isolate the average function, and test it.
        self.assertEqual(1, 2)
        print("running test_list_average")
        lists = (
            ([],                   0),
            ([1, 2, 3, 4],         2.5),
            (['1', '2', '3', '4'], 2.5),
            (['5', 5],             5),
            ((1, 2, 3, 4, 5, 6, 7), 0),   # this should fail!!! 4
            )
        for l in lists:
            self.assertEqual(list_average(l[0]), l[1])

    def test_list_high_low(self):
        pass

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


    def test_useful_lines(self):  # (stream, comment="#"):
        expected = [
        "The quick brown fox",
        "jumped over the moon",
        "# but of course this is rediculous!",
        "# as is this.",
        "indented => unindented line",
            ]
        self.assertEqual([line for line in
                bp_tracker.useful_lines( self.stream, comment='')],
                expected)


    def test_useful_lines_without_comments(self):
        expected = [
        "The quick brown fox",
        "jumped over the moon",
        "indented => unindented line",
            ]
        self.assertEqual([line for line in bp_tracker.useful_lines(
                self.stream, comment='#')], expected)

    def test_array_from_file(self):
        # Write a test file with three lines of data, and test that the
        # returned list has a len of 3.
        pass

    def test_report(self):
        # Pass in hard coded data, test the result values.
        pass

    def test_print_report(self):
        # This one is a little trickier, but you just pass in data,
        # capture the output, split the output into a list of lines,
        # then test each line.
        pass

    def test_list_collations(self):
        # Pass in hard coded data, test the result values.
        pass

    def test_dict_for_display(self):
        # Pass in hard coded data, test the result values.
        pass

    def test_list_average(self):
        # Pass in hard coded data, test the result values.
        pass

    def test_list_high_low(self):
        # Pass in hard coded data, test the result values.
        pass

    def test_averages(self):
        # Pass in hard coded data, test the result values.
        pass

    def test_display_averages(self):
        # Pass in hard coded data, test the result.
        pass


class TestTestsAreRun(unittest.TestCase):
    def test_testing(self):
        print('In test_testing: about to fail!')
        self.assertEqual(1, 2)
    

if __name__ == '__main__':
    unittest.main()
