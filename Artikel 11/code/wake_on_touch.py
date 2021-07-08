from machine import Pin, TouchPad, lightsleep
from machine import wake_reason, reset_cause
from time import sleep
import esp32

WAKEUP_THRESHOLD = 500

wakeup_pin = Pin(14, mode = Pin.IN)
touch = TouchPad(wakeup_pin)
touch.config(WAKEUP_THRESHOLD)
esp32.wake_on_touch(True)

def blink_led():
  led = Pin(2, Pin.OUT)
  for n in range(1, 5):
    led.value(1)
    sleep(0.3)
    led.value(0)
    sleep(0.3)

while True:
  blink_led()
  lightsleep()
  print('Wake reason:', wake_reason())
  print('Reset cause:', reset_cause())
