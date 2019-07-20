"""
`nunchuk`
================================================================================

CircuitPython library for Nintendo Nunchuk controller


* Author(s): Carter Nelson

Implementation Notes
--------------------

**Hardware:**

* `Wii Remote Nunchuk <https://en.wikipedia.org/wiki/Wii_Remote#Nunchuk>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""
import time
from adafruit_bus_device.i2c_device import I2CDevice

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/caternuson/CircuitPython_Nunchuk.git"

_DEFAULT_ADDRESS = 0x52

class Nunchuk:
    """Class which provides interface to Nintendo Nunchuk controller."""

    def __init__(self, i2c, address=_DEFAULT_ADDRESS):
        self.buffer = bytearray(6)
        self.i2c_device = I2CDevice(i2c, address)
        time.sleep(0.1)
        with self.i2c_device as i2c:
            # turn off encrypted data
            # http://wiibrew.org/wiki/Wiimote/Extension_Controllers
            i2c.write(b'\xF0\x55')
            time.sleep(0.1)
            i2c.write(b'\xFB\x00')

    @property
    def joystick(self):
        self._read_data()
        return self.buffer[0], self.buffer[1]

    @property
    def button_C(self):
        return not bool(self._read_data()[5] & 0x02)

    @property
    def button_Z(self):
        return not bool(self._read_data()[5] & 0x01)

    @property
    def acceleration(self):
        self._read_data()
        x = (self.buffer[5] & 0xC0) >> 6
        x |= self.buffer[2] << 2
        y = (self.buffer[5] & 0x30) >> 4
        y |= self.buffer[3] << 2
        z = (self.buffer[5] & 0x0C) >> 2
        z |= self.buffer[4] << 2
        return x, y, z

    def _read_data(self):
        return self._read_register(b'\x00')

    def _read_register(self, address, delay=0.05):
        with self.i2c_device as i2c:
            time.sleep(delay)
            i2c.write(address)
            time.sleep(delay)
            i2c.readinto(self.buffer)
        time.sleep(delay)
        return self.buffer
