#!/usr/bin/env python

'''Try out the servo Fixture.'''

import time
import sys

from servo.dynamixelv2_0 import Fixture

if len(sys.argv) > 1:
     device_name = sys.argv[1]
else:
     device_name = input('Enter device name (e.g. /dev/ttyUSB0 or COM1): ')

f = Fixture(device_name, True)

angles = [
     [ 30,  30],
     [-30, -30],
     [-30,  30],
     [ 30, -30],
]

i = 0

while True:
     f.moveto(angles[i])
     i = (i + 1) % len(angles)
     time.sleep(0.5)
