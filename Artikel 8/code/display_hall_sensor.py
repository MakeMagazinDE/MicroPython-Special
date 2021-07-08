from machine import Pin, I2C
import ssd1306, esp32, time

SAMPLES = const(1000)
WIDTH = const(128)
HEIGHT = const(64)
MAX_HALL = const(700)

def clean_hall_read():
  value = 0;
  for i in range(SAMPLES):
    value += esp32.hall_sensor()
    time.sleep_us(100)
  return value // SAMPLES

def convert(x, imin, imax, omin, omax):
  v = (x - imin) * (omax - omin) // (imax - imin) + omin
  return max(min(omax, v), omin)

i2c = I2C(1, scl = Pin(22), sda = Pin(21))
display = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

while True:
  hall_value = abs(clean_hall_read())
  width = convert(hall_value, 0, MAX_HALL, 0, WIDTH)
  value_text = str(hall_value)
  xpos = (WIDTH - len(value_text) * 8) // 2
  display.fill(0)
  display.text(value_text, xpos, 2)
  display.fill_rect(0, 28, width, 8, 1)
  display.show()
