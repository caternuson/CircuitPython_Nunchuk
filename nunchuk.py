# The MIT License (MIT)
#
# Copyright (c) 2019 Carter Nelson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import time
from adafruit_bus_device.i2c_device import I2CDevice

_DEFAULT_ADDRESS = 0x52

class Nunchuk:
    """Class which provides interface to Nintendo Nunchuk controller."""

    def __init__(self, i2c, address=_DEFAULT_ADDRESS):
        self.buffer = bytearray(6)
        self.i2c_device = I2CDevice(i2c, address)
        with self.i2c_device as i2c:
            # turn off encrypted data
            # http://wiibrew.org/wiki/Wiimote/Extension_Controllers
            i2c.write(b'\xf0\x55')
            i2c.write(b'\xfb\x00')

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
            i2c.write(address)
            time.sleep(delay)
            i2c.readinto(self.buffer)
        return self.buffer

