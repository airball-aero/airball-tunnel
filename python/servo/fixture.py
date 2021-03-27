import time

class Fixture:

    def __init__(self, devicename):
        self.__devicename = devicename
    
    def moveto(self, az_el):
        print('Moving to %s' % az_el)
        time.sleep(1)
