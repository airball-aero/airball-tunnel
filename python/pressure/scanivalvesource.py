import pressure.source
import random
import socket

class Source(pressure.source.Source):
    '''Pressure source that connects to a Scanivalve DSA 3217 over TCP/IP.'''

    def __init__(self):
        self.set_var('EU', 1)
        self.set_var('BIN', 0)
        self.set_var('FORMAT', 0)

    def __init_todo__(self):
        # TODO: Add these to the beginning of __init__().
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('TODO: IP address of Scanivalve', 23))
        self.__file = s.makefile()
        
    def scan(self):
        self.send('SCAN')
        lines = self.get_scan_lines()
        return [
            float(lines[i].split(' ')[1])
            for i in range(2, len(lines))
        ]

    def set_var(self, var, value):
        self.send('SET ' + var + ' ' + str(value))

    def send(self, str):
        print('Sending to Scanivalve: %s' % str)

    def send_todo(self, str):
        # TODO: Replace send() with this.
        self.__file.write(str + '\n')
        
    def get_scan_lines(self):
        lines = [
            'Frame # 123',
            'Time 12345 µs',
        ] + [
            str(i) + ' ' + str(random.uniform(0, 100)) + ' ' + str(random.uniform(25, 29))
            for i in range(0, 16)
        ]
        for l in lines:
            print('Received from Scanivalve: %s' % l)
        return lines

    def get_scan_lines_todo(self):
        # TODO: replace get_scan_lines() with this.
        return [
            (self.__file.readline()).strip()
            for i in range(0, 2 + 16)
        ]
