---
layout: post
date: 2008-06-28
title: Owww! It's hot in here!
---
I checked the current weather on the Web to make sure that the very high
humidity was not a product of my imagination. Some clothes from this morning's
laundry have been hanged but at this rate they are not even close to be dry
until tomorrow. Environment Canada confirms: the air is over 90 % saturated
with humidity and humidex is 29.

What really is humidex? I knew that it was supposed to represent the perceived
temperature, but I clicked on the link for more information. It finally reveals
that the formula does not have a strong physical basis. This empirical formula
essentially is <i>H</i> = <i>T</i> + (<i>e</i> − 10), where, <i>T</i> is the
temperature in degrees Celsius and <i>e</i> is the vapor pressure in mbar
calculated from the dew point.

![Chilldex screenshot](/img/chilldex.png)

The site also offers a program named Chilldex to calculate the humidex
and relative humidity based on the temperature and the dew point, but only if
you run Windows... Ha! Let's use our mad Python skillz and create our own
tools! Don't hesitate to modify and share.

[humidex.py](/code/humidex.py)

[windchill.py](/code/windchill.py)

(It will also spare you having to look at a picture of mounted police...)
