#!/usr/bin/env python

'''Try out the servo Fixture.'''

import time

from servo.dynamixel import Fixture

device_name = input('Enter device name (e.g. /dev/ttyUSB0 or COM1): ')

f = Fixture(device_name)

angles = [
     [ 30,  30],
     [ 30, -30],
     [-30, -30],
     [-30,  30],
]

i = 0

while True:
     f.moveto(angles[i])
     i = (i + 1) % len(angles)
     time.sleep(1)
