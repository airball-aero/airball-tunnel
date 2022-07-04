from pressure.calibration import Calibration
from pressure.sweep import Sweep
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import math
import numpy as np
import sys

class Plotter:

    def __init__(self):
        self.__fig__ = plt.figure()
        self.__ax__ = self.__fig__.add_subplot(1, 1, 1, projection='3d')
        self.__ax__.set_xlabel('alpha (degrees)')
        self.__ax__.set_ylabel('beta (degrees)')

    def add_data(self, channels, chan):
        self.__ax__.scatter3D(channels.alpha,
                              channels.beta,
                              channels[chan],
                              label=channels.label + ('[%d]' % chan))

    def show(self):
        self.__ax__.legend()
        plt.show()
        
if __name__ == '__main__':
    s = Sweep.read('../data/2022-07/roomfan.csv',
                   '../data/2022-07/esp32_scanner.cal')
    p = Plotter()
    p.add_data(s.data, 1)
    p.add_data(s.sigma, 1)
    p.show()
