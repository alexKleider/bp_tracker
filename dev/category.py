#!/usr/bin/env python3

# File: category.py

"""
"systolics", "diastolics" and "categories" are taken from
https://healthiack.com/wp-content/uploads/blood-pressure-chart-80.jpg
Results indicate that many (?most) readings can't be classified,
i.e. systolic and diastolic values don't both fall into the same
category.
"""

systolics =  (50, 70, 90, 100, 121, 130, 140, 160, 180, 211, )
diastolics = (35, 40, 60,  65,  81,  85,  90, 100, 110, 121, )
categories = ('extreme hypotsn',
              'severe hypotsn',
              'moderate hypotsn',
              'low normal BP',
              'ideal BP',
              'high normal BP',
              'pre-hypertsn',
              'stage 1 hypertsn',
              'stage 2 hypertsn',
              'stage 3 hypertsn',
              'hypertensive crisis',
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

def unpack(tup):
    pass


def get_category(bp, sord):
    """
    Given <bp> (a reading)
    specified as <sord> (systolic or diastolic)
    returns a category.
    """
#   for n in range(len(categories)):
    for n in range(len(sord)):
        category = categories[n]
        if int(bp) < sord[n]:
            return categories[n]
    return categories[-1]


def main():
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
    main()
