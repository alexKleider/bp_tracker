#!/usr/bin/env python3

# File: prog1.py

"""
https://docs.python.org/3/howto/argparse.html#id1
"""

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("echo")
args = parser.parse_args()
print(args.echo)


