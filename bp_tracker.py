#!/usr/bin/env python3

# name:     bp_tracker.py
# version:  0.0.1
# date:     20220509
# author:   Leam Hall
# desc:     Track and report on blood pressure numbers.

# Notes:
#  Datafile expects three ints and one float, in order.

# TODO
#   Add statistical analysis for standard deviation.
#   Report based on time of day (early, midmorning, afternoon, evening)
#   (?) Add current distance from goal?
#   Error checking for input. Three ints? 
##     -fails if incorrect number of arguments are given
##     -so me thinks no need for this- error message is pretty good
#   Add tests.  - have begun with testing averages func

import argparse
from datetime import datetime
import os.path


def useful_lines(stream, comment="#"):
    """
    A generator which accepts a stream of lines (strings.)
    Blank lines (or white space only) are ignored.
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
  [1] Each element is a string representation of a number:
  first three are integers, last (the fourth) is a float.
  """
  data = []
  with open(report_file, 'r') as stream:
    for line in useful_lines(stream):
      datum = line.split()
      if len(datum) == 4:
        data.append(tuple(datum))
      else:
        # the following print statements are the closest we come to a
        # test of this function.
        print("Badly formated line found in input file:")
        print('"{}"'.format(line))
  return data
 

def report(report_data):
# Suggest renaming 'highest_events_report'
# Why include the latest date??
# ..wouldn't one expect it to always be the last item?
# Also: now where in the code can I find a place where this
# information is used.
  """
  Input is a list of 4 tuples.
  Output is a 4 tuple, each member of which is
  the highest of its category in the input.
  """
  highest_systolic  = 0
  highest_diastolic = 0
  highest_pulse     = 0
  latest            = -1.0
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
    if date > latest:
      latest_record = datum
  return (highest_systolic_event, highest_diastolic_event,
          highest_pulse_event, latest_record,)


def print_report(highest_systolic_event,
                highest_diastolic_event,
                highest_pulse_event,
                latest_record):
  # I'm curious why you include the latest record
  # This function is not used anywhere in the code.
  print("Highest Systolic: {}/{} {} {}".format(*highest_systolic_event))
  print("Highest Diastolic: {}/{} {} {}".format(*highest_diastolic_event))
  print("Highest Pulse: {}/{} {} {}".format(*highest_pulse_event))
  print("Latest Record: {}/{} {} {}".format(*latest_record))


def list_collations(report_data):
  """ Takes a data set and returns a tuple of three lists. """
  # a tuple (immutable) of lists (mutable)? Is that even possible??
  systolics   = []
  diastolics  = []
  pulses      = []

  for datum in report_data:
    systolics.append(int(datum[0]))
    diastolics.append(int(datum[1]))
    pulses.append(int(datum[2]))

  return systolics, diastolics, pulses


def list_average(l):
  """
  Takes a numeric list and returns the average
  expressed as an integer.
  """
  average = sum(l) // len(l)
  return average


def list_high_low(l):
  """ Takes a numeric list and returns the highest and lowest entries. """
  return (min(l), max(l))


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
    return sys_sum/n, dia_sum/n, pul_sum/n


def display_averages(averages):
    return ('{:.1f}/{:.1f} {:.1f}'
            .format(*averages))


if __name__ == '__main__':
    report_file = "data/bp_numbers.txt"

    parser = argparse.ArgumentParser()
    parser.add_argument(
      "-a", "--add",
      nargs=3,
      help = "Add in the order of systolic, diastolic, pulse",
      )
    parser.add_argument(
      "-f", "--file",
      help = "Report file (default data/bp_numbers.txt)",
      default = "data/bp_numbers.txt",
      )
    parser.add_argument(
# How can I add a command line option without it having an argument??
      "-v", "--averages",
      nargs=1,
      help = "Report average of last n values, 0 for all",
      default=0,
      )
    args    = parser.parse_args()

    if args.file:
      report_file = args.file

    if args.add:
      # This format allows sequencing now and parsing later.
      timestamp   = datetime.now().strftime("%Y%m%d.%H%M")
      this_report = args.add
      this_report.append(timestamp) 
      with open(report_file, 'a') as file:
        file.write("{} {} {} {}\n".format(*this_report))
    elif args.averages:
        n = int(args.averages[0])
        data = array_from_file(report_file)
        l = len(data)
        if (n > l) or (n < 1) : n = l
        print(
            "Average valuess (sys/dia pulse)" +
            "of last {} readings are ...\n"
            .format(n) +
            "{:.0f}/{:.0f}  {:.0f}"
            .format(*averages(data, n)))
    else: 
      # Default behavior is to report.
      if os.path.exists(report_file):
        try:
          report_data = array_from_file(report_file)
          systolics, diastolics, pulses  = list_collations(report_data)
          print("Systolic: Average {}, Low {}, High {}".format(
            list_average(systolics),  
            list_high_low(systolics)[0],
            list_high_low(systolics)[1],
          ))
          print("Diastolic: Average {}, Low {}, High {}".format(
            list_average(diastolics),  
            list_high_low(diastolics)[0],
            list_high_low(diastolics)[1],
          ))
          print("Pulse: Average {}, Low {}, High {}".format(
            list_average(pulses),  
            list_high_low(pulses)[0],
            list_high_low(pulses)[1],
          ))
        except Exception as e:
          print("Error processing report data", e)
      else:
        print("Cannot find ", report_file)
     

