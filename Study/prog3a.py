#!/usr/bin/env python3

# File: prog3a.py

"""
https://docs.python.org/3/howto/argparse.html#id1
Dealing with positional argument.
"""

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", 
                help="display a square of a given number",
                type=int)
args = parser.parse_args()
print(args.square**2)


