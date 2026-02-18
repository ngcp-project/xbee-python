import queue
from xbee import XBee
from xbee.frames import x81, x88, x89 # Frame parser for classes for each Xbee frame type
from logger import Logger    # Custom logging class
import paho.mqtt.client as mqtt

class XBeeEmulator(XBee):

    def __init__(self, *args, logger: Logger = None, mqtt_client: mqtt.Client = None, **kwargs):
    # def __init__(self):
        """Initialize serial connection

        Args:
          port: Port of serial device.
          baudrate: Baudrate of serial device (/port)
          status: Automatically receive status packets after a transmission.
          logger: Logger instance
        """
        print("!! RUNNING XBeeEmulator !!")

        self.logger = logger or Logger()

        if logger is None:  
            self.logger.write("LOGGER CREATED By XBeeEmulator.py")
        else:
            self.logger.write("XBeeEmulator")
            
        super().__init__(*args, logger=self.logger, **kwargs)
        self.mqtt_client = mqtt_client
        

    def open(self) -> bool:
        """Opens serial port.

        Returns:
            True if success, False if failure.
        """

        self.logger.write("Attempting to open serial XBee connection.")

        if self.ser is not None:
            self.logger.write(f"A serial connection is already open. ser: {self.ser}")
            return False
        
        self.ser = True
        
        self.logger.write("Serial port opened.")

    def close(self) -> bool:
        """Close serial port.

        Returns:
          True if success, False if failure (Error or port already closed).
        """
        if self.ser is not None:
            self.logger.write("Attempting to close serial XBee connection.")

            self.logger.write("Serial port closed.")
            return True
        
        self.logger.write("Serial port is already closed.")
        return False


    def transmit_data(self, data) -> bool:
        """Transmit data.

        Args:
          data: String data to transmit.

        Returns:
          True if success, False if failure.
        """
        return "Transmitting", data

    def retrieve_data(self):
        """Read incomming data.

        Returns:
          Incomming String data (Deframed data), None if no data.
        """
        pass