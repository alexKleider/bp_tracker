#!/usr/bin/env python3

# File: aha-bpc.py

"""
https://www.heart.org/en/health-topics/high-blood-pressure/understanding-blood-pressure-readings
    Blood preasure categories:
    /--------------------------------------------\
   / BP CATEGORY           | SYSTOLIC | DIASTOLIC \
   |----------------------------------------------|
0  | NORMAL                |  < 120   &   < 80    |
1  | ELEVATED              |  120-129 &   < 80    |
2  | STAGE 1 HYPERTENSION  |  130-139 or  80-89   |
3  | STAGE 2 HYPERTENSION  |  >= 140  or  >= 90   |
4  | HYPERTENSIVE CRISIS   |  > 180   or  >= 120  |
   \----------------------------------------------/
"""

import re
import sys
categories = ('NORMAL', 'ELEVATED', 'STAGE 1 HYPERTENSION', 
        'STAGE 2 HYPERTENSION', 'HYPERTENSIVE CRISIS',)
valid_data_re = r"\s?(\d{2,3})\s+(\d{2,3})\s+(\d{2,})\s+(\d+[.]\d+)"
valid_pattern = re.compile(valid_data_re)

def category(sys, dia):
    sys, dia = int(sys), int(dia)
    if sys>180 or dia>=120:
        return 'HYPERTENSIVE CRISIS'
    if (sys>=140) or (dia>=90):
        return 'STAGE 2 HYPERTENSION'
    if (sys>=130 and sys <=139) or (dia>=80 and dia<=89):
        return 'STAGE 1 HYPERTENSION'
    if (sys>=120 and sys <=129) and dia<80:
        return 'ELEVATED'
    if sys < 120 and dia < 80:
        return 'NORMAL'
    # should never get to this last line...
    _ = input(f"'category({sys}/{dia})' failed!!")
    sys.exit()

if __name__ == '__main__':
    test_data = (
        (181, 0, 4,),
        (0, 121, 4,),
        (140, 0, 3,),
        (0, 90, 3,),
        (130, 0, 2,),
        (139, 0, 2,),
        (0, 80, 2,),
        (0, 89, 2,),
        (120, 79, 1,),
        (129, 79, 1,),
        (119, 79, 0,),
    )
    for datum in test_data:
        if category(datum[0], datum[1]) != categories[datum[2]]:
            print('{0:}/{1:} != {2:}'.format(*datum))
    sys.exit()
    with open('bp_numbers.txt', 'r') as stream:
        for line in stream:
            line = line.strip()
            match = valid_pattern.match(line)
            if match:
                print(f"{line} => " + category(match[1],match[2]))
            else:
                print(f'no match for: {line}')

