#!/usr/bin/env python3

# File test/tests.py

import os
import os.path
import tempfile
import unittest

import bp_tracker


class TestBpTracker(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.good_file = os.path.join(self.test_dir.name, 'good_data.txt')
        with open(self.good_file, 'w') as f:
            f.write("# A comment, just to keep us honest.\n")
            f.write("120 65 55 20220914.1407\n")
            f.write("120 64 60 20220914.1753\n")
            f.write("140 64 65 20220915.1408\n")
            f.write("140 62 60 20220915.1714\n")
        self.good_data = bp_tracker.array_from_file(self.good_file)


    def tearDown(self):
        self.test_dir.cleanup()


    def test_averaging(self):
        self.assertTrue(bp_tracker.averages(self.good_data) == [130, 64, 60] )


    def test_check_file_readable_file(self):
        self.assertTrue(bp_tracker.check_file(self.good_file, 'r'))
 

    def test_check_file_writeable_file(self):
        self.assertTrue(bp_tracker.check_file(self.good_file, 'w'))


    def test_check_file_writeable_dir(self):
        test_dir_writeable = os.path.join(self.test_dir.name, 'writeable')
        os.mkdir(test_dir_writeable)
        os.chmod(test_dir_writeable, 0o777)
        test_file = os.path.join(test_dir_writeable, 'missing.file')
        self.assertTrue(bp_tracker.check_file(self.test_dir.name, 'w'))


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


    def test_useful_lines(self):
        self.assertEqual( len(self.good_data), 4)


    def test_valid_data(self):
        data     = "120 65 55 20220914.1407"
        result   = bp_tracker.valid_data(data)
        expected = [120, 65, 55, '20220914.1407']
        self.assertTrue( result == expected)

    def test_array_from_file(self):
        data = (
            "110 59 68 20220809.1640",
            "124 62 62 20220810.0840",
            "134 63 57 20220812.0758",
            "134 62 57 20220812.1128",
            "100 59 62 20220812.1323",
                )
        report_file = os.path.join(self.test_dir.name,
                                    'test_write_data.txt')
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
        #!! Need to add test for following keys:
        #   s_cls, d_cls, n_data_points, calcs
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
        self.assertEqual((70, 90, 80),
                bp_tracker.list_low_high_avg([90, 70, 80]))


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
            self.assertEqual(
                bp_tracker.get_category(data[0], data[1]),
                bp_tracker.categories[int(data[2])])


    def test_get_unified_status(self):
        test_data = ((115, 70, 85, 45, 'Normal BP'),
             (127, 85, 99, 42, 'Pre-hypertension'),
             (145, 93, 110,52, 'Stage I hypertension'),
             (170, 104,126,66, 'Stage II hypertension'),
             (200, 112,141,88, 'Hypertensive crisis'),
            )
        for sp, dp, mean, pp, status in test_data:
            res = bp_tracker.calc(sp, dp)
            self.assertEqual(res, (mean, pp, status,))


    def test_calc(self):
        for sys, dia, mean, pp, status in(
                (115, 70, 85, 45, 'Normal BP'),
                (127, 85, 99, 42, 'Pre-hypertension'),
                (145, 93, 110,52, 'Stage I hypertension'),
                ):
            res = bp_tracker.calc(sys, dia)
            self.assertEqual(res, (mean, pp, status,))


    def test_show_calc(self):
        self.assertEqual(bp_tracker.show_calc(127, 85),
        "Mean BP: 99, Pulse pressure: 42, Status: Pre-hypertension")


    def test_no_date_stamp(self):
        self.assertEqual(bp_tracker.no_date_stamp(
            (115, 67, 66, '0.0' )), None)


    def test_time_of_day_filter(self):
        self.assertEqual(bp_tracker.time_of_day_filter(
            (115, 67, 66, '20220914.0800'), '0800', '0900'), True)
        self.assertEqual(bp_tracker.time_of_day_filter(
            (115, 67, 66, '20220914.0839'), '0800', '0900'), True)
        self.assertEqual(bp_tracker.time_of_day_filter(
            (115, 67, 66, '20220914.0839'), '0900', '1000'), None)
        self.assertEqual(bp_tracker.time_of_day_filter(
            (115, 67, 66, '0.0'), '0800', '0900'), None)


    def test_date_range_filter(self):
        self.assertEqual(bp_tracker.date_range_filter(
            (115, 67, 66, '20220914.0839'),
            '20220913.0800', '20220916.0900'), True)
        self.assertEqual(bp_tracker.time_of_day_filter(
            (115, 67, 66, '20220914.0839'),
            '20220910.0800', '20220913.0900'), None)
        self.assertEqual(bp_tracker.time_of_day_filter(
            (115, 67, 66, '0.0'),
            '20220910.0800', '20220913.0900'), None)


    def test_not_before_filter(self):
        self.assertEqual(bp_tracker.not_before_filter(
            (115, 67, 66, '20220914.0839'),
            '20220913.0800'), True)
        self.assertEqual(bp_tracker.not_before_filter(
            (115, 67, 66, '20220914.0839'),
            '20220915.0800'), None)
        self.assertEqual(bp_tracker.not_before_filter(
            (115, 67, 66, '0.0'),
            '20220915.0800'), None)


    def test_get_label(self):
        # Test at lower boundry
        self.assertTrue( bp_tracker.get_label(70, bp_tracker.systolics) == 'low')
        self.assertTrue( bp_tracker.get_label(56, bp_tracker.diastolics) == 'low')

        # Test at upper boundry
        self.assertTrue( bp_tracker.get_label(179, bp_tracker.systolics) == 'high: stage 2')
        self.assertTrue( bp_tracker.get_label(119, bp_tracker.diastolics) == 'high: stage 2')

        # Test out of bounds
        self.assertTrue( bp_tracker.get_label(-1, bp_tracker.systolics) == None)
        self.assertTrue( bp_tracker.get_label(301, bp_tracker.diastolics) == None)

    def test_report_format(self):
        expected = [
            "Systolic 165 (high: stage 2) ",
            "Diastolic 89 (high: stage 1) ",
            "Average 160/88 ",
        ]
        result = bp_tracker.report_format_3.split("\n")
        self.assertTrue(result[0] == expected[0])
        self.assertTrue(result[1] == expected[1])
        self.assertTrue(result[2] == expected[2])

    def test_filter_data(self):
        pass


    def test_get_args(self):
        pass

    
    def test_set_data_file(self):
        pass


    def test_add(self):
        pass


    def test_format_data(self):
        pass

if __name__ == '__main__':
    unittest.main()
