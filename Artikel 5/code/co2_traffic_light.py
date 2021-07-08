import time, neopixel
from machine import I2C, Pin
from scd30 import SCD30

MAX_LEDS = 10
LED_PIN = 5

pixels = neopixel.NeoPixel(Pin(LED_PIN), MAX_LEDS)
i2c = I2C(1, scl = Pin(22), sda = Pin(21), freq = 10000)
scd30 = SCD30(i2c, 0x61)

while True:
  while scd30.get_status_ready() != 1:
    time.sleep_ms(200)
  scd30_values = scd30.read_measurement()
  co2 = int(scd30_values[0])
  
  if co2 < 1000:
    color = (0, 255, 0)
  elif co2 < 2000:
    color = (255, 255, 0)
  elif co2 < 5000:
    color = (160, 32, 240)
  else:
    color = (255, 0, 0)

  for i in range(MAX_LEDS):
    pixels[i] = color
  pixels.write()
