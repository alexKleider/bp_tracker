#!/usr/bin/env python3

# File: aha/bpc.py

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
This is dealt with by the 'SingleCategory' class.

There are also criteria for evaluating individual systolic or
diastolic readings.  (See the 'SeparateCategory' class.)
"""

import re
import sys

valid_data_re = r"\s?(\d{2,3})\s+(\d{2,3})\s+(\d{2,})\s+(\d+[.]\d+)"
valid_pattern = re.compile(valid_data_re)

class SingleCategory(object):
    categories = ('NORMAL', 'ELEVATED', 'STAGE 1 HYPERTENSION', 
        'STAGE 2 HYPERTENSION', 'HYPERTENSIVE CRISIS',)

    def category(self,sys, dia):
        sys, dia = int(sys), int(dia)
        if sys>180 or dia>=120:
            return self.categories[4]
        if (sys>=140) or (dia>=90):
            return self.categories[3]
        if (sys>=130 and sys <=139) or (dia>=80 and dia<=89):
            return self.categories[2]
        if (sys>=120 and sys <=129) and dia<80:
            return self.categories[1]
        if sys < 120 and dia < 80:
            return self.categories[0]
        # should never get to this last line...
        _ = input(f"'SingleCategory.category({sys}/{dia})' failed!!")
        sys.exit()

class SeparateCategory(object):
    s = (50, 70, 90, 100, 121, 130, 140, 160, 180, 211, )
    d = (35, 40, 60,  65,  81,  85,  90, 100, 110, 121, )
    categories = ('Extreme hypotension',        # 0
                  'Severe hypotension',         # 1
                  'Moderate hypotension',       # 2
                  'Low normal BP',              # 3
                  'Ideal BP',                   # 4
                  'High normal BP',             # 5
                  'Pre-hypertension',           # 6
                  'Stage I hypertension',       # 7
                  'Stage II hypertension',      # 8
                  'Stage III hypertension',     # 9
                  'Hypertensive crisis',        #10
                 )


    def get_category(self, bp, sord):
        """
        Given:
            <bp>: a single (systolic or diastolic) reading.
          & <sord>: a string that begins with an 's' or a 'd',
            to specifiy if <bp> is systolic or diastolic:
        returns a category.
        """
        if sord.startswith('s'):
            sord = self.s
        elif sord.startswith('d'):
            sord = self.d
        else:
            print("Must specify systolic or diastolic.")
            sys.exit()
        for n in range(len(sord)):
            category = self.categories[n]
            if int(bp) < sord[n]:
                return self.categories[n]
        return self.categories[-1]


    def get_categories(self, sys, dia):
        sys_val = self.get_category(sys, 's')
        dia_val = self.get_category(dia, 'd') 
        return f"{sys_val:>22}/{dia_val:<22}"


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
    bp_instance = SingleCategory()
    both = SeparateCategory()
    for datum in test_data:
        if (bp_instance.category(datum[0], datum[1]) !=
                            bp_instance.categories[datum[2]]):
            _ = input('{0:}/{1:} != {2:}'.format(*datum))
    with open('../bp_numbers.txt', 'r') as stream:
        for line in stream:
            line = line.strip()
            match = valid_pattern.match(line)
            if match:
                print(f"{line:>24} => " +
                    f"{bp_instance.category(match[1],match[2]):<24}"
                    + both.get_categories(match[1], match[2]))
            else:
                print(f'no match for: {line}')

