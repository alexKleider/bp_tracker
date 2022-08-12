#!/usr/bin/env python3

# File: ck4duplicate_tests.py

test_file = 'test/test_bp_tracker.py'

l = []
with open(test_file, 'r') as instream:
    for line in instream:
        words = line.split()
        try:
            i = words.index('def')
        except ValueError:
            continue
        else:
            l.append(words[i+1])
s = set(l)
if len(s) == len(l):
    print("No duplicates.")
else:
    duplicates = []
    for item in l:
        if l.count(item) > 1 and not item in duplicates:
            duplicates.append(item)
    print("The following function names have duplicates:")
    for item in duplicates:
        print('\t{}'.format(item))

