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

#?! A bad name! It's a data file not a report file.
data_file = 'bp_numbers.txt'

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

invalid_lines = []  # to be used when -v --verbose option is implemented.


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


def no_date_stamp(data):
    if data[3] == 0:
        return True


def filter_data(data, args):
    """
    """
    ret = []
    ok = True
    for item in data:
        if args.time_of_day and not time_of_day_filter(data,
                time_of_day[0], time_of_day[1]):
            continue
        if args.date_range and not date_range_filter(data, 
                date_range[0], date_range[1]):
            continue
        if args.not_before_date and not not_before_filter(data,
                not_before):
            continue
        ret.append(item)
    n = args.number2consider
    if n != 0:
        l = len(ret)
        if l == 0:
            print("No readings to report!")
            sys.exit()
        if (n > l) or (n < 1):
            n = l
        ret = ret[-n:]
    return ret


def time_of_day_filter(data, begin, end):
    if no_date_stamp(data):
        return
    time = int(str(data[3]).split('.')[-1])
    if time >= begin and time <= end:
        return True


def date_range_filter(data, begin, end):
    if no_date_stamp(data):
        return
    day = int(str(data[3]).split('.')[0])
    if day >= begin and day <= end:
        return True


def not_before_filter(data, date):
    if no_date_stamp(data):
        return
    day = int(str(data[3]).split('.')[0])
    if day >= date:
        return True


def valid_data(line, invalid_lines=None):
    """
    Accepts what is assumed to be a valid line.
    If valid, returns a 4 tuple (int, int, int, float).
    If not valid and if <invalid_lines> is not None,
    assumes errors is a list to which the invalid line is added.
    """
    data = line.split()
    if len(data) == 4:
        try:
            for i in range(3):
                data[i] = int(data[i])
            data[3] = float(data[3])
        except ValueError:
            if invalid_lines != None:
                invalid_lines.append(line)
            return
    else:
        if invalid_lines != None:
            invalid_lines.append(line)
        return
    return (tuple(data))


def array_from_file(report_file, invalid_lines=None):
    """
    Input is the report file: four (string) values per line.[1]
    Output is a list of 4 tuples: (int, int, int, float).
    Tuples are: systolic, diastolic, pulse, time stamp.[1]
    [1] Each of the 4 strings represents a number:
    first three are integers, last (the fourth) is a float.
    #? the last isn't really a float: it's YYYYmmdd.hhmm
    #? a string representation of a timestamp!
    """
    res = []
    with open(report_file, 'r') as stream:
        for line in useful_lines(stream):
            numbers = valid_data(line, invalid_lines=invalid_lines)
            if numbers:
                res.append(numbers)
    return res
 

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
        if n < 1:
            print(
            "Number of data to consider can not be less than one!")
            assert False
        if n > l: n = l
        data = data[-n:]
    else:
        n = l
    sys_sum = dia_sum = pul_sum = 0
    for vals in data:
        sys_sum += vals[0]
        dia_sum += vals[1]
        pul_sum += vals[2]
#   print((sys_sum, dia_sum, pul_sum))  # debug
#   print(n)                            # debug
    return [round(val/n) for val in (sys_sum, dia_sum, pul_sum)]


def display_averages(averages):
    """
    <averages> is a length 3 iterable of floats.
    """
    return ('{:.0f}/{:.0f} {:.0f}'
            .format(*averages))

#!! What follows consist of AHA related
#!! functionality pulled out of /dev

# Numeric representation of the criteria used to classify
# (individual single number) blood pressure readings:
# s == systolic values; d == diastolic values
# Note: these do _not_ correspond with the 'unified' system.
s =  (50, 70, 90, 100, 121, 130, 140, 160, 180, 211, )
d = (35, 40, 60,  65,  81,  85,  90, 100, 110, 121, )
categories = ('Extreme hypotension',        # 0
              'Severe hypotension',         # 1
              'Moderate hypotension',       # 2
              'Low normal BP',              # 3
              'Ideal BP',                   # 4
              'High normal BP',             # 5
              'Pre-hypertension',           # 6
              'Stage I hypertension',       # 7
              'Stage II hypertension',      # 8
              'Stage III hypertension',     # 9
              'Hypertensive crisis',        #10
             )


def get_category(bp, sord):
    """
    Given:
        <bp>: a single (systolic or diastolic) reading.
      & <sord>: a string that begins with an 's' or a 'd',
        to specifiy if <bp> is systolic or diastolic:
    returns a category.
    """
    if sord.startswith('s'):
        sord = s
    elif sord.startswith('d'):
        sord = d
    else:
        print("Must specify systolic or diastolic.")
        sys.exit()
    for n in range(len(sord)):
        category = categories[n]
        if int(bp) < sord[n]:
            return categories[n]
    return categories[-1]


