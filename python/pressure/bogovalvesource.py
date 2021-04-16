import pressure.source
import socket


class Source(pressure.source.Source):
    """Pressure source that connects to a BogoValve [tm] over Wi-Fi."""

    def __init__(self):
        pass

    def scan(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('192.168.4.1', 80))
        f = s.makefile(mode='r')
        lines = [
            f.readline()
            for i in range(0, 10)
        ]
        s.close()
        raw_arrays = [
            list(map(float, lines[i].strip().split(',')[1:]))
            for i in range(0, len(lines))
        ]
        num_readings = len(raw_arrays[0])
        avg_array = []
        for j in range(0, num_readings):
            avg = 0.0
            for i in range(0, len(lines)):
                avg += raw_arrays[i][j]
            avg /= num_readings
            avg_array.append(avg)
        return avg_array
