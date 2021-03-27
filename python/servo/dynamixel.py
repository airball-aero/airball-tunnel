import time

class Fixture:
    """Abstract base class for a fixture that controls Dynamixel servos."""

    def __init__(self, device_name):
        """Initialize the fixture.

        Args:
            device_name: Name of serial device.
        """
        self.__device_name = device_name

    def moveto(self, az_el):
        """Move to a given azimuth and elevation.
        
        Args:
            az_el: An array containing azimuth and elevation angles
                in degrees.
        """
        print('Moving to az_el = %s' % az_el)
        time.sleep(1)
