from xbee import XBeeEmulator as XBee

MAC_ADDRESS = "0013A200424366C7"

device = XBee(mac_address=MAC_ADDRESS)

# device.close()

device.open()

# device.open()

# device.close()