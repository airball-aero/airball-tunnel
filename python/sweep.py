#!/usr/bin/env python

from servo.fixture1 import Fixture
from pressure.scanivalvesource import Source
import alphabeta

f = Fixture('/dev/ttyACM4')
s = Source()

with open('output.csv', 'w') as of:
    for alpha in range(-45, 45 + 1, 5):
        for beta in range(-45, 45 + 1, 5):
            f.moveto(alphabeta.alpha_beta_to_az_el([alpha, beta]))
            p = s.scan()
            of.write(
                ','.join(
                    map(str, [alpha, beta] + p)) + '\n')
