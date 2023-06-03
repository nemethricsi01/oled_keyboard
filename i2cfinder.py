
import time
import board
import digitalio
import board, busio, displayio, os, terminalio
import adafruit_displayio_ssd1306
import adafruit_displayio_sh1106
from adafruit_display_text import label
import keypad
import supervisor
import rotaryio
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.rect import Rect
import neopixel
from rainbowio import colorwheel
import gc

displayio.release_displays()
sda, scl = board.GP0, board.GP1
i2c = busio.I2C(scl, sda, frequency = 400_000)
while not i2c.try_lock():
    pass
try:
    while True:
        print(
            "I2C addresses found:",
            [hex(device_address) for device_address in i2c.scan()],
        )
        time.sleep(2)

finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
    i2c.unlock()