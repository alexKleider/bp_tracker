#!/usr/bin/env python3

# File: ck_bp_data.py

"""
Provides function:
    get_reading

Uses regex to get (systolic, diastolic, pulse & time)
components from a data file.
"""

import re

data = [
"# bp_numbers.txt",
"# systolic, diastolic, pulse, time stamp",
"134 68 75 20220630.0929",
"134 68 75 202206.0929",
"136 67 73 20220630.09",
"  143 66 73 20220630.1049",
"145 75 69 20220630.1656   ",
"124 61 64 0.0   # notes re this reading",
"133 64 65 20220630.1839",
"extranious 134 65 60 20220630.2300",
" extra 117 62 62 0.0#annotations",
"144 70 70 20220705.2137",
"  extranious 144 70 70 20220705.2137front and back",
"150 71 71 20220707.1143",
"150 71 71",
]

valid_data_re = r"\s?(\d{2,3})\s+(\d{2,3})\s+(\d{2,})\s+(\d{8}[.]\d{4})"
valid_data_re = r"""
(
(?P<sys>\d{2,3})
\s+
(?P<dia>\d{2,3})
\s+
(?P<pulse>\d{2,})
\s+
(?P<time>(\d{8}[.]\d{4})|(0[.]0))
)
"""
valid_pattern = re.compile(valid_data_re, re.VERBOSE)

def get_reading(line):
    m = valid_pattern.search(line)
    if m:
        return (m.group('sys'), m.group('dia'),
                m.group('pulse'), m.group('time'))
for line in data:
    ret = get_reading(line)
    if ret:
        print(f"{line} >> ",end='')
        print("'{0:}/{1:} {2:} {3:}'".format(*ret))
    else:
        print(f"{line} <<doesn't match>>")
