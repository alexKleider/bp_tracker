#!/usr/bin/env python3

# File: aha.py  (for American Heart Association)

"""
An amalgamation of what used to be category.py and calculate.py.

"cat..." deals with a BP 'class' depending on whether systolic or
diastolic pressure is provided. i.e. each (sys vs dia) is classified
separately.) Provides get_category(bp_value, systolic_or_diastolic.)
https://healthiack.com/wp-content/uploads/blood-pressure-chart-80.jpg
(which I believe are from the American Heart Association.)
See categories.txt
Note: more often than not systolic and diastolic values don't both fall
into the same category. (see 'main' code)
Hence the use of the next set of utilities...

"calc..."  does some calculations as defined @ 
https://www.thecalculator.co/health/Blood-Pressure-Calculator-487.html
Using formulas provided by the AHA we get a 'unified' classification.

The mean arterial pressure (MAP) formula is:
MAP ≈ [(2*DP) + SP]/3

The pulse pressure (PP) formula used is:
PP = SP – DP

"""

import sys

# Numeric representation of the criteria used to
# classify blood pressure readings:
# s == systolic values; d == diastolic values
s =  (50, 70, 90, 100, 121, 130, 140, 160, 180, 211, )
d = (35, 40, 60,  65,  81,  85,  90, 100, 110, 121, )
categories = ('extreme hypotension',        # 0
              'severe hypotension',         # 1
              'moderate hypotension',       # 2
              'low normal BP',              # 3
              'ideal BP',                   # 4
              'high normal BP',             # 5
              'pre-hypertension',           # 6
              'stage 1 hypertension',       # 7
              'stage 2 hypertension',       # 8
              'stage 3 hypertension',       # 9
              'hypertensive crisis',        #10
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

def get_unified_status(sys, dia):
    """
    The calculator returns the blood pressure status reading based
    on the following ranges for systolic and diastolic presures:
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
    if sys < 120 and dia < 80: return 'Normal BP'
    if (sys >=120 and sys <140) or (dia >=80 and dia < 90):
        return 'Pre-hypertension'
    if (sys >=140 and sys <160) or (dia >=80 and dia <= 99):
        return 'Stage I hypertension'
    if (sys >=160 and sys <180) or (dia >=100 and dia <= 110):
        return 'Stage II hypertension'
    if sys > 180 or dia > 110: return 'Hypertensive crisis'
    assert False

def calc(sys, dia):
    sys, dia = int(sys), int(dia)
    mean = round((2 * dia + sys)/3)
    pp = sys - dia
    status = get_unified_status(sys, dia)
    return mean, pp, status


def show_calc(sys, dia):
    mean, pp, status = calc(sys, dia)
    return f"Mean BP: {mean}, Pulse pressure: {pp}, Status: {status}"


if __name__ == '__main__':   # calculator

    def show_missmatches(test_data):
        """
        Shows that in most instances (of my readings)
        the systolic and the diastolic readings don't
        both fall into the same AHA category.
        """
        nmatches = nmissmatches = 0
        matches = []
        missmatches = []
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
                nmissmatches += 1
                addendum = ''
                missmatches.append("{}/{}: {} / {}  {}"
                    .format(systolic, diastolic,
                        sys_category, dia_category, addendum))
        print(
          f"Result: {nmatches} matches and {nmissmatches} missmatches")
        both = matches + missmatches
        for res in both:
            print(res)


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
    show_missmatches(readings)  # category 
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
    for sys, dia, mean, pp, status in test_data:
        res = calc(sys, dia)
        try:
            assert res == (mean, pp, status,)
        except AssertionError:
            ok = False
            print(
            f"calc({sys}, {dia}) => {res} NOT ({mean}, {pp}, {status})")
    if ok:
        print("Test completed successfully.")
    else:
        print("Errors described above.")


presentation = '''
          Current   State                Average    State
systolic      151   Hypertension             156    {:<22}
diastolic      79   Normal                    85    {:<22}
mean/unified
'''   # as proposed by Leam week of Aug 22nd
