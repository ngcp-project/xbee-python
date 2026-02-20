import os
from dotenv import load_dotenv
from xbee import XBee
from xbee.utils import MqttClient, FakeSerial
from xbee.frames import x81, x89
from logger import Logger

load_dotenv()
HOST = os.getenv("host")
PORT = int(os.getenv("port"))
KEEPALIVE = int(os.getenv("keepalive"))

# Binary helpers

def _mac64_hex_to_bytes(mac: str) -> bytes:
    mac = (mac or "").replace(":", "").upper()
    if len(mac) != 16:
        raise ValueError(f"mac_address must be 16 hex chars (got {mac!r})")
    return bytes.fromhex(mac)

def _build_envelope(src64_hex: str, payload: bytes, frame_id: int, broadcast: bool) -> bytes:
    """
    Envelope format:
        version (1 byte) = 1
        flags   (1 byte) bit0=broadcast
        frame_id (1 byte)
        src64   (8 bytes)
        payload (N bytes)
    """
    version = 1
    flags = 0x01 if broadcast else 0x00
    src64 = _mac64_hex_to_bytes(src64_hex)
    return bytes([version, flags, frame_id & 0xFF]) + src64 + payload

def _parse_envelope(packet: bytes):
    if not packet or len(packet) < 11:
        raise ValueError("packet too short")
    version = packet[0]
    if version != 1:
        raise ValueError(f"unsupported version {version}")
    flags = packet[1]
    frame_id = packet[2]
    src64 = packet[3:11]      # 8 bytes
    payload = packet[11:]
    broadcast = bool(flags & 0x01)
    return broadcast, frame_id, src64, payload


class XBeeEmulator(XBee):
    def __init__(self, *args, logger: Logger = None, pan_id: int = 3332, mac_address: str = "", **kwargs):
        self.pan_id = pan_id
        self.mac_address = (mac_address or "").upper()

        self.logger = logger or Logger()
        super().__init__(*args, logger=self.logger, pan_id=pan_id, mac_address=mac_address, **kwargs)

        self.client = MqttClient(str(pan_id), self.mac_address, on_rf=self._on_mqtt, use_tls=True)

        self.client.set_username_pw(self.mac_address, self.mac_address)

        self._running = False

    def open(self) -> bool:
        if self.ser is not None:
            self.logger.write(f"Already open. ser={self.ser}")
            return False

        self.client.connect(HOST, PORT, KEEPALIVE)
        self.client.subscribe_rf()

        self.ser = FakeSerial(logger=self.logger)
        self._running = True
        self.logger.write("XBeeEmulator open (MQTT connected; FakeSerial active).")
        return True

    def close(self) -> bool:
        if self.ser is None:
            self.logger.write("Already closed.")
            return False

        try:
            self.client.disconnect()
        finally:
            try:
                self.ser.close()
            except Exception:
                pass
            self.ser = None
            self._running = False

        self.logger.write("XBeeEmulator closed.")
        return True

    def transmit_data(self, data: str, address: str = "0000000000000000", retrieveStatus: bool = False) -> x89 | None:
        if self.ser is None:
            raise Exception("Error: connection is not open (ser is None).")

        current_frame_id = self.frame_id
        self.frame_id = self.frame_id % 0xFF + 0x01

        dst64 = (address or "").upper()
        broadcast = (dst64 == "0000000000000000" or dst64 == "FFFFFFFFFFFFFFFF")

        if isinstance(data, str):
            payload_bytes = data.encode("utf-8")
        elif isinstance(data, (bytes, bytearray)):
            payload_bytes = bytes(data)
        else:
            raise TypeError("data must be str/bytes/bytearray")

        packet = _build_envelope(self.mac_address, payload_bytes, current_frame_id, broadcast)

        try:
            if broadcast:
                self.client.publish_broadcast(packet)
            else:
                self.client.publish_unicast(dst64, packet)

            if retrieveStatus and current_frame_id != 0:
                return x89(0x89, current_frame_id, 0x00)  # success
            return None

        except Exception as e:
            self.logger.write(f"Emulator transmit failed: {e}", self.logger.ERROR)
            if retrieveStatus and current_frame_id != 0:
                return x89(0x89, current_frame_id, 0x21)  # generic failure
            return None

    def _on_mqtt(self, topic: str, payload: bytes):
        """
        Convert MQTT payload -> x81 -> enqueue into the same queue XBee.retrieve_data() uses.
        """
        try:
            _broadcast, _frame_id, src64_bytes, rf_payload = _parse_envelope(payload)

            # Ignore broadcasts from self
            if src64_bytes.hex().upper() == self.mac_address.upper():
                return

            source_address = src64_bytes[-2:]

            rssi = -40
            options = 0x00

            try:
                decoded = rf_payload.decode("utf-8")
            except UnicodeDecodeError:
                decoded = rf_payload.decode("latin1")

            frame = x81(0x81, source_address, rssi, options, decoded)
            self.x81_queue.put(frame)

        except Exception as e:
            self.logger.write(f"MQTT RX parse failed: {e}", self.logger.ERROR)

    def _retrieve_data(self):
        return None