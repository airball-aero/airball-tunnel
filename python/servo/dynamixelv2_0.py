import servo.dynamixel
import dynamixel_sdk
import sys

# Control table address
ADDR_PRO_TORQUE_ENABLE      = 64
ADDR_PRO_GOAL_POSITION      = 116
ADDR_PRO_PRESENT_POSITION   = 132

# Protocol version
PROTOCOL_VERSION            = 2.0

# Default setting
BAUDRATE                    = 57600

TORQUE_ENABLE               = 1
TORQUE_DISABLE              = 0

DXL_MINIMUM_POSITION_VALUE  = 10
DXL_MAXIMUM_POSITION_VALUE  = 4000
DXL_MOVING_STATUS_THRESHOLD = 0

ID_AZ                       = 1
ID_EL                       = 2

MOVING_THRESHOLD            = 10

class Fixture(servo.dynamixel.Fixture):
    
    def __init__(self, device_name):
        super().__init__(device_name)
        self.__port_handler = dynamixel_sdk.PortHandler(self.__device_name)
        self.__packet_handler = dynamixel_sdk.PacketHandler(PROTOCOL_VERSION)
        if not self.__port_handler.openPort():
            print('Connection failed.')
            sys.exit(-1)
        self.__port_handler.setBaudRate(BAUDRATE)
        for id in [ID_AZ, ID_EL]:
            dxl_comm_result, dxl_error = self.__packet_handler.write1ByteTxRx(
                self.__port_handler,
                id,
                ADDR_PRO_TORQUE_ENABLE,
                TORQUE_ENABLE)
            self.handle_result(dxl_comm_result, dxl_error)
    
    def moveto(self, az_el):
        self.go_motor(ID_AZ, az_el[0])
        self.go_motor(ID_EL, az_el[1])        

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

    def go_motor(self, id, degrees):
        """Command a motor to slew to an angle and wait for completion.
        
        Args:
            id: The motor ID on the Dynamixel chain.
            degrees: The desired angle in degrees.
        """
        goal = self.count(degrees)
        dxl_comm_result, dxl_error = self.__packet_handler.write4ByteTxRx(
            self.__port_handler,
            id,
            ADDR_PRO_GOAL_POSITION,
            goal)
        self.handle_result(dxl_comm_result, dxl_error)
        while 1:
            present, dxl_comm_result, dxl_error = self.__packetHandler.read4ByteTxRx(
                self.__port_handler, id, ADDR_PRO_PRESENT_POSITION)
            self.handle_result(dxl_comm_result, dxl_error)
            if not abs(goal - present) > MOVING_THRESHOLD:
                break
