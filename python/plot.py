#!/usr/bin/env python

from pressure.calibration import Calibration
from pressure.sweep import Sweep
from pressure.plotter import Plotter

s = Sweep.read('../data/2022-07/roomfan.csv',
               '../data/2022-07/esp32_scanner.cal')
s = s.asymmetry()

p = Plotter()
p.add_data(s.data, 2)
p.add_data(s.sigma, 2)
p.show()
