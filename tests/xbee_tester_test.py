from xbee import XBeeTester

device = XBeeTester()

print(device.transmit_data("Test"))