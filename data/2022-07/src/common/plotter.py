from common.calibration import Calibration
from common.sweep import Channels, read_channels
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

def make_restriction(alpha, beta):
    return lambda a, b: abs(a) <= alpha and abs(b) <= beta
        
if __name__ == '__main__':

    restrict = make_restriction(15, 15)
    
    (s01_05, s01_05_sigma) = read_channels('../data/c01_05.csv',
                                           '../data/esp32_scanner.cal')
    (s01_10, s01_10_sigma) = read_channels('../data/c01_10.csv',
                                           '../data/esp32_scanner.cal')
    (s02_10, s02_10_sigma) = read_channels('../data/c02_10.csv',
                                           '../data/esp32_scanner.cal')
    (s03_10, s03_10_sigma) = read_channels('../data/c03_10.csv',
                                           '../data/esp32_scanner.cal')

    # s01_05 = s01_05.restrict_alphabeta(restrict)
    # s01_10 = s01_10.restrict_alphabeta(restrict)
    # s02_10 = s02_10.restrict_alphabeta(restrict)
    # s03_10 = s03_10.restrict_alphabeta(restrict)

    # s01_05_sigma = s01_05_sigma.restrict_alphabeta(restrict)
    # s01_10_sigma = s01_10_sigma.restrict_alphabeta(restrict)
    # s02_10_sigma = s02_10_sigma.restrict_alphabeta(restrict)
    # s03_10_sigma = s03_10_sigma.restrict_alphabeta(restrict)

    p = Plotter()
    
    p.add_data(s01_05, 6)
    p.add_data(s01_10, 6)
    p.add_data(s02_10, 6)
    p.add_data(s03_10, 6)

    p.add_data(s01_05_sigma, 6)
    p.add_data(s01_10_sigma, 6)
    p.add_data(s02_10_sigma, 6)
    p.add_data(s03_10_sigma, 6)

    p.show()

    (s04_10, s04_10_sigma) = read_channels('../data/c04_10.csv',
                                           '../data/esp32_scanner.cal')

    # p.add_data(s04_10.restrict_alphabeta(restrict), 2)
    # p.add_data(s04_10_sigma.restrict_alphabeta(restrict), 2)    

    p = Plotter()
    
    p.add_data(s04_10, 2)
    p.add_data(s04_10_sigma, 2)

    p.show()
    
