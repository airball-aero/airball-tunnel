#!/usr/bin/env python

'''Sweep a range of alpha/beta values and write the output to a CSV file.'''

import sys
import alphabeta
import time
from servo.dynamixelv2_0 import Fixture
from pressure.pressurescanner import PressureScanner

WAIT_TIME=1.0
NUM_READINGS=100

if len(sys.argv) != 4:
    device_servo = input('Enter servo device name (e.g. /dev/ttyUSB*): ')
    device_pressure = input('Enter pressure device name (e.g. /dev/ttyUSB*): ')
    file_name = input('Enter file name for output (e.g., output.csv): ')
else:
    device_servo = sys.argv[1]
    device_pressure = sys.argv[2]
    file_name = sys.argv[3]

f = Fixture(device_servo)
s = PressureScanner(device_pressure)

for alpha in range(-24, 24 + 1, 6):
    for beta in range(-24, 24 + 1, 6):
        print('Moving to alpha=%f, beta=%f' % (alpha, beta))
        az_el = alphabeta.alpha_beta_to_az_el([alpha, beta])
        f.moveto(az_el)
        print('Sleeping for %f sec' % WAIT_TIME)
        time.sleep(WAIT_TIME)
        print('Reading %f points' % NUM_READINGS)
        readings = s.read(100)
        print('Writing')
        with open(file_name, 'a') as of:
            for r in readings:
                of.write(
                    ','.join(
                        map(str, [alpha, beta] + r)) + '\n')
