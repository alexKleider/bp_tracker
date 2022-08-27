#!/usr/bin/env python3

# File: dev/category.py

"""
Provides get_category(bp_value, systolic_or_diastolic)
which returns an American Heart Association blood pressure category.

"systolics", "diastolics" and "categories" are taken from
https://healthiack.com/wp-content/uploads/blood-pressure-chart-80.jpg
(which I believe are from the American Heart Association.)

The 'main' code shows that many (?most) readings can't be classified,
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


def get_category(bp, s_or_d, categories=categories):
    """
    Given <bp> (a reading)
    specified as <s_or_d> (systolic or diastolic)
    returns a category.
    <bp> must be something that can be turned into an int.
    <s_or_d> must be a string beginning in either 's' for systolic
    or 'd' for diastolic.
    <categories> is a parameter incase the user wants to use a
    different set of descriptors.
    """

    def terminate():
        print(
        "unacceptable <s_or_d> parmeter for get_category function")
        sys.exit()

    try: bp = int(bp)
    except (ValueError, TypeError):
        print(
        "{} not an integer (parameter of get_category function)"
            .format(bp))
        sys.exit()
    if s_or_d and isinstance(s_or_d, str):
        if s_or_d[0] in {'s', 'S'}:
            sord = systolics
        elif s_or_d[0] in {'d', 'D'}:
            sord = diastolics
        else: terminate()
    else: terminate()
    for n in range(len(sord)):
        category = categories[n]
        if bp < sord[n]:
            return categories[n]
    return categories[-1]


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
        sys_category = get_category(systolic, 's')
        dia_category = get_category(diastolic, 'd')
        if sys_category == dia_category:
            matches += 1
            print("{}/{} fits '{}'"
                    .format(systolic, diastolic,
                        sys_category))
        else:
            missmatches += 1
            addendum = ''
        print("{}/{}: {} / {}  {}"
            .format(systolic, diastolic,
                sys_category, dia_category, addendum))


if __name__ == '__main__':
    show_missmatches()
