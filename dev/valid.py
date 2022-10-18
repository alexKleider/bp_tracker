#!/usr/bin/env python3

# File: valid.py

"""
Check data file line validity.
"""

import sys

DEFAULT_DATA_FILE = "bp_numbers.txt"


def valid_line(line, errors=None):
    """
    Returns True only if line is deemed valid.
    <errors>, if provided, is expected to be a
    list to which invalid lines are added.
    """
    parts = line.strip().split()
    if ( (len(parts) == 4)
    and  (len(parts[-1].split(".")) == 2)
    and  (parts[0].isdigit())
    and  (parts[1].isdigit())
    and  (parts[2].isdigit())
    and  (parts[3].isdecimal)
    ):
        return True
    elif errors != None:
        errors.append(line)


def main():
    if len(sys.argv) > 1:
        data_file = sys.argv[1]
    else:
        data_file = DEFAULT_DATA_FILE
    errors = []
    n_valid_lines = 0
    print(f"Sourcing '{data_file}'.")
    with open(data_file, 'r') as infile:
        for line in infile:
            if valid_line(line, errors=errors):
                n_valid_lines += 1
    if errors:
        print(f"Found {n_valid_lines} valid lines.")
        print("The following {} lines are invalid:"
                .format(len(errors)))
        for line in errors:
            print('\t' + line, end='')
    else:
        print(f"Found {n_valid_lines} all valid")


if __name__ == "__main__":
    main()
