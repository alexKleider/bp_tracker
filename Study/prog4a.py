#!/usr/bin/env python3

# File: prog4a.py

"""
https://docs.python.org/3/howto/argparse.html#id1
Dealing with optional argument.
"""

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--verbose", 
                help="increase output verbosity",
                action="store_true")
args = parser.parse_args()
if args.verbose:    # without the if, 
    print("verbosity turned on")


