#!/usr/bin/env python3

# File: test_aha.py
## Renamed this so it would not get picked up in unittest.

import os
try:
    import aha
except ImportError:
    from dev import aha

cwd = os.getcwd()
print(cwd)
if cwd.endswith('dev'):
    TEST_DATA = 'bp_test_data'
else:
    TEST_DATA = 'dev/bp_test_data'

def test_translation():
    with open(TEST_DATA, 'r') as instream:
        for line in instream:
            line = line.strip()
            if not line or line.startswith('#'): continue
            parts = line.strip().split()
            sys, dia = parts[0].split('/')
            level = ' '.join(parts[1:])
            sys_category = aha.get_category(sys, 
                's')
            dia_category = aha.get_category(dia, 
                'd')
            if (sys_category != level):
                print("Error Systolic {}: {} != {}"
                    .format(sys, sys_category, level))
            else: print("OK ", end='')
            if (dia_category != level):
                print("Error diastolic {}: {} != {}"
                    .format(dia,dia_category, level)) 
            else: print("OK ", end='')
            
            assert aha.get_category(sys, 
                    's') == level
            assert aha.get_category(dia, 
                    'd') == level
    print()

if __name__ == '__main__':
    test_translation()
