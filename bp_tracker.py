#!/usr/bin/env python3

# working in branch main

# name:     bp_tracker.py
# version:  0.0.1
# date:     20220509
# authors:  Leam Hall, Alex Kleider
# desc:     Track and report on blood pressure numbers.

# Notes:
#  Datafile expects three ints and one float, in order.

# TODO
#   Add statistical analysis for standard deviation.
#   Report based on time of day (early, midmorning, afternoon, evening)
#   (?) Add current distance from goal?
#   Add more tests.

import os
import sys
import argparse
from datetime import datetime
import dev
from dev import aha

#?! A bad name! It's a data file not a report file.
global_report_file = 'bp_numbers.txt'

report_format ="""
           | Low  | High | Avg  |
           | ---  | ---- | ---  |
Systolic ..|{sl:^6}|{sh:^6}|{sa:^6}|
Diastolic .|{dl:^6}|{dh:^6}|{da:^6}|
Pulse .....|{pl:^6}|{ph:^6}|{pa:^6}|
"""

report_format_2 =  "          | Low  | High | Avg  |\n"
report_format_2 += "Systolic  |{:^6}|{:^6}|{:^6}|\n"
report_format_2 += "Diastolic |{:^6}|{:^6}|{:^6}|\n"
report_format_2 += "Pulse     |{:^6}|{:^6}|{:^6}|\n"

def check_file(file, mode):
    """
    Mode (must be 'r' or 'w') specifies if we need to 
    r)ead or w)rite to the file.
    """
    if mode == 'r' and os.access(file, os.R_OK):
        return True
    if mode == 'w':
        if os.access(file, os.W_OK):
            return True
        if not os.path.exists(file) and os.access(os.path.dirname(file), os.W_OK):
            return True
    return False

def useful_lines(stream, comment="#"):
    """
    A generator which accepts a stream of lines (strings.)
    Blank lines and leading and/or trailing white space are ignored.
    If <comment> resolves to true, lines beginning with <comment>
    (after being stripped of leading spaces) are also ignored.
    <comment> can be set to <None> if don't want this functionality.
    Other lines are returned ("yield"ed) stripped of leading and
    trailing white space.
    """
    for line in stream:
        line = line.strip()
        if comment and line.startswith(comment):
            continue
        if line:
            yield line


def array_from_file(report_file):
    """
    Input is the report file: four (string) values per line.[1]
    Output is a list of 4 tuples.
    Tuples are: systolic, diastolic, pulse, time stamp.[1]
    [1] Each of the 4 strings represents a number:
    first three are integers, last (the fourth) is a float.
    #? the last isn't really a float: it's YYYYmmdd.hhmm
    #? a string representation of a timestamp!
    """
    data = []
    #! replace with clause with store_report function
    with open(report_file, 'r') as stream:
        for line in useful_lines(stream):
            datum = line.split()
            if len(datum) == 4:
                data.append(tuple(datum))
            else:
                raise Exception(
                  "Badly formated line found in input ..."
                  + "\n file: {}" .format(report_file)
                  + '\n"{}"'.format(line))
    return data
 

def report(report_data):
    """
    #! not used
    Input is a list of 4 tuples.
    Output is a 4 tuple, each member of which is
    the highest of its category in the input.
    Ordering function is based on int() for the first three
    and float() for the last of each 4 tuple of input.
    """
    highest_systolic  = 0
    highest_diastolic = 0
    highest_pulse     = 0
    latest_date       = 0.0
    for datum in report_data:
        systolic  = int(datum[0])
        diastolic = int(datum[1])
        pulse     = int(datum[2])
        date      = float(datum[3]) 
        if systolic > highest_systolic:
            highest_systolic = systolic
            highest_systolic_event = datum
        if diastolic > highest_diastolic:
            highest_diastolic = diastolic
            highest_diastolic_event = datum
        if pulse > highest_pulse:
            highest_pulse = pulse
            highest_pulse_event = datum
        if date > latest_date:
            latest_date = date
            latest_record = datum
    return (highest_systolic_event, highest_diastolic_event,
            highest_pulse_event, latest_record,)
  
  
def format_report(systolics, diastolics, pulses, style = report_format_2):
    """
    Takes the numeric lists of systolics, diastolics, and pulses, and 
    return a string for printing.
    TODO: Allow for different report formats.
    """
    sl, sh, sa = list_low_high_avg(systolics)
    dl, dh, da = list_low_high_avg(diastolics)
    pl, ph, pa = list_low_high_avg(pulses)
    
    result = style.format(sl, sh, sa, dl, dh, da, pl, ph, pa)    
    return result

def list_collations(report_data):
    """
    Takes a data set each entry of which contains a minimum of 3
    strings, each representing an int.
    Returns a tuple of three lists: all values are ints.
    """
    systolics   = []
    diastolics  = []
    pulses      = []

    for datum in report_data:
        systolics.append(int(datum[0]))
        diastolics.append(int(datum[1]))
        pulses.append(int(datum[2]))

#   _ = input("list_collections provides:\n" +
#           repr((systolics, diastolics, pulses)))
    return systolics, diastolics, pulses


