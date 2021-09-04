import servo.dynamixel
from dxl import *
from dxl.dxlcore import *

class Fixture(servo.dynamixel.Fixture):
    '''Fixture for Dyanamixel Protocol 1.0 (e.g., AX-12A) servos.'''

    __az_id = 1
    __el_id = 2
    __speed = 50
    
    def __init__(self, device_name):
        super().__init__(device_name)
        self.__chain = dxlchain.DxlChain(self.__device_name, rate=1000000)
        self.__chain.get_motor_list()
    
    def moveto(self, az_el):
        self.__chain.goto(
            self.__az_id,
            self.count(az_el[0]),
            speed=self.__speed)
        self.__chain.goto(
            self.__el_id,
            self.count(az_el[1]),
            speed=self.__speed)
        
    def count(self, degrees):
        '''Convert angle in degrees to servo counts.'''
        count = int(float(degrees) / 0.29) + 512
        count = max(0, count)
        count = min(1023, count)
        return count
        
