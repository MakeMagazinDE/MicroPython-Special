from machine import Pin
import uasyncio

led1 = Pin(18, Pin.OUT)
led2 = Pin(19, Pin.OUT)

async def blink(led, delay):
  while True:
    led.on()
    await uasyncio.sleep_ms(delay)
    led.off()
    await uasyncio.sleep_ms(delay)

async def main(led1, led2):
  uasyncio.create_task(blink(led1, 100))
  uasyncio.create_task(blink(led2, 1000))
  await uasyncio.sleep_ms(10000)

uasyncio.run(main(led1, led2))
