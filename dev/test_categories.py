#!/usr/bin/env python3

# File: test_categories.py

import category

TEST_DATA = 'bp_test_data'

def test_translation():
    with open(TEST_DATA, 'r') as instream:
        for line in instream:
            parts = line.strip().split()
            sys, dia = parts[0].split('/')
            level = ' '.join(parts[1:])
            sys_category = category.get_category(sys, 
                category.systolics)
            dia_category = category.get_category(dia, 
                category.diastolics)
            if (sys_category != level):
                print("Error Systolic {}: {} != {}"
                    .format(sys, sys_category, level))
            else: print("OK ", end='')
            if (dia_category != level):
                print("Error diastolic {}: {} != {}"
                    .format(dia,dia_category, level)) 
            else: print("OK ", end='')
            
            assert category.get_category(sys, 
                    category.systolics) == level
            assert category.get_category(dia, 
                    category.diastolics) == level
    print()

if __name__ == '__main__':
    test_translation()
