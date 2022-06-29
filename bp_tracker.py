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
#   Add tests.

import argparse
from datetime import datetime
import os.path

def array_from_file(report_file):
  data = []
  with open(report_file, 'r') as file:
    for line in file:
      line.strip()
      datum = line.split()
      if len(datum) == 4:
        data.append(datum)
  return data
 
def report(report_data):
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
  return highest_systolic_event, highest_diastolic_event, highest_pulse_event, latest_record

def print_report(highest_systolic_event, highest_diastolic_event, highest_pulse_event, latest_record):
  print("Highest Systolic: {}/{} {} {}".format(*highest_systolic_event))
  print("Highest Diastolic: {}/{} {} {}".format(*highest_diastolic_event))
  print("Highest Pulse: {}/{} {} {}".format(*highest_pulse_event))
  print("Latest Record: {}/{} {} {}".format(*latest_record))

def list_collations(report_data):
  """ Takes a data set and returns a tuple of three lists. """
  systolics   = []
  diastolics  = []
  pulses      = []

  for datum in report_data:
    systolics.append(int(datum[0]))
    diastolics.append(int(datum[1]))
    pulses.append(int(datum[2]))

  return systolics, diastolics, pulses


def list_average(l):
  """ Takes a numeric list and returns an integer. """
  average = sum(l) // len(l)
  return average

def list_high_low(l):
  """ Takes a numeric list and returns the highest and lowest entries. """
  return (min(l), max(l))


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
        except Exception as e:
          print("Error processing report data", e)
      else:
        print("Cannot find ", report_file)
     

