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
_I2C_INIT_DELAY = .1
_I2C_READ_DELAY = 0.01

class Nunchuk:
    """Class which provides interface to Nintendo Nunchuk controller."""

    def __init__(self, i2c, address=_DEFAULT_ADDRESS):
        self.buffer = bytearray(6)
        self.i2c_device = I2CDevice(i2c, address)
        time.sleep(_I2C_INIT_DELAY)
        with self.i2c_device as i2c_dev:
            # turn off encrypted data
            # http://wiibrew.org/wiki/Wiimote/Extension_Controllers
            i2c_dev.write(b'\xF0\x55')
            time.sleep(_I2C_INIT_DELAY)
            i2c_dev.write(b'\xFB\x00')

    @property
    def joystick(self):
        """Return tuple of current joystick position."""
        self._read_data()
        return self.buffer[0], self.buffer[1]

    @property
    def button_C(self): #pylint: disable=invalid-name
        """Return current pressed state of button C."""
        return not bool(self._read_data()[5] & 0x02)

    @property
    def button_Z(self): #pylint: disable=invalid-name
        """Return current pressed state of button Z."""
        return not bool(self._read_data()[5] & 0x01)

    @property
    def acceleration(self):
        """Return 3 tuple of accelerometer reading."""
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

    def _read_register(self, address):
        with self.i2c_device as i2c:
            time.sleep(_I2C_READ_DELAY)
            i2c.write(address)
            time.sleep(_I2C_READ_DELAY)
            i2c.readinto(self.buffer)
        time.sleep(_I2C_READ_DELAY)
        return self.buffer
