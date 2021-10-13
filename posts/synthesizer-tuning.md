---
title: Synthesizer tuning
date: 2007-11-19
tags:
- electronics
layout: layouts/post.njk
---
A typical modular synthesizer is not limited to a number of fixed pitches, but can generate sounds in a very wide range
of frequencies. However, if one needs to play the synth much like any other standard Western musical instrument, it
will need to be tuned. The pitch relations between notes are generally handled by a MIDI to control voltage (CV)
converter, or a quantizer. Tuning is usually performed by playing a note — in our case this is standard A above middle
C, or A-440 — on a keyboard and turning on an oscillator with a constant reference pitch, like a virtual tuning fork.
The main oscillator is tuned when no beats can be detected.

In my synthesizer, I now need a precise reference oscillator. There is a design by
[Dave Brown](http://www.modularsynthesis.com/a440/A440.htm) using the timers of a small AVR microcontroller to create
a very accurate square wave. This signal is then transformed into a pure sine wave by a very sharp low-pass filter that
removes the overtones. Dave does not publish his code on his page but even if I could get help if I asked, I'm reading
the ATtiny25 datasheet and doing it the hard way.

The microcontroller has two timers that can be run from an external clock. There is a prescaler circuit that will
increment the timer counter every power of 2 clock ticks up to 256 ticks per count. The idea here is to use a clock
frequency that when divided by the prescaler will produce a timer very close to a multiple of 440 counts per second.
Dave found that a clock running at 5.0688 MHz divided by 11520 is a very good approximation. The counters are limited
to 8 bits (256 values). So the 5.0688 Mhz clock divided by 64 runs the counter at 79.2 kHz. If we count up to 180 to
start a new pulse we get exactly 440 Hz.
