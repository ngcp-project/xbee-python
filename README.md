# XBee Serial Library

> [!Warning]
> Some documentation in this repository may be outdated.

This library allows for the communication between a computer and a XBee RF module over the serial port. 

## Requirements
* Linux, Windows, or macOS
* Python 2.7 or Python 3.4 and newer

## Getting Started
Clone the XBee-Python GitHub repository
```sh
git clone --recurse-submodules https://github.com/ngcp-project/xbee-python.git

# If you forget --recurse-submodules and you already cloned the library: 
# In ./xbee-python
git submodule update --init --recursive
```

> [!Note]
> You may want to create a virtual environment before installing this package. This can be done with the following command.
> ```py
> python -m venv venv
> ```
> See python's [venv](https://docs.python.org/3/library/venv.html) docs for more details.

Install dependencies
```py
pip install -r requirements.txt
```

See the [XBee Serial API][api] page for method details.

See the [Xbee Emulator][xbee_emulator] page if you would like to use the `XBeeEmulator` module.

See the [Examples][examples] page for example implementations of the XBee Serial Library.


## Getting Help
Any questions? Feel free to @ GCS Infrastructure on Discord.

## Resources
* [Finding the serial port (device name)][serial_port]
* [XBee Serial API][api]
* [Examples][examples]
* [Frame Details][frame_details]


<!-- Links -->
[api]: ./docs/api.md
[examples]: ./docs/examples.md
[frame_details]: ./docs/frame_details.md
[serial_port]: ./docs/serial_port.md
[xbee_emulator]: ./docs/xbee_emulator.md