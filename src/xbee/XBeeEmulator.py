import queue
from serial_io import ISerial
from xbee import XBee
from xbee.frames import x81, x88, x89 # Frame parser for classes for each Xbee frame type
from logger import Logger    # Custom logging class

class XBeeEmulator(ISerial):

    def __init__(self, port: str = None, baudrate: int = 115200, status: bool = False, logger: Logger = None, config_file: str = None):
        """Initialize serial connection

        Args:
          port: Port of serial device.
          baudrate: Baudrate of serial device (/port)
          status: Automatically receive status packets after a transmission.
          logger: Logger instance
        """
        self.port = port    # Serial port to use
        self.baudrate = baudrate     # Communication speed  
        self.ser = None      # Will hold the actual Serial object
        self.status = status     # If True, it will try to read back status frames (0x89)
        
        if logger is None:  
            self.logger = Logger()   # Create logger if not provided
            self.logger.write("LOGGER CREATED By XBeeEmulator.py")
        else:
            self.logger.write("XBeeEmulator")
            self.logger = logger
        self.timeout = 0.1 # Allow programmer to configure timeout? # Max time to wait for responses
        self.status_timeout = 0.2
        self.frame_id = 0x01    # Frame ID (used to track commands)

        self.config_file = config_file # Add AT_Config.py file  # Path to config file with AT commands 

        # Retrieve Queues
        self.x81_queue: queue.Queue = queue.Queue()
        self.x88_queue: queue.Queue = queue.Queue() # If working properly, this queue should never have more than 1 element
        self.x89_queue: queue.Queue = queue.Queue()

        # Transmit Queue
        self.transmit_queue: queue.Queue = queue.Queue()

        # self.__transmitting = False # Flag: are we currently sending?
        # self.__receiving = False    # Flag: are we currently receiving?d1b2fd40841964d904a7927082

        self.logger.write(f"port: {self.port}, baudrate: {self.baudrate}, timeout: {self.timeout}, config_file: {self.config_file}")    # Log configuration for debugging

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