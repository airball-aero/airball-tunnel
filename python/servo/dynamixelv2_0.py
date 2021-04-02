import servo.dynamixel
import dynamixel_sdk
import sys
import time

# Control table address
ADDR_PRO_TORQUE_ENABLE      =  64
ADDR_PRO_POSITION_D_GAIN    =  80
ADDR_PRO_POSITION_I_GAIN    =  82
ADDR_PRO_POSITION_P_GAIN    =  84
ADDR_PRO_PROFILE_VELOCITY   = 112
ADDR_PRO_GOAL_POSITION      = 116
ADDR_PRO_MOVING             = 122
ADDR_PRO_PRESENT_POSITION   = 132

# Protocol version
PROTOCOL_VERSION            = 2.0

# Default setting
BAUDRATE                    = 57600

TORQUE_ENABLE               = 1
TORQUE_DISABLE              = 0

VELOCITY                    = 25

POSITION_P_GAIN             = 1000
POSITION_I_GAIN             = 1000
POSITION_D_GAIN             = 100

DXL_MINIMUM_POSITION_VALUE  = 10
DXL_MAXIMUM_POSITION_VALUE  = 4000
DXL_MOVING_STATUS_THRESHOLD = 0

ID_AZ                       = 1
ID_EL                       = 2

MOVING_THRESHOLD            = 5

class Fixture(servo.dynamixel.Fixture):
    
    def __init__(self, device_name, verbose=False):
        super().__init__(device_name)
        self.__verbose = verbose
        self.__port_handler = dynamixel_sdk.PortHandler(self.__device_name)
        self.__packet_handler = dynamixel_sdk.PacketHandler(PROTOCOL_VERSION)
        if not self.__port_handler.openPort():
            print('Connection failed.')
            sys.exit(-1)
        self.__port_handler.setBaudRate(BAUDRATE)
        for id in [ID_AZ, ID_EL]:
            self.write_4_byte(id, ADDR_PRO_PROFILE_VELOCITY, VELOCITY)
            self.write_2_byte(id, ADDR_PRO_POSITION_P_GAIN, POSITION_P_GAIN)
            self.write_2_byte(id, ADDR_PRO_POSITION_I_GAIN, POSITION_I_GAIN)
            self.write_2_byte(id, ADDR_PRO_POSITION_D_GAIN, POSITION_D_GAIN)
            self.write_1_byte(id, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
    
    def moveto(self, az_el):
        counts = list(map(self.count, az_el))
        self.go_motor(ID_AZ, counts[0])
        self.go_motor(ID_EL, counts[1])
        self.await_motor(ID_AZ, counts[0])
        self.await_motor(ID_EL, counts[1])

    def count(self, degrees):
        """Convert angle in degrees to servo counts."""
        return int((float(degrees) / 0.0879) + 2048)
        
    def handle_result(self, dxl_comm_result, dxl_error):
        """Handle results of a call to the Dynamixel servos.

        Args:
            dxl_comm_result: The result of the communications.
            dxl_error: The error code returned.
        """
        if dxl_comm_result != dynamixel_sdk.COMM_SUCCESS:
            print('%s' % self.__packet_handler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print('%s' % self.__packet_handler.getRxPacketError(dxl_error))

    def write_1_byte(self, id, addr, data):
        dxl_comm_result, dxl_error = self.__packet_handler.write1ByteTxRx(
            self.__port_handler, id, addr, data)
        self.handle_result(dxl_comm_result, dxl_error)

    def write_2_byte(self, id, addr, data):
        dxl_comm_result, dxl_error = self.__packet_handler.write2ByteTxRx(
            self.__port_handler, id, addr, data)
        self.handle_result(dxl_comm_result, dxl_error)
        
    def write_4_byte(self, id, addr, data):
        dxl_comm_result, dxl_error = self.__packet_handler.write4ByteTxRx(
            self.__port_handler, id, addr, data)
        self.handle_result(dxl_comm_result, dxl_error)

    def read_4_byte(self, id, addr):
        data, dxl_comm_result, dxl_error = self.__packet_handler.read4ByteTxRx(
            self.__port_handler, id, addr)
        self.handle_result(dxl_comm_result, dxl_error)
        return data

    def read_1_byte(self, id, addr):
        data, dxl_comm_result, dxl_error = self.__packet_handler.read1ByteTxRx(
            self.__port_handler, id, addr)
        self.handle_result(dxl_comm_result, dxl_error)
        return data

    def log(self, s):
        if self.__verbose: print(s)
        
    def go_motor(self, id, count):
        """Command a motor to slew to a given count.
        
        Args:
            id: The motor ID on the Dynamixel chain.
            count: The desired count
        """
        self.log('go_motor(%s, %s)' % (id, count))
        self.log('  goal = %s' % count)
        self.write_4_byte(id, ADDR_PRO_GOAL_POSITION, count)

    def await_motor(self, id, count):
        """Wait for a motor to reach a given count.

        Args:
            id: The motor ID on the Dynamixel chain.
            count: The desired count
        """
        while 1:
            present = self.read_4_byte(id, ADDR_PRO_PRESENT_POSITION)
            delta = abs(count - present)
            self.log('  %s - Δ = %s' % (id, delta))
            if not delta > MOVING_THRESHOLD:
                break
