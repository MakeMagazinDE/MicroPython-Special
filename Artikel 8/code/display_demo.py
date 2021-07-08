from machine import Pin, I2C
import ssd1306

WIDTH = const(128)
HEIGHT = const(64)

i2c = I2C(1, scl = Pin(22), sda = Pin(21))
display = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

display.rect(0, 0, WIDTH, HEIGHT, 1)
display.text('Make-Magazin', 16, 28)
display.show()
