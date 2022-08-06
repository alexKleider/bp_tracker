#!/usr/bin/env python3

# File: dev/category.py

"""
"systolics", "diastolics" and "categories" are taken from
https://healthiack.com/wp-content/uploads/blood-pressure-chart-80.jpg
Results indicate that many (?most) readings can't be classified,
i.e. systolic and diastolic values don't both fall into the same
category.
/home/alex/Git/LH/bp_tracker/dev/
"""

import sys

# s == systolic values; d == diastolic values
s =  (50, 70, 90, 100, 121, 130, 140, 160, 180, 211, )
d = (35, 40, 60,  65,  81,  85,  90, 100, 110, 121, )

categories = ('extreme hypotension',        # 0
              'severe hypotension',         # 1
              'moderate hpyotension',       # 2
              'low normal blood pressure',  # 3
              'ideal blood pressure',       # 4
              'high normal blood pressure', # 5
              'pre-hypertension',           # 6
              'stage 1 hypertension',       # 7
              'stage 2 hypertension',       # 8
              'stage 3 hypertension',       # 9
              'hypertensive crisis',        #10
             )

test_data = (  # a subset of my readings
        (145, 67),
        (123, 64),
        (124, 56),
        (137, 74),
        (132, 64),
        (166, 78),
        (116, 65),
        (163, 70),
        (189, 90),
        (171, 83),
        (131, 66),
        (117, 69),
        (116, 62),
        (250, 130),  # fictional reading
    )


def get_category(bp, sord):
    """
    Given:
        <bp> (a single (systolic or diastolic) reading)
      & <sord> (any word that begins with either an 's' or a 'd',
        specifiying use of systolic or diastolic scale:
    returns a category.
    """
    if sord.startswith('s'):
        sord = s
    elif sord.startswith('d'):
        sord = d
    else:
        print("Must specify systolic or diastolic.")
        sys.exit()
    for n in range(len(sord)):
        category = categories[n]
        if int(bp) < sord[n]:
            return categories[n]
    return categories[-1]


def show_missmatches():
    """
    Shows that in most instances (of my readings)
    the systolic and the diastolic readings don't
    both fall into the same AHA category.
    """
    matches = missmatches = 0
    for item in test_data:
        systolic = item[0]
        diastolic = item[1]
        sys_category = get_category(systolic, systolics)
        dia_category = get_category(diastolic, diastolics)
        if sys_category == dia_category:
            matches += 1
            print("{}/{} fits '{}'"
                    .format(systolic, diastolic,
                        sys_category))
        else:
            missmatches += 1
            print("{}/{}: systolic => '{}'; diastolic => '{}'"
                .format(systolic, diastolic,
                    sys_category, dia_category))


if __name__ == '__main__':
    show_missmatches()
