#!/usr/bin/env python

'''Displays the wind chill index from the air temperature and the wind
velocity.

See http://www.msc.ec.gc.ca/education/windchill/science_equations_e.cfm
for more information about the model equations used in this program.

Copyright (C) 2008 Zoé Cassiopée Gauthier <zoe.gauthier@blorp.dev>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.
'''

from math import exp
import sys

if len(sys.argv) != 3:
    sys.stdout.write("Usage: %s TEMPERATURE WIND\n" % sys.argv[0])
    sys.exit(1)

try:
    temperature = float(sys.argv[1])
    wind = float(sys.argv[2])
except ValueError:
    sys.stderr.write("%s: invalid value given.\n" % sys.argv[0]);
    sys.exit(2)

chill = 13.12 + (0.6215 * temperature) - (11.37 * wind**0.16) + (0.3965 * temperature * wind**0.16)

print "%d" % round(chill)

