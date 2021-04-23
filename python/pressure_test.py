#!/usr/bin/env python

'''Try out the pressure Source.'''

import time

from pressure.scanivalvesource import Source

s = Source()

while True:
     print(s.scan())
     time.sleep(0.1)