# -------  calculate  -----------#

def get_unified_status(sp, dp):
    """
    The calculator returns a TEXT REPRESENTATION of AHA status
    based on the blood pressure provided (<sp>/<dp>).
    The rules:
    Blood Pressure Status     Systolic (mm Hg) IF  Distolic (mm Hg)
                                 Min     Max       Min     Max
    Normal Blood Pressure   	    <120      and      <80
    Pre-hypertension             120     139  or    80      89
    Stage I High Blood Pressure  140     159  or    90      99
    (Hypertension)
    Stage II High Blood Pressure 160 	180   or   100     110
    (Hypertension)
    Hypertensive crisis             >180      or       >110
    (where emergency care is required)
    """
    if sp < 120 and dp < 80: return 'Normal BP'
    if (sp >=120 and sp <140) or (dp >=80 and dp < 90):
        return 'Pre-hypertension'
    if (sp >=140 and sp <160) or (dp >=80 and dp <= 99):
        return 'Stage I hypertension'
    if (sp >=160 and sp <180) or (dp >=100 and dp <= 110):
        return 'Stage II hypertension'
    if sp > 180 or dp > 110: return 'Hypertensive crisis'
    assert False


def calc(sp, dp):
    sp, dp = int(sp), int(dp)
    mean = round((2 * dp + sp)/3)
    pp = sp - dp
    status = get_unified_status(sp, dp)
    return mean, pp, status


def show_calc(sp, dp):
    mean, pp, status = calc(sp, dp)
    return f"Mean BP: {mean}, Pulse pressure: {pp}, Status: {status}"

#!! End of what was pulled out of /dev


#!! The functions that follow are ones that Leam would prefer
#!! be put back into the 'if __name__ == "__main__":' clause.
#!! I'll leave that to be done later (another issue.)

def get_args():
    """
    -d, -n, or the "time of day" option was used?
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--add",
        nargs=3,
        help = "Add in the order of systolic, diastolic, pulse",
        )
    parser.add_argument(
        "-f", "--file",
        help = "Report file (default bp_numbers.txt)",
        default=data_file
        )
    parser.add_argument(
        "-n", "--number2average",
        nargs=1,
        type=int,
        help = (
        """Average the most recent NUMBERS2AVERAGE values, 0 for all;
if other filters are set, they are applied first."""),
        default=0,
        )
    parser.add_argument(
        "-t", "--time_of_day",
        nargs=2,
        type=int,
        help = "Ignore readings outside of time range",
        default=0,
        )
    parser.add_argument(
        "-r", "--date_range",
        nargs=2,
        type=int,
        help = "Only consider readings within the date range",
        default=0,
        )
    parser.add_argument(
        "-d", "--not_before_date",
        nargs=1,
        type=int,
        help = "Ignore readings prior to NOT_BEFORE_DATE",
        default=0,
        )
    return parser.parse_args()


def set_data_file(args):
    """
    Modify data file prn and ..
    Notify user which data file is being used:
    """
    if args.file == data_file:
        print("Using '{}' as data file."
            .format(data_file))
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
            get_category(sp, 's'),
            get_category(dp, 'd')
            ))
    print(show_calc(sp,dp))


def averages_cmd(args):
    if not check_file(args.file, 'r'):
        print("Unable to find ", args.file)
        sys.exit(1)
    n = int(args.number2average[0])
    data = array_from_file(args.file, invalid_lines)
    l = len(data)

    if l == 0:
        print("No readings to report!")
        sys.exit()
    redacted = """
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
            get_category(sp, 's'),
            get_category(dp, 'd')
            ))
    print(show_calc(sp,dp))


def format_data_cmd(args):
    if check_file(args.file, 'r'):
        report_data = array_from_file(args.file, invalid_lines)
        print(report_format
            .format(**dict_for_display(report_data)))


def main():
    args = get_args()

    set_data_file(args)

    if args.add:  # User wants to add data:
        add_cmd(args)

    elif args.number2average:  # User wants average of latest readings:
        averages_cmd(args)

    else:
        # we already have a report function that is not a player
        # in this code and perhaps should be renamed.
        # Default behavior is to report.
#       print("...going to default behaviour...")
        format_data_cmd(args)


             

if __name__ == '__main__':
    main()

