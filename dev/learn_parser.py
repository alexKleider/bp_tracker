#!/usr/bin/env python3

# File: parser_test.py

"""
Code writen for myself (Alex Kleider) to
help me understand the argparse module.
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

def main():
    args = parser.parse_args()
    print("args.add_one is: {}".format(args.add_one))
    print("args.set_flag is: {}".format(args.set_flag))
    print(args)


if __name__ == "__main__":
    main()
