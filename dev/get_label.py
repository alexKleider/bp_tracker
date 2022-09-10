#!/usr/bin/env python3

""" Demo code for getting a classification from a numeric range. """

sys = (
    (0, 0, 'dead'),
    (1, 49, 'low: medication required'),
    (50, 69, 'low: at risk'),
    (70, 85, 'low'),
    (86, 120, 'good'),
    (121, 129, 'elevated'),
    (130, 139, 'high: stage 1'),
    (140, 179, 'high: stage 2'),
    (180, 300, 'high: crisis'),
)

dia = (
    (0, 0, 'dead'),
    (1, 45, 'low: medication required'),
    (46, 55, 'low: at risk'),
    (56, 65, 'low'),
    (66, 79, 'good'),
    (80, 89, 'high: stage 1'),
    (90, 119, 'high: stage 2'),
    (120, 300, 'high: crisis'),
)

def get_label(num, scale):
    """ Takes a number and a tuple of (min, max, lable) tuples, 
        returns the label for the range the number falls into. 
    """
    for group in scale:
        lower, upper, label = group
        if num in range(lower, upper + 1):
            # The 'upper + 1' is required because range doesn't include upper
            return label
    return None

if __name__ == "__main__":

    # Test at lower boundry
    assert( get_label(70, sys) == 'low')
    assert( get_label(56, dia) == 'low')

    # Test at upper boundry
    assert( get_label(179, sys) == 'high: stage 2')
    assert( get_label(119, dia) == 'high: stage 2')

    # Test out of bounds
    assert( get_label(-1, sys) == None)
    assert( get_label(301, dia) == None)
