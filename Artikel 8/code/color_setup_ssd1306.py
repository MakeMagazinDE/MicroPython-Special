from machine import Pin, I2C
from drivers.ssd1306.ssd1306 import SSD1306_I2C

WIDTH = const(128)
HEIGHT = const(64)

i2c = I2C(1, scl = Pin(22), sda = Pin(21))
ssd = SSD1306_I2C(WIDTH, HEIGHT, i2c)
