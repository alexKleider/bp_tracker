#!/usr/bin/env python3

# File test/tests.py

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

to_test_ck4duplicate_tests = '''
def increment_sums_by_values(sums, values):
    """
    Include this redundant declaration just to check 
    that checking for duplicates actually works.
    """
    pass
'''

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

# And add a helper class:

class Collector(object):

    def __init__(self, lines=[]):
        self.lines = lines

    def write(self, text):
        self.lines.append(text)
        

# It is generally easier to put the data into the test.
# Relying on an actual data file is fragile,
# it changes data and location.
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
        # Using the below as a starting point,
        # write two lines to the file.
        # You can hard code the 'averages' and
        # not need the methods above.

#       test_file = os.path.join(self.test_dir.name,
#                                'readable.file')
#       with open(test_file, 'w') as f:
#          f.write("howdy\n")
#       self.assertTrue(bp_tracker.check_file(test_file, 'r'))

        averages = collect_averages(infile)
        averages = [round(avg) for avg in averages]
        self.assertEqual(averages,
                bp_tracker.averages(
                    bp_tracker.array_from_file(infile))
                )

    def test_averaging_from_file_with_comments(self):
        # Using the below as a starting point, write two good
        # data lines and two comment lines to the file,
        # You can hard code the 'averages' and
        # not need the methods above.

