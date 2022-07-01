#!/usr/bin/env python3

# File: get_averages.py

infile = 'data/bp_numbers.txt'

print(infile)

def add3values(sums, values):
    for n in range(len(values)):
        sums[n] += values[n]

def collect_averages(infile):
    with open(infile, 'r') as stream:
        denominator = 0
        totals = [0, 0, 0]
        for line in stream:
            if line:
                parts = [int(val) for val in line.split()[:3]]
                add3values(totals, parts)
                denominator += 1
    return [total/denominator for total in totals]  

if __name__ == '__main__':
    print(collect_averages(infile))
