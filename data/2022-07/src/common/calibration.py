import sys
from numpy.polynomial.polynomial import Polynomial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines

NUMSENSORS = 8

class Calibration:

    def __init__(self, path):
        self.__sensors__ = [
            {
                'reading': [],
                'pressure': [],
            }
            for i in range(0, NUMSENSORS)
        ]
        with open(path) as infile:
            while True:
                l = infile.readline()
                if not l: break
                values = l.strip().split(',')
                for i in range(0, NUMSENSORS):
                    self.__sensors__[i]['reading'].append(float(values[i + 1]))
                    self.__sensors__[i]['pressure'].append(float(values[0]))
        for i in range(0, NUMSENSORS):
            self.__sensors__[i]['fit'] = Polynomial.fit(
                self.__sensors__[i]['reading'],
                self.__sensors__[i]['pressure'],                
                1).convert().coef

    def apply(self, readings):
        return [
            self.__sensors__[i]['fit'][0] + self.__sensors__[i]['fit'][1] * readings[i]
            for i in range(0, NUMSENSORS)
        ]

    def sensor(self, i):
        return self.__sensors__[i]

########################################################################
#
# Honeywell TruStability transfer function, from page 11 of:
# https://www.mouser.com/datasheet/2/187/honeywell-sensing-trustability-hsc-series-high-acc-708740.pdf
#
# r = 0.8 * (P - Pmin) / (Pmax - Pmin) + 0.1
# M = 2^14
# o = digital output = (r * M)
#
# Rearranging, we get:
#
# o / M - 0.1 = 0.8 * (P - Pmin) / (Pmax - Pmin)
# 1.25 * (o / M - 0.1) = (P - Pmin) / (Pmax - Pmin)
# (P - Pmin) = (Pmax - Pmin) * 1.25 * (o / M - 0.1)
# P = Pmin + 1.25 * (Pmax - Pmin) * (o / M - 0.1)
#
# For a differential sensor, of range +/- diff_range, we get:
#
# P = diff_range * (2.5 * (o / M - 0.1) - 1)
#
########################################################################

def theoretical_output(reading, diff_range):
    return diff_range * (2.5 * (reading / pow(2, 14) - 0.1) - 1)    
    
def graph_calibration(cal, diff_range, filename):
    all_fit_x = [
        [0 for i in range(0, NUMSENSORS)],
        [pow(2, 14) for i in range(0, NUMSENSORS)],
    ]
    all_fit_y = [
        cal.apply(x)
        for x in all_fit_x
    ]
    for i in range(0, NUMSENSORS):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        
        ax.set(xlabel='Raw reading (counts)',
               ylabel='Pressure (engineering units)',
               title='Calibration for sensor %d' % i)
        
        fit_x = [all_fit_x[j][i] for j in range(0, len(all_fit_x))]
        fit_y = [all_fit_y[j][i] for j in range(0, len(all_fit_y))]
        
        ax.plot(fit_x,
                fit_y,
                label='Calibration least squares fit',
                color='green',
                linewidth=0.5)
        
        theory_x = [0, pow(2, 14)]
        theory_y = [
            theoretical_output(x, diff_range)
            for x in theory_x
        ]
        
        ax.plot(theory_x,
                theory_y,
                label='Published output (range +/- %f)' % diff_range,
                color='blue',
                linewidth=0.5)
        
        ax.scatter(cal.sensor(i)['reading'],
                   cal.sensor(i)['pressure'],
                   label='Calibration points',
                   color='red',
                   marker='x',
                   linewidth=0.5)                   
        
        ax.axhline(0,
                   color='grey',
                   linewidth=0.5)
        ax.axvline(pow(2, 13),
                   color='grey',
                   linewidth=0.5)
        
        ax.legend()

        fig.savefig(filename + '_plot_' + str(i) + '.png', dpi=600)
        
########################################################################

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: ' + sys.argv[0] + ' <cal_file_path> <sensor_diff_range>')
        sys.exit(-1)
    c = Calibration(sys.argv[1])
    graph_calibration(c, float(sys.argv[2]), sys.argv[1])
