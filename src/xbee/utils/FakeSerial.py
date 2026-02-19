import queue

class FakeSerial:
    """
    Minimal pyserial-like object so existing code that checks/uses self.ser keeps working.
    """
    def __init__(self, logger=None):
        self._open = True
        self._rx = queue.Queue()  # optional: allow .read() to return queued bytes
        self.logger = logger

    def close(self):
        self._open = False

    @property
    def is_open(self):
        return self._open

    # pyserial-like methods used in your base XBee code
    def reset_input_buffer(self): ...
    def reset_output_buffer(self): ...

    def write(self, data: bytes):
        # If any legacy code calls self.ser.write(), don't crash.
        # You can log it or ignore it (your emulator probably publishes via transmit_data instead).
        if self.logger:
            self.logger.write(f"FakeSerial.write({len(data)} bytes)", getattr(self.logger, "DEBUG", None))
        return len(data)

    def read(self, n: int = 1) -> bytes:
        # Optional behavior: return bytes if you inject some into _rx.
        # Otherwise behave like a non-blocking serial with timeout=0 => returns b"".
        out = bytearray()
        while n > 0:
            try:
                b = self._rx.get_nowait()
            except queue.Empty:
                break
            out.append(b)
            n -= 1
        return bytes(out)

    # Optional helper: let emulator inject bytes that legacy code reads via ser.read()
    def inject_rx_bytes(self, data: bytes):
        for b in data:
            self._rx.put(b)
