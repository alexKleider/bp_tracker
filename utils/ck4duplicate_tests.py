#!/usr/bin/env python3

# File: ck4duplicate_tests.py

test_file = 'test/test_bp_tracker.py'

def list_duplicate_defs(code_file):
    """
    Returns a (possibly empty) listing of names of
    functions (or methods) declared more than once.
    """
    defs = []
    with open(code_file, 'r') as instream:
        for line in instream:
            words = line.strip().split()
            try:
                i = words.index('def')
            except ValueError:
                continue
            else:  # we want the part between 'def' and '('
                parts = words[i+1].split('(')
                defs.append(parts[0])
    s = set(defs)
    if len(s) == len(defs):
        return []
    else:
        duplicates = []
        for item in defs:
            if defs.count(item) > 1 and not item in duplicates:
                duplicates.append(item)
        ret = []
        for item in duplicates:
            ret.append(item)
        return ret


if __name__ == '__main__':
    res = list_duplicate_defs(test_file)
    if res:
        print("The following are defined more than once:")
        for item in res:
            print("\t{}".format(item))
    else:
        print("No duplicates found.")
