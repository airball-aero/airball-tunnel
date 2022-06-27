import serial

NUMSENSORS=8

class PressureScanner:

    def __init__(self, path, baud):
        self.__path__ = path
        self.__baud__ = baud

    def read(self, n):
        readings = []
        with serial.Serial(self.__path__, self.__baud__) as port:
            for i in range(0, n):
                r = port.readline().decode().strip().split(',')
                if len(r) != NUMSENSORS + 1:
                    continue
                readings.append([int(k) for k in r[1:]])
        return readings
