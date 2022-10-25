#!/usr/bin/env python3

# File: ck_bp_data.py

import re

data = [
"# bp_numbers.txt",
"# systolic, diastolic, pulse, time stamp",
"134 68 75 20220630.0929",
"136 67 73 20220630.0941",
"  143 66 73 20220630.1049",
"145 75 69 20220630.1656   ",
"124 61 64 20220630.1808   # notes re this reading",
"133 64 65 20220630.1839",
"extranious 134 65 60 20220630.2300",
"117 62 62 20220703.1204",
"144 70 70 20220705.2137",
"150 71 71 20220707.1143",
]

valid_data_re = r"\s?(\d{2,3})\s+(\d{2,3})\s+(\d{2,})\s+(\d+[.]\d+)"
valid_pattern = re.compile(valid_data_re)

for line in data:
    match = valid_pattern.match(line.strip())
    if match:
        print(f"{line} >> {match.groups()}")
    else:
        print(f"{line} <<doesn't match>>")
