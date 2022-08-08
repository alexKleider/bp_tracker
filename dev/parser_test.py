#!/usr/bin/env python3

# File: parser_test.py

"""
Where I'm playing around trying to understand how argparse works.
"""

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--add_one",
        nargs=1,
        help="Add one argument."
        )
parser.add_argument("--set_flag",
        action="store_true",
        help="No arguments.",
        )
