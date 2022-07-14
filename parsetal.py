#!/usr/bin/env python3
#
# Parse tallies out of an MCNP output file
#
# Ondrej Chvala, ondrejch@gmail.com
# MIT license

import sys
import re

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
        break
    else:
        print('ERROR - This should not happen')
        sys.exit(-3)
    tunits = re.findall('units\s+([a-zA-Z0-9_/\*]+)', tdata)[0]
    tparse = re.findall('\n\s+(\w+)\s+\n([\s+[\d,.,E,+,-]+\s+[\d,.,E,+,-]+\s+[\d,.,E,+,-]+\n)+', tdata)
    xaxis  = tparse[0][0]
    with open(f'mytally_{tname}.dat', 'w') as of:
        print('Writing tally ', tname)
        of.write(f'# TALLY {tname}, x-axis: {xaxis}, y-units: {tunits}\n')
        of.write(tparse[0][1])
        of.close()

