#!/usr/bin/env python

'''Sweep a range of alpha/beta values and write the output to a CSV file.'''

import alphabeta
import time
from pressure.scanivalvesource import Source  #  Pressure data
from servo.dynamixelv2_0 import Fixture  #  servo interface

device_name = input('Enter device name (e.g. /dev/ttyUSB0 or COM1): ')
file_name = input('Enter file name for output (e.g., output.csv): ')

f = Fixture(device_name)
s = Source()

with open(file_name, 'w') as of:
    for alpha in range(-24, 24 + 1, 6):
        for beta in range(-24, 24 + 1, 6):
            f.moveto(alphabeta.alpha_beta_to_az_el([alpha, beta]))
            time.sleep(2.8)
            p = s.scan()
            of.write(
                ','.join(
                    map(str, [alpha, beta] + p)) + '\n')
