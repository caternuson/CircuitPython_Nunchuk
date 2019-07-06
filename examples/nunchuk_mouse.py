import board
import nunchuk
from adafruit_hid.mouse import Mouse

STEP = 5
m = Mouse()
nc = nunchuk.Nunchuk(board.I2C())

while True:
    x, y = nc.joystick
    if x < 100:
        m.move(-STEP, 0, 0)
    if x > 150:
        m.move( STEP, 0, 0)
    if y < 100:
        m.move( 0, STEP, 0)
    if y > 150:
        m.move( 0,-STEP, 0)
    if nc.button_Z:
        m.click(Mouse.LEFT_BUTTON)
    if nc.button_C:
        m.click(Mouse.RIGHT_BUTTON)