#       test_file = os.path.join(self.test_dir.name,
#                                'readable.file')
#       with open(test_file, 'w') as f:
#          f.write("howdy\n")
#       self.assertTrue(bp_tracker.check_file(test_file, 'r'))

        averages = collect_averages(infile)
        averages = [round(avg) for avg in averages]
        self.assertEqual(averages,
                bp_tracker.averages(
                    bp_tracker.array_from_file(infile)))


    def test_averaging_only_last_few(self):
        for n in range(7):
            averages = collect_averages(infile)[-7:]
            averages = [round(avg) for avg in averages]
            self.assertEqual(averages,
                bp_tracker.averages(
                    bp_tracker.array_from_file(infile)), n
                )


    def test_check_file_readable_file(self):
        test_file = os.path.join(self.test_dir.name,
                                 'readable.file')
        with open(test_file, 'w') as f:
            f.write("howdy\n")
        self.assertTrue(bp_tracker.check_file(test_file, 'r'))


    def test_check_file_writeable_file(self):
        test_file = os.path.join(self.test_dir.name, 'writeable.file')
        with open(test_file, 'w') as f:
          f.write("howdy\n")
        self.assertTrue(bp_tracker.check_file(test_file, 'w'))


    def test_check_file_writeable_dir(self):
        test_dir_writeable = os.path.join(self.test_dir.name,
                                          'writeable')
        os.mkdir(test_dir_writeable)
        os.chmod(test_dir_writeable, 0o777)
        test_file = os.path.join(test_dir_writeable,
                                 'missing.file')
        self.assertTrue(bp_tracker.check_file(test_file, 'w'))


    def test_check_file_read_missing_file(self):
        test_dir_unwriteable = os.path.join(self.test_dir.name,
                                            'unwriteable')
        os.mkdir(test_dir_unwriteable)
        os.chmod(test_dir_unwriteable, 0o000)
        test_file = os.path.join(test_dir_unwriteable,
                                 'missing.file')
        self.assertFalse(bp_tracker.check_file(test_file, 'w'))
  

    def test_check_file_write_unwriteable_file(self):
        test_file = os.path.join(self.test_dir.name,
                                 'bad_file.txt')
        with open(test_file, 'w') as f:
            f.write("bleagh")
        os.chmod(test_file, 0o000) 
        self.assertFalse(bp_tracker.check_file(test_file, 'w'))


    def test_check_file_write_unwriteable_dir(self):
        test_dir_unwriteable = os.path.join(self.test_dir.name,
                                            'unwriteable')
        os.mkdir(test_dir_unwriteable)
        os.chmod(test_dir_unwriteable, 0o00)
        test_file = os.path.join(test_dir_unwriteable,
                                 'bad_dir.file')
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
                bp_tracker.useful_lines(self.stream,
                                        comment='')],
                expected)


    def test_useful_lines_without_comments(self):
        expected = [
        "The quick brown fox",
        "jumped over the moon",
        "indented => unindented line",
            ]
        self.assertEqual([line for line in
            bp_tracker.useful_lines(self.stream, comment='#')],
            expected)


    def test_valid_data(self):
        bad = []
        lines_and_results = (
            ("110 59 68 20220809.1640", (110,59,68,20220809.1640)),
            ("124 62 62 20220810.0840", (124,62,62,20220810.0840)),
            ("134 63 57 20220812.0758", (134,63,57,20220812.0758)),
            ("134 62 57 20220812.1128", (134,62,57,20220812.1128)),
            ("100 59 62 20220812.1323", (100,59,62,20220812.1323)),
            ("total junk times four", None),
            ("to few components", None),
            ("to many all junk components", None),
            ("23 14 sixty 4.5", None),
            ("23 14 89 4.5 00", None),
                )
        for entry in lines_and_results:
            self.assertEqual(bp_tracker.valid_data(entry[0],bad),
                                entry[1])
        errors = [parts[0] for parts in lines_and_results
                    if parts[1] == None]
        self.assertEqual(bad, errors)
        pass


    def test_array_from_file(self):
        # Write a test file with three lines of data,
        # and test that the returned list has a len of 3.
        data = (
            "110 59 68 20220809.1640",
            "124 62 62 20220810.0840",
            "134 63 57 20220812.0758",
            "134 62 57 20220812.1128",
            "100 59 62 20220812.1323",
                )
        report_file = os.path.join(self.test_dir.name,
                                    'bp-data.txt')
        with open(report_file, 'w') as f:
            for line in data:
                f.write(line + "\n")
        res = bp_tracker.array_from_file(report_file)
        self.assertEqual(5, len(res))
        for tup in res:
            self.assertEqual(4, len(tup))


    def test_report(self):
        # Pass in hard coded data, test the result values.
        #! Note: the bp_tracker.report function is NOT used!
        data = [
            ('110', '59', '68', '20220812.1323'),
            ('124', '62', '62', '20220810.0840'),
            ('134', '63', '57', '20220812.0758'),
            ('134', '62', '57', '20220812.1128'),
            ('100', '59', '62', '20220809.1640'),
                ]
        res = bp_tracker.report(data)
        self.assertEqual(
            (
            ('134', '63', '57', '20220812.0758'),
            ('134', '63', '57', '20220812.0758'),
            ('110', '59', '68', '20220812.1323'),
            ('110', '59', '68', '20220812.1323'),
            ),
                    res)


    def test_format_report(self):
        # This one is a little trickier, but you just pass in data,
        # capture the output, split the output into a list of lines,
        # then test each line.
        #? why not simply assert results == expected
        #? rather than the two last lines??
          
        expected = [
            "          | Low  | High | Avg  |",
            "Systolic  | 110  | 134  | 122  |",
            "Diastolic |  59  |  63  |  61  |",
            "Pulse     |  59  | 110  |  84  |",
            ]
        results = bp_tracker.format_report(
            [134, 134, 110, 110],
            [63, 63, 59, 59],
            [59, 59, 110, 110],).split("\n")
        
        for line in range(0,4):
            assert results[line] == expected[line] 


    def test_list_collations(self):
        # Pass in hard coded data, test the result values.
        data = [ 
            [ 100, 80, 60 ],
            [ 110, 90, 70 ],
            [ 120, 100, 80 ],
        ]
        first, second, third = bp_tracker.list_collations(data)
        self.assertTrue(first == [100, 110, 120]) 
        self.assertTrue(second == [80, 90, 100])
        self.assertTrue(third  == [60, 70, 80])

    def test_dict_for_display(self):
        # Pass in hard coded data, test the result values.
        data = [ 
            [ 100, 80, 60 ],
            [ 110, 90, 70 ],
            [ 120, 100, 80 ],
        ]
        result = bp_tracker.dict_for_display(data)
        self.assertTrue(result['sl'] == 100)
        self.assertTrue(result['sh'] == 120)
        self.assertTrue(result['sa'] == 110)
        self.assertTrue(result['dl'] == 80)
        self.assertTrue(result['dh'] == 100)
        self.assertTrue(result['da'] == 90)
        self.assertTrue(result['pl'] == 60)
        self.assertTrue(result['ph'] == 80)
        self.assertTrue(result['pa'] == 70)



    def test_list_average(self):
        # Isolate the average function, and test it.
        lists = (
            ([],                   0),
            ([1, 2, 3, 4],         2),
            ([5, 5],             5),
            ((1, 2, 3, 4, 5, 6, 7), 29//7),
            )
        for l in lists:
            self.assertEqual(bp_tracker.list_average(l[0]), l[1])


    def test_list_low_high(self):
        # Pass in hard coded data, test the result values.
        self.assertTrue((70, 90) == bp_tracker.list_low_high([70, 80, 90]))

    def test_list_low_high_avg(self):
        # Pass in hard coded data, test the result values.
        self.assertTrue((70, 90, 80) == bp_tracker.list_low_high_avg([70, 80, 90]))


    def test_averages(self):
        # Pass in hard coded data, test the result values.
        self.assertTrue(80 == bp_tracker.list_average([70, 80, 90]))


    def test_display_averages(self):
        # Pass in hard coded data, test the result.
        expected = '110/90 70'
        result = bp_tracker.display_averages([110.345, 89.9, 70.41]) 
        self.assertTrue(result == expected)

##! The next tests pertain to AHA criteria.

    def test_get_category(self):
        for data in (
                [tuple(item.split()) for item in (
                    "49 s 0", "34 d 0", "50 s 1", "35 d 1",
                    "69 s 1", "39 d 1",
                    "70 s 2", "40 d 2", "89 s 2", "59 d 2",
                    "90 s 3", "60 d 3", "99 s 3", "64 d 3",
                    "100 s 4", "65  d 4", "120 s 4", "80  d 4",
                    "121 s 5", "81  d 5", "129 s 5", "84  d 5",
                    "130 s 6", "85  d 6", "139 s 6", "89  d 6",
                    "140 s 7", "90  d 7", "159 s 7", "99  d 7",
                    "160 s 8", "100 d 8", "179 s 8", "109 d 8",
                    "180 s 9", "110 d 9", "210 s 9", "120 d 9",
                    "211 s 10", "121 d 10",
                                    )]):
#           print("{} {} {} yields {}"
#               .format(data[0], data[1], data[2],
#               category.get_category(data[0], data[1])
#                   ))
            self.assertEqual(
                bp_tracker.get_category(data[0], data[1]),
                bp_tracker.categories[int(data[2])])


    def test_calc(self):
        for sys, dia, mean, pp, status in(
                (115, 70, 85, 45, 'Normal BP'),
                (127, 85, 99, 42, 'Pre-hypertension'),
                (145, 93, 110,52, 'Stage I hypertension'),
                ):
            res = bp_tracker.calc(sys, dia)
            self.assertEqual(res, (mean, pp, status,))


    def test_no_date_stamp(self):
        self.assertEqual(bp_tracker.no_date_stamp(
            (115, 67, 66, 20220914.0839)), None)
        self.assertEqual(bp_tracker.no_date_stamp(
            (115, 67, 66, 0.0)), True)


    def test_time_of_day_filter(self):
        self.assertEqual(bp_tracker.time_of_day_filter(
            (115, 67, 66, 20220914.0839), 800, 900), True)
        self.assertEqual(bp_tracker.time_of_day_filter(
            (115, 67, 66, 20220914.0839), 900, 1000), None)
        self.assertEqual(bp_tracker.time_of_day_filter(
            (115, 67, 66, 0.0), 800, 900), None)


    def test_date_range_filter(self):
        self.assertEqual(bp_tracker.date_range_filter(
            (115, 67, 66, 20220914.0839),
            20220913.0800, 20220916.0900), True)
        self.assertEqual(bp_tracker.time_of_day_filter(
            (115, 67, 66, 20220914.0839),
            20220910.0800, 20220913.0900), None)
        self.assertEqual(bp_tracker.time_of_day_filter(
            (115, 67, 66, 0.0),
            20220910.0800, 20220913.0900), None)


    def test_not_before_filter(self):
        self.assertEqual(bp_tracker.not_before_filter(
            (115, 67, 66, 20220914.0839),
            20220913.0800), True)
        self.assertEqual(bp_tracker.not_before_filter(
            (115, 67, 66, 20220914.0839),
            20220915.0800), None)
        self.assertEqual(bp_tracker.not_before_filter(
            (115, 67, 66, 0.0),
            20220915.0800), None)


redact = '''  # We should run the following once in awhile!
class TestTestsAreRun(unittest.TestCase):
    def test_testing(self):
        print('In test_testing: about to fail!')
        self.assertEqual(1, 2)
'''
    

if __name__ == '__main__':
    unittest.main()
