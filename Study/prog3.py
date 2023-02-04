#!/usr/bin/env python3

# File: prog3.py

"""
https://docs.python.org/3/howto/argparse.html#id1
"""

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", help="display a square of a given number")
args = parser.parse_args()
print(args.square**2)


