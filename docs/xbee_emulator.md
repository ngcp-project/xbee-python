# XBee Emulator

The `XBeeEmulator` module emulates the connection between XBee RF modules to allow for testing without the need of setting up physical hardware. It utilizes MQTT and its publisher/subscriber architecture and can be used in pace of the base `XBee` module for quick prototyping.

> [!WARNING]
> The `XBeeEmulator` module does not serve as a one to one replacement of the `XBee` module. Please note that there may be discrepancies between the `XBeeEmulator` and `XBee` modules.

## Setup Instructions

In the script where you are importing the XBee library, import the `XBeeEmulator` module instead of the `Xbee` module.

```py
from xbee import XbeeEmulator as XBee
```

Navigate to the xbee library and create a .env file at the following directory:

```bash
./xbee-python/src/xbee/
```

The `.env` file should have the following fields. Set host to the mqtt broker address. You can host a broker yourself, or contact GCS Infrastructure for the broker address:
```env
host= #MQTT HOST ADDRESS
port=8883
keepalive=60
```

## Limitations
TODO

## Known Issues