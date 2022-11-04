#!/usr/bin/env python3

# File: aha.py  (for American Heart Association)

"""
Blood Pressure consists of sys/dia. i.e. two numbers.
There are criteria for determining the BP Category of a single 
systolic or diastolic reading
and criteria for determining BP Category based on a sys/dia reading.
One can also calculate a mean arterial pressure (MAP) and get a
classification based on that.


The "Category" section deals with individual (systolic or diastolic)
values and assigns the appropriate AHA classification.
https://healthiack.com/wp-content/uploads/blood-pressure-chart-80.jpg
(which I believe are from the American Heart Association.)
See categories.txt
Note: more often than not systolic and diastolic values don't both fall
into the same category. (see 'main' code)
Hence the use of the next set of utilities...

The "Calculate" section  does some calculations as defined @ 
https://www.thecalculator.co/health/Blood-Pressure-Calculator-487.html
using formulas provided by the AHA we get a 'unified' classification.

The mean arterial pressure (MAP) formula is:
MAP ≈ [(2*DP) + SP]/3

Pulse pressure is the difference between systolic and diastolic.
"""

import sys

# Numeric representation of the criteria used to classify
# (individual single number) blood pressure readings:
# s == systolic values; d == diastolic values
# Note: these do _not_ correspond with the 'unified' system.
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


def get_category(bp, sord):
    """
    Given:
        <bp>: a single (systolic or diastolic) reading.
      & <sord>: a string that begins with an 's' or a 'd',
        to specifiy if <bp> is systolic or diastolic:
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


# -------  calculate  -----------#

def get_unified_status(sp, dp):
    """
    The calculator returns a TEXT REPRESENTATION of AHA status
    based on the blood pressure provided (<sp>/<dp>).
    The rules:
    Blood Pressure Status     Systolic (mm Hg) IF  Distolic (mm Hg)
                                 Min     Max       Min     Max
    Normal Blood Pressure   	    <120      and      <80
    Pre-hypertension             120     139  or    80      89
    Stage I High Blood Pressure  140     159  or    90      99
    (Hypertension)
    Stage II High Blood Pressure 160 	180   or   100     110
    (Hypertension)
    Hypertensive crisis             >180      or       >110
    (where emergency care is required)
    """
    if sp < 120 and dp < 80: return 'Normal BP'
    if (sp >=120 and sp <140) or (dp >=80 and dp < 90):
        return 'Pre-hypertension'
    if (sp >=140 and sp <160) or (dp >=80 and dp <= 99):
        return 'Stage I hypertension'
    if (sp >=160 and sp <180) or (dp >=100 and dp <= 110):
        return 'Stage II hypertension'
    if sp > 180 or dp > 110: return 'Hypertensive crisis'
    assert False


def calc(sp, dp):
    sp, dp = int(sp), int(dp)
    mean = round((2 * dp + sp)/3)
    pp = sp - dp
    status = get_unified_status(sp, dp)
    return mean, pp, status


def show_calc(sp, dp):
    mean, pp, status = calc(sp, dp)
    return f"Mean BP: {mean}, Pulse pressure: {pp}, Status: {status}"


if __name__ == '__main__':   # calculator

    def show_mismatches(test_data):
        """
        Shows that in most instances (of my readings)
        the systolic and the diastolic readings don't
        both fall into the same AHA category.
        """
        nmatches = nmismatches = 0
        matches = []
        mismatches = []
        for item in test_data:
            systolic = item[0]
            diastolic = item[1]
            sys_category = get_category(systolic, 's')
            dia_category = get_category(diastolic, 'd')
            if sys_category == dia_category:
                nmatches += 1
                matches.append("{}/{} fits '{}'"
                        .format(systolic, diastolic,
                            sys_category))
            else:
                nmismatches += 1
                addendum = ''
                mismatches.append("{}/{}: {} / {}  {}"
                    .format(systolic, diastolic,
                        sys_category, dia_category, addendum))
        print(
          f"Result: {nmatches} matches and {nmismatches} mismatches")
        both = matches + mismatches
        for res in both:
            print(res)


systolic_edges = (
        ( 49, categories[ 0]),
        ( 50, categories[ 1]),
        ( 69, categories[ 1]),
        ( 70, categories[ 2]),
        ( 89, categories[ 2]),
        ( 90, categories[ 3]),
        ( 99, categories[ 3]),
        (100, categories[ 4]),
        (120, categories[ 4]),
        (121, categories[ 5]),
        (129, categories[ 5]),
        (130, categories[ 6]),
        (139, categories[ 6]),
        (140, categories[ 7]),
        (159, categories[ 7]),
        (160, categories[ 8]),
        (179, categories[ 8]),
        (180, categories[ 9]),
        (210, categories[ 9]),
        (211, categories[10]),
        )

diastolic_edges = (
        ( 34, categories[ 0]),
        ( 35, categories[ 1]),
        ( 39, categories[ 1]),
        ( 40, categories[ 2]),
        ( 59, categories[ 2]),
        ( 60, categories[ 3]),
        ( 64, categories[ 3]),
        ( 64, categories[ 4]),
        ( 80, categories[ 4]),
        ( 81, categories[ 5]),
        ( 84, categories[ 5]),
        ( 85, categories[ 6]),
        ( 89, categories[ 6]),
        ( 90, categories[ 7]),
        ( 99, categories[ 7]),
        (100, categories[ 8]),
        (109, categories[ 8]),
        (110, categories[ 9]),
        (120, categories[ 9]),
        (121, categories[10]),
        )


readings = (  # a subset of my readings
        (145, 67),# used for testing
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
        (110, 61),
        (128, 63),
        (141, 70),
        (155, 67),
        (144, 73),
        (124, 66),
        (121, 64),
        (123, 66),
    )
    show_mismatches(readings)  # category 
    # the above demonstrates that for many/most readings
    # the classification regarding systolic vs diastolic
    # do not match!

    test_data = ((115, 70, 85, 45, 'Normal BP'),
             (127, 85, 99, 42, 'Pre-hypertension'),
             (145, 93, 110,52, 'Stage I hypertension'),
             (170, 104,126,66, 'Stage II hypertension'),
             (200, 112,141,88, 'Hypertensive crisis'),
            )
    ok = True
    for sp, dp, mean, pp, status in test_data:
        res = calc(sp, dp)
        try:
            assert res == (mean, pp, status,)
        except AssertionError:
            ok = False
            print(
            f"calc({sp}, {dp}) => {res} NOT ({mean}, {pp}, {status})")
    if ok:
        print("Test completed successfully.")
    else:
        print("Errors described above.")


# work in progress...
presentation = '''
          Current   State                Average    State
systolic      151   Hypertension             156    {:<22}
diastolic      79   Normal                    85    {:<22}
mean/unified
'''   # as proposed by Leam week of Aug 22nd
