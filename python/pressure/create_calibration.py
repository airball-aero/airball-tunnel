# Create a sensor calibration file

import sys
from pressure.pressurescanner import PressureScanner

NUMVALUES = 128

def mean(values):
    return int(round(sum(values) / len(values)))

########################################################################

if __name__ == '__main__':

    if len(sys.argv) != 4:
        print('Usage: ' + sys.argv[0] + ' <device_path> <baud_rate> <cal_file_path>')
        sys.exit(-1)

    device_path = sys.argv[1]
    baud_rate = int(sys.argv[2])
    cal_file_path = sys.argv[3]

    scanner = PressureScanner(device_path, baud_rate)

    while True:
        pressure = float(input('Enter test pressure (^C when done): '))
        input('Hit Enter to take readings')
        readings = scanner.read(NUMVALUES)
        averages = [
            mean([r[i] for r in readings])
            for i in range(0, len(readings[0]))
        ]
        with open(cal_file_path, 'a') as outfile:
            print(
                '%f,%s' %
                (pressure, ','.join(map(str, averages))),
                file=outfile)
