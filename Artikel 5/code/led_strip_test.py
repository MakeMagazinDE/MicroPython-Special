import time, machine, neopixel

MAX_LEDS = 10
LED_PIN = 5

pixels = neopixel.NeoPixel(machine.Pin(LED_PIN), MAX_LEDS)

def clear():
  for i in range(MAX_LEDS):
    pixels[i] = (0, 0, 0)
  pixels.write()

while True:
  for i in range(MAX_LEDS):
    pixels[i] = (150, 0, 0)
    pixels.write()
    time.sleep(0.2)

  clear()

  for i in reversed(range(MAX_LEDS - 1)):
    pixels[i] = (150, 0, 0)
    pixels.write()
    time.sleep(0.2)

  clear()
