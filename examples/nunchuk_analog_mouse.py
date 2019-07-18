import board
import nunchuk
from adafruit_hid.mouse import Mouse
import time

m = Mouse()
nc = nunchuk.Nunchuk(board.I2C())

centerX = 128
centerY = 128

scaleX = 0.3
scaleY = 0.3

cDown = False
zDown = False

CHECK_COUNT=0
#x,y = nc.joystick

while True:
    print((0 if nc.button_C else 1, 0 if nc.button_Z else 1))

while True:
    x, y = nc.joystick
    if (x == 255 or y == 255):
        continue
    relX = x - centerX
    relY = centerY - y

    m.move(int(scaleX * relX), int(scaleY * relY), 0)

    c = nc.button_C
    z = nc.button_Z

    if z and not zDown:
        stillDown = True
        for n in range(CHECK_COUNT):
            if nc.button_Z:
                stillDown = False
                break
        if stillDown:
            m.press(Mouse.LEFT_BUTTON)
            zDown = True
    elif not z and zDown:
        stillDown = True
        for n in range(CHECK_COUNT):
            if not nc.button_Z:
                stillDown = False
                break
        if stillDown:
            m.release(Mouse.LEFT_BUTTON)
            zDown = False
    if c and not cDown:
        m.press(Mouse.RIGHT_BUTTON)
        cDown = True
    elif not c and cDown:
        m.release(Mouse.RIGHT_BUTTON)
        cDown = False