# import queue
import os
# import threading

# from xbee import XBee
# from xbee.frames import x81, x88, x89 # Frame parser for classes for each Xbee frame type
# from logger import Logger    # Custom logging class
# from xbee.utils import MqttClient
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("host")
PORT = int(os.getenv("port"))
KEEPALIVE = int(os.getenv("keepalive"))

# class XBeeEmulator(XBee):

#     def __init__(self, *args, logger: Logger = None, pan_id = 3332, mac_address: str = "", **kwargs):
#         """Initialize serial connection

#         Args:
#             port: Port of serial device.
#             baudrate: Baudrate of serial device (/port)
#             status: Automatically receive status packets after a transmission.
#             logger: Logger instance
#         """
#         print("!! RUNNING XBeeEmulator !!")

#         self.pan_id = pan_id
#         self.mac_address = mac_address

#         self.logger = logger or Logger()

#         if logger is None:  
#             self.logger.write("LOGGER CREATED By XBeeEmulator.py")
#         else:
#             self.logger.write("XBeeEmulator")
            
#         super().__init__(*args, logger=self.logger, pan_id=pan_id, mac_address=mac_address, **kwargs)

#         self.client = MqttClient(pan_id, mac_address)
#         self.client.set_username_pw(mac_address, mac_address)

#     def open (self):
#         """Opens the serial port.

#         Returns:
#           True if success, False if failure (There is already an open port, close the port before opening another one).
#         Raises:
#           SerialException if there is an error opening the serial port
#         """

#         # Add try except blocks?
#         def poll_and_write_serial():
#             while self.ser is not None:
#                 # Check if there is a message to transmit
#                 if not self.transmit_queue.empty():
#                     data = self.transmit_queue.get()
#                     self.ser.write(data)
#                 # Check serial port for incomming data
#                 else:
#                     self._retrieve_data()
#             else:
#                 # Normal exit of loop
#                 return 0

#         self.logger.write("Attempting to open serial XBee connection.")

#         if self.ser is not None:
#             self.logger.write(f"A serial connection is already open. ser: {self.ser}")
#             return False
        
#         try:
#             self.client.connect(HOST, PORT, KEEPALIVE)
#             self.ser = True
#             t1 = threading.Thread(target=poll_and_write_serial)
#             t1.start()
        
#         except Exception as e:
#             self.logger.write((f"Error : {e}"))
#             raise Exception(e)

#         self.logger.write("Serial port opened.")
#         return True

#     def close(self) -> bool:
#         """Close serial port.

#         Returns:
#             True if success, False if failure (Error or port already closed).
#         """
#         if self.ser is not None:
#             self.logger.write("Attempting to close serial XBee connection.")

#             self.logger.write("Serial port closed.")
#             return True
        
#         self.logger.write("Serial port is already closed.")
#         return False


#     def transmit_data(self, data) -> bool:
#         """Transmit data.

#         Args:
#             data: String data to transmit.

#         Returns:
#             True if success, False if failure.
#         """
#         return "Transmitting", data

#     def retrieve_data(self):
#         """Read incomming data.

#         Returns:
#             Incomming String data (Deframed data), None if no data.
#         """
#         pass
    
#     def _retrieve_data(self):
#         pass

import json
import time
import queue
import threading
from typing import Optional

from xbee import XBee
from xbee.frames import x81, x89
from logger import Logger
from xbee.utils import MqttClient, FakeSerial

class XBeeEmulator(XBee):
    """
    Emulates an XBee using MQTT instead of a physical serial radio.

    - transmit_data() publishes an RF message over MQTT
    - incoming MQTT messages are converted into x81 frames and pushed to x81_queue
    - retrieveStatus=True produces an x89 TX status frame (success/fail)
    """

    def __init__(
        self,
        *args,
        logger: Logger = None,
        pan_id: int = 3332,
        mac_address: str = "",
        **kwargs
    ):
        self.pan_id = pan_id
        self.mac_address = (mac_address or "").upper()

        self.logger = logger or Logger()
        if logger is None:
            self.logger.write("LOGGER CREATED By XBeeEmulator.py")
        else:
            self.logger.write("XBeeEmulator")

        # init base class (it creates queues, frame_id, etc.)
        super().__init__(*args, logger=self.logger, pan_id=pan_id, mac_address=mac_address, **kwargs)

        # MQTT transport
        self.client = MqttClient(str(pan_id), self.mac_address, on_rf=self._on_rf_message)
        self.client.set_username_pw(self.mac_address, self.mac_address)

        self._running = False

    def open(self) -> bool:
        if self.ser is not None:
            self.logger.write("A connection is already open.")
            return False

        # connect MQTT
        self.client.connect(HOST, PORT, KEEPALIVE)
        self.client.subscribe_rf()

        # IMPORTANT: mark "open" exactly like the real device
        self.ser = FakeSerial(logger=self.logger)

        self.logger.write("XBeeEmulator is open (FakeSerial + MQTT).")
        return True

    def close(self) -> bool:
        if self.ser is None:
            self.logger.write("Connection already closed.")
            return False

        try:
            self.client.disconnect()
        finally:
            # IMPORTANT: mark closed
            try:
                self.ser.close()
            except Exception:
                pass
            self.ser = None

        self.logger.write("XBeeEmulator is closed.")
        return True
    # def open(self) -> bool:
    #     """
    #     "Open" the emulator: connect MQTT and subscribe to RX + broadcast topics.
    #     """
    #     if self._running:
    #         self.logger.write("Emulator already open.")
    #         return False

    #     try:
    #         self.client.connect(HOST, PORT, KEEPALIVE)
    #         self.client.subscribe_rf()
    #         self._running = True
    #         self.logger.write("XBeeEmulator connected to MQTT and subscribed.")
    #         return True
    #     except Exception as e:
    #         self.logger.write(f"Error opening emulator (MQTT): {e}", self.logger.ERROR)
    #         raise

    # def close(self) -> bool:
    #     if not self._running:
    #         self.logger.write("Emulator already closed.")
    #         return False

    #     try:
    #         self.client.disconnect()
    #     finally:
    #         self._running = False
    #         self.logger.write("XBeeEmulator disconnected from MQTT.")
    #     return True

    def transmit_data(self, data: str, address: str = "0000000000000000", retrieveStatus: bool = False) -> Optional[x89]:
        """
        Publish outgoing 'RF' to MQTT.

        address is treated like a 64-bit dest (mac) string in emulator mode.
        If address is all zeros, treat as broadcast.
        """
        if self.ser is None:
            raise Exception("Emulator is not open (MQTT not connected).")

        if isinstance(data, str):
            payload_bytes = data.encode("utf-8")
        elif isinstance(data, (bytes, bytearray)):
            payload_bytes = bytes(data)
        else:
            raise TypeError("data must be str/bytes/bytearray")

        dst64 = (address or "").upper()

        # Capture frame id now (like real XBee)
        current_frame_id = self.frame_id
        self.frame_id = self.frame_id % 0xFF + 0x01

        # Build an RF-ish message envelope
        msg = {
            "v": 1,
            "pan": str(self.pan_id),
            "src64": self.mac_address,
            "dst64": dst64,
            "broadcast": (dst64 == "0000000000000000" or dst64 == "FFFFFFFFFFFFFFFF"),
            "frame_id": current_frame_id,
            "payload": payload_bytes.decode("latin1"),  # byte-safe string
        }

        try:
            if msg["broadcast"]:
                self.client.publish_broadcast(json.dumps(msg))
            else:
                self.client.publish_unicast(dst64, json.dumps(msg))

            # If caller wants TX status, fabricate a success status (0x00)
            if retrieveStatus and current_frame_id != 0:
                status = x89(0x89, current_frame_id, 0x00)  # 0x00 success
                return status

            return None

        except Exception as e:
            self.logger.write(f"Transmit failed: {e}", self.logger.ERROR)
            if retrieveStatus and current_frame_id != 0:
                # 0x21 is a common “network ack failure” style code in some contexts;
                # use whatever your x89/status semantics are.
                return x89(0x89, current_frame_id, 0x21)
            return None

    # The base class already has retrieve_data() which reads from x81_queue.
    # So the key is pushing x81 frames into that queue from MQTT messages.

    def _on_rf_message(self, msg: dict) -> None:
        """
        Called by MqttClient when an MQTT packet arrives.
        Convert it into an x81 frame and enqueue.
        """
        try:
            # Expect JSON string payload in msg_payload
            raw = msg.get("raw_payload")
            if raw is None:
                return

            data = json.loads(raw)
            payload_str = data.get("payload", "")
            payload_bytes = payload_str.encode("latin1")

            # x81 is 16-bit source in your frames model; derive a fake 16-bit addr
            src64 = (data.get("src64") or "0000000000000000").upper()
            src16 = bytes.fromhex(src64[-4:]) if len(src64) >= 4 else b"\x00\x00"

            # Fake RSSI/options
            rssi = -40
            options = 0x00

            # Your x81 constructor expects decoded string data (you used decoded_message)
            try:
                decoded = payload_bytes.decode("utf-8")
            except UnicodeDecodeError:
                decoded = payload_bytes.decode("latin1")

            frame = x81(0x81, src16, rssi, options, decoded)
            self.x81_queue.put(frame)

            self.logger.write(f"Emulator RX from {src64}: {decoded}")

        except Exception as e:
            self.logger.write(f"Failed to parse RF message: {e}", self.logger.ERROR)
