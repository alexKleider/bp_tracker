#!/usr/bin/env python3

# File: test/test_category.py

import unittest
import os
import sys
sys.path.insert(0, os.path.split(sys.path[0])[0])

import dev.category as category
from test.data4category import test_data


redact = '''
levels = category.categories
for n in range(len(levels)):
    print("#{:>2}: {}"
        .format(n, levels[n]))
'''


def value2test(test_data):
    for item in test_data:
        yield tuple(item.split())


class TestCategory(unittest.TestCase):

    def test_get_category(self):
        for datum in value2test(test_data):
#           print("{} {} {} yields {}"
#               .format(datum[0], datum[1], datum[2],
#               category.get_category(datum[0], datum[1])
#                   ))
            self.assertEqual(
                category.get_category(datum[0], datum[1]),
                category.categories[int(datum[2])])

if __name__ == "__main__":
    unittest.main()

