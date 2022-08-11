#!/usr/bin/python3
#
# Generates log-equidistant bins, useful for MCNP tally definition.
#
# Ondrej Chvala, ondrejch@gmail.com
# MIT license
#

import numpy as np
import sys

Nbins  = 500   # number of nins
mybins = 0
try:
    mybins = int(sys.argv[1])
except:
    pass
if mybins > 0:
    Nbins = mybins

expEmin = -10   # 10E{expEmin} MeV
expEmax =  2    # 10E{expEmax] MeV

e_per_line = 6  # records per line

i=0
for e in np.logspace(expEmin, expEmax, Nbins):
    i = i + 1
    print(f'{e:10.4e} ', end='')
    if i % e_per_line == 0:
        print('\n     ', end='')
print()

