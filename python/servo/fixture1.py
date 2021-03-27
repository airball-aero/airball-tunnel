import servo.fixture
from dxl import *
from dxl.dxlcore import *

class Fixture(servo.fixture.Fixture):

    __az_id = 1
    __el_id = 2
    __speed = 50
    
    def __init__(self, devicename):
        super(self.__class__, self).__init__(devicename)
        self.__chain = dxlchain.DxlChain(self.__devicename, rate=1000000)
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
        count = int(float(degrees) / 0.29) + 512
        count = max(0, count)
        count = min(1023, count)
        return count
        
