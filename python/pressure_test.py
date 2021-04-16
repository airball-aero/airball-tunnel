#!/usr/bin/env python

'''Try out the pressure Source.'''

import time

from pressure.bogovalvesource import Source

s = Source()

while True:
     print(s.scan())
     time.sleep(1)
