import pressure.source
import random
import socket

class Source(pressure.source.Source):

    def __init__(self):
        self.set_var('EU', 1)
        self.set_var('BIN', 0)
        self.set_var('FORMAT', 0)

    def __init_todo__(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('????', 23))
        self.__file = s.makefile()
        
    def scan(self):
        lines = self.get_scan_lines()
        return [
            float(lines[i].split(' ')[1])
            for i in range(2, len(lines))
        ]

    def set_var(self, var, value):
        self.send('SET ' + var + ' ' + str(value))

    def send(self, str):
        print('sending ' + str)

    def send_todo(self, str):
        self.__file.write(str + '\n')
        
    def get_scan_lines(self):
        hdr = [
            'Frame # 123',
            'Time 12345 µs',
        ]
        data = [
            str(i) + ' ' + str(random.uniform(0, 100)) + ' ' + str(random.uniform(25.0, 29.0))
            for i in range(0, 16)
        ]
        return hdr + data

    def get_scan_lines_todo(self):
        send('SCAN')
        return [
            self.__file.readline()
            for i in range(0, 2 + 16)
        ]