def dict_for_display(report_data):
    """
    Takes a data set each entry of which contains a minimum of 3
    strings, each representing an int.
    Returns a dict of ints keyed by:
        sh, sa, sl,  # s(ystolic  h{ighest a(verage l(lowest
        dh, da, dl,  # d(iastolic
        ph, pa, pl.  # p(ulse
    """
    systolics, diastolics, pulses = list_collations(report_data)
    res = {}
    res['sl'] = list_low_high(systolics)[0]
    res['sh'] = list_low_high(systolics)[1]
    res['sa'] = list_average(systolics)
    res['dl'] = list_low_high(diastolics)[0]
    res['dh'] = list_low_high(diastolics)[1]
    res['da'] = list_average(diastolics) 
    res['pl'] = list_low_high(pulses)[0]
    res['ph'] = list_low_high(pulses)[1]
    res['pa'] = list_average(pulses) 
    return res


def list_average(l):
    """
    Takes a numeric list and returns the average
    expressed as an integer.
    """
    if not l: return 0  # list might be empty!
    average = round(sum(l) / len(l))
    return average


def list_low_high(l):
    """
    Takes a numeric list; returns a tuple of lowest and highest entries.
    """
    return (min(l), max(l))


def list_low_high_avg(l):
    """
    Takes a numeric list; returns a tuple: lowest, highest, and average entries.
    """
    return ( min(l), max(l), sum(l) // len(l) )


def averages(data, n=None):
    """
    Input is a list of 4 tuples. (output of array_from_file func)
    Result is a tuple of floats: averages of the
    systoli, diastolic and pulse values.
    If n is provided, it must be an integer representing how 
    many of the last recorded values to include in the average.
    If greater than number of values, it will be scaled down.
    """
    l = len(data)
    if n:
        if n < 0:
            print("Number to consider can not be less than zero!")
            assert False
        l = len(data)
        if n > l: n = l
        d = data[-n:]
    else:
        d = data
        n = len(d)
    sys_sum = dia_sum = pul_sum = 0
    for vals in d:
        sys_sum += int(vals[0])
        dia_sum += int(vals[1])
        pul_sum += int(vals[2])
    return [round(val/n) for val in (sys_sum, dia_sum, pul_sum)]


def display_averages(averages):
    """
    Assumes want one decimal place. (Leam may want none!)
    """
    return ('{:.1f}/{:.1f} {:.1f}'
            .format(*averages))


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--add",
        nargs=3,
        help = "Add in the order of systolic, diastolic, pulse",
        )
    parser.add_argument(
        "-f", "--file",
        help = "Report file (default bp_numbers.txt)",
        default=global_report_file
        )
    parser.add_argument(
        "-v", "--averages",
        nargs=1,
        help = "Report average of last n values, 0 for all",
        default=0,
        )
    return parser.parse_args()


def set_data_file(args):
    """
    Modify data file prn and ..
    Notify user which data file is being used:
    """
    if args.file == global_report_file:
        print("Using '{}' as data file."
            .format(global_report_file))
    else:
        print("Reassigned data file to '{}'."
                .format(args.file))

def add_cmd(args):
    # This format allows sequencing now and parsing later.
    if check_file(args.file, 'w'):
        timestamp   = datetime.now().strftime("%Y%m%d.%H%M")
        this_report = args.add
        this_report.append(timestamp) 
        #! replace next two lines with store_report function
        with open(args.file, 'a') as file:
            file.write("{} {} {} {}\n".format(*this_report))
    else:
        print("Unable to write to", args.file)
        sys.exit(1)
    sp, dp, pulse, date = this_report
    print("Recording BP of {}/{}."
        .format(sp, dp))
    print("{} / {}"
        .format(
            dev.aha.get_category(sp, 's'),
            dev.aha.get_category(dp, 'd')
            ))
    print(dev.aha.show_calc(sp,dp))


def averages_cmd(args):
    if not check_file(args.file, 'r'):
        print("Unable to find ", args.file)
        sys.exit(1)
    n = int(args.averages[0])
    data = array_from_file(args.file)
    l = len(data)
    redacted = """
    if l == 0:
        print("No readings to report!")
        sys.exit()
    """  # already checked that file isn't empty!
    if (n > l) or (n < 1) : n = l
    try:
        avgs = averages(data, n)
    except ValueError:
        print("Bad data found in file")
        sys.exit()
    sp, dp = avgs[:2]
    print(
        "Average valuess (sys/dia pulse)" +
        "of last {} readings are ...\n"
        .format(n) +
        "{:.0f}/{:.0f}  {:.0f}"
        .format(*avgs))
    print("{} / {}"
        .format(
            dev.aha.get_category(sp, 's'),
            dev.aha.get_category(dp, 'd')
            ))
    print(dev.aha.show_calc(sp,dp))


def format_data_cmd(args):
    if check_file(args.file, 'r'):
        report_data = array_from_file(args.file)
        print(report_format
            .format(**dict_for_display(report_data)))


def main():
    args = get_args()

    set_data_file(args)

    if args.add:  # User wants to add data:
        add_cmd(args)

    elif args.averages:  # User wants average of latest readings:
        averages_cmd(args)

    else:
        # we already have a report function that is not a player
        # in this code and perhaps should be renamed.
        # Default behavior is to report.
#       print("...going to default behaviour...")
        format_data_cmd(args)


             

if __name__ == '__main__':
    main()

