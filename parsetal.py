#!/usr/bin/env python3
#
# Parse tallies out of an MCNP output file
#
# Ondrej Chvala, ondrejch@gmail.com
# MIT license

import sys
import re
import math

# Read input file
try:
    mcnp_outfile = sys.argv[1]
except IndexError:
    print('ERROR: Thescript needs an MCNP Output file as an argument')
    sys.exit(-1)
try:
    fh =  open(mcnp_outfile)
except FileNotFoundError:
    print('EROR: File ',mcnp_outfile,' not found')
    sys.exit(-2)
data = fh.read()

# List of tallies
tallies = re.findall('^1tally\s+(\d+)\s+nps', data, re.MULTILINE)

# Dump tally data
for tname in tallies:
    print('Processing tally ', tname)
    tmatch  = re.findall(f'1tally\s+{tname}.+((?:\n.*)+)bin of tally\s+{tname}', data)
    if len(tmatch) == 1:        # We have results
        tdata = tmatch[0]
    elif len(tmatch) == 0:
        print('No results for tally ',tname,'. Please check')
        continue
    else:
        print('ERROR - This should not happen')
        sys.exit(-3)
    tmatch = re.findall('units\s+([a-zA-Z0-9_/\*]+)', tdata)
    if tmatch == []:
        print("Skipping tally ",tname)
        continue
    tunits = tmatch[0]
    tparse = re.findall('\n\s+(\w+)\s+\n([\s+[\d,.,E,+,-]+\s+[\d,.,E,+,-]+\s+[\d,.,E,+,-]+\n)+', tdata)
    xaxis  = tparse[0][0]
    with open(f'mytally_{tname}.dat', 'w') as of:
        print('Writing tally ', tname)
        of.write(f'# TALLY {tname}, x-axis: {xaxis}, y-units: {tunits}\n')
        of.write(f'# x  y   relsigma(y)     y/dx     y/du\n')
        #of.write(tparse[0][1])
        x0:float =  0.0
        for line in tparse[0][1].splitlines():
            (x, y, yerr) = line.split()
            x1 = float(x)
            dx = x1 - x0
            yperdx = float(y)/dx        # flux per bin width
            if x0 > 0:
                du = math.log(x1/x0)
                yperdu = float(y)/du    # flux per lethargy
            else:
                yperdu = 'NaN'
            of.write(f"{x} {y} {yerr} {yperdx} {yperdu}\n")
            x0 = x1
        of.close()

