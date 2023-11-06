#!/usr/bin/env python

'''Displays the humidex from the air temperature and the dew point based on
the Meteorological Service of Canada formula. Optionally display the
relative humidity.

See http://www.meteo.gc.ca/mainmenu/faq_e.html#weather4b
for more information about the model equations used in this program.

Copyright (C) 2008 Zoé Cassiopée Gauthier <zoe.gauthier@blorp.dev>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.
'''

from optparse import OptionParser
from math import exp
import sys

def error(message, errnum=1):
    sys.stderr.write("%s: %s\n" % (sys.argv[0], message))
    sys.exit(errnum)

usage = "Usage: %prog [options] TEMPERATURE DEWPOINT"
version = "%prog 1.0"
parser = OptionParser(version=version)
parser.add_option("-H", "--humidity", 
                  action="store_true", dest="display_humidity", default=False,
                  help="display relative humidity")
(options, args) = parser.parse_args()

KELVIN = 273.16

if len(args) < 1:
    error("missing temperature value\n", 2)
if len(args) < 2:
    error("missing dew point value\n", 2)

# Read dry temperature and dew point in degrees Celsius.    
try:
    temperature = float(args[0]) + KELVIN
except ValueError:
    error("invalid temperature value\n", 2)
try:
    dewpoint = float(args[1]) + KELVIN
except ValueError:
    error("invalid dew point value\n", 2)

# Calculate vapor pressure in mbar.
e = 6.11 * exp(5417.7530 * ((1 / KELVIN) - (1 / dewpoint)))

# Calculate saturation vapor pressure
es = 6.11 * exp(5417.7530 * ((1 / KELVIN) - (1 / temperature)))
humidity = e / es

h = 0.5555 * (e - 10.0)
humidex = temperature + h - KELVIN

if options.display_humidity:
    print "%d %%" % round(humidity * 100)
else:
    print "%d" % round(humidex)

