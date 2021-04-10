import pressure.source
import socket


class Source(pressure.source.Source):
    """Pressure source that connects to a Scanivalve DSA 3217 over TCP/IP."""

    def __init__(self):
        self.__file_r = None
        self.__file_w = None

    def scan(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('191.30.80.175', 23))
        self.__file_r = s.makefile(mode='r')
        self.__file_w = s.makefile(mode='w')
        self.set_var('EU', 1)
        self.set_var('BIN', 0)
        self.set_var('FORMAT', 0)
        self.set_var('FPS', 0)
        self.set_var('AVG', 16)
        self.set_var('PERIOD', 20000)
        self.send('SCAN')
        lines = self.get_scan_lines()
        self.__file_r = None
        self.__file_w = None
        s.close()
        return [
            float(lines[i].split(' ')[1])
            for i in range(1, len(lines))
        ]

    def set_var(self, var, value):
        self.send('SET ' + var + ' ' + str(value))

    def send(self, str):
        print('send(%s)' % str)
        self.__file_w.write(str + '\n')

    def get_scan_lines(self):
        return [
            self.readline()
            for i in range(0, 1 + 16)
        ]

    def readline(self):
        return self.__file_r.readline()
