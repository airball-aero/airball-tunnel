#!/usr/bin/env python

'''Manual alpha,beta selection for fixture servos'''

import alphabeta
from servo.dynamixelv2_0 import Fixture  # servo interface

device_name = input('Enter device name (e.g. /dev/ttyUSB0 or COM1): ')
f = Fixture(device_name)

Repeat = 1
while Repeat > 0:
    alpha = float(input('Enter desired alpha in degrees: '))
    beta = float(input('Enter desired beta in degrees: '))

    f.moveto(alphabeta.alpha_beta_to_az_el([alpha, beta]))

    print("moving to ",[alpha, beta])

    Repeat = int(input('Repeat?(1 = yes, 0 = no): '))

print('program has been canceled')

