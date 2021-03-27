#!/usr/bin/env python

'''Sweep a range of alpha/beta values and write the output to a CSV file.'''

import alphabeta
from pressure.scanivalvesource import Source  # Fake Scanivalve data
from servo.dynamixel import Fixture  # Dummy servo interface

device_name = input('Enter device name (e.g. /dev/ttyUSB0 or COM1): ')

f = Fixture(device_name)
s = Source()

with open('output.csv', 'w') as of:
    for alpha in range(-45, 45 + 1, 5):
        for beta in range(-45, 45 + 1, 5):
            f.moveto(alphabeta.alpha_beta_to_az_el([alpha, beta]))
            p = s.scan()
            of.write(
                ','.join(
                    map(str, [alpha, beta] + p)) + '\n')
