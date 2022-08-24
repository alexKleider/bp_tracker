#!/usr/bin/env python3

# File: bin/calculator.py

"""
Begin implementing a 'calculator' as described here:
https://www.thecalculator.co/health/Blood-Pressure-Calculator-487.html

The mean arterial pressure (MAP) formula is:
MAP ≈ [(2*DP) + SP]/3

The pulse pressure (PP) formula used is:
PP = SP – DP

"""

def get_status(sys, dia):
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
    if sys < 120 and dia < 80: return 'normal'
    if (sys >=120 and sys <140) or (dia >=80 and dia < 90):
        return 'pre'
    if (sys >=140 and sys <160) or (dia >=80 and dia <= 99):
        return 'stage I'
    if (sys >=160 and sys <180) or (dia >=100 and dia <= 110):
        return 'stage II'
    if sys > 180 or dia > 110: return 'crisis'
    assert False

test_data = ((115, 70, 85, 45, 'normal'),
             (127, 85, 99, 42, 'pre'),
             (145, 93, 110,52, 'stage I'),
             (170, 104,126,66, 'stage II'),
            )

def calc(sys, dia):
    sys, dia = int(sys), int(dia)
    mean = (2 * dia + sys)/3
    pp = sys - dia
    status = get_status(sys, dia)
    return mean, pp, status


def show_calc(sys, dia):
    mean, pp, status = calc(sys, dia)
    return f"Mean BP: {mean:.0f}, Pulse pressure: {pp}, Status: {status}"


if __name__ == '__main__':
    for sys, dia, mean, pp, status in test_data:
        res = calc(sys, dia)
        try:
            assert res == (mean, pp, status,)
        except AssertionError:
            print(
            f"calc({sys}, {dia}) => {res} NOT ({mean}, {pp}, {status})")
    print("Test completed")

