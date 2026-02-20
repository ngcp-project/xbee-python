class FakeSerial:
    """
    Prevents crashes from ser.write(), ser.close(), etc. calls
    """
    def __init__(self, logger=None):
        self._open = True
        self.logger = logger

    @property
    def is_open(self):
        return self._open

    def close(self):
        self._open = False

    def reset_input_buffer(self):
        pass

    def reset_output_buffer(self):
        pass

    def write(self, data: bytes):
        return len(data)

    def read(self, n: int = 1) -> bytes:
        return b""