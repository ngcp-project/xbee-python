from serial_io import serial_io
from xbee import XBee

class XBeeTester(serial_io):

    def __init__(self):
        pass

    def open(self) -> bool:
        """Opens serial port.

        Returns:
            True if success, False if failure.
        """
        return False

    def close(self) -> bool:
        """Close serial port.

        Returns:
          True if success, False if failure (Error or port already closed).
        """
        pass

    def transmit_data(self, data) -> bool:
        """Transmit data.

        Args:
          data: String data to transmit.

        Returns:
          True if success, False if failure.
        """
        pass

    def retrieve_data(self):
        """Read incomming data.

        Returns:
          Incomming String data (Deframed data), None if no data.
        """
        pass