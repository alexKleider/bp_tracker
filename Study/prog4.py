#!/usr/bin/env python3

# File: prog4.py

"""
https://docs.python.org/3/howto/argparse.html#id1
Dealing with optional argument.
"""

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--verbosity", 
                help="increase output verbosity")
args = parser.parse_args()
if args.verbosity:    # without the if, 
    print("verbosity turned on")


