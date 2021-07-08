from machine import Pin, Timer
from time import sleep

led1 = Pin(18, Pin.OUT)
led2 = Pin(19, Pin.OUT)

led1_timer = Timer(0)
led2_timer = Timer(1)

def blink_led1(timer):
  led1.value(not led1.value())

led1_timer.init(
  period = 100,
  mode = Timer.PERIODIC,
  callback = blink_led1)

led2_timer.init(
  period = 1000,
  mode = Timer.PERIODIC,
  callback = lambda timer: led2.value(not led2.value()))

sleep(10)

led1_timer.deinit()
led2_timer.deinit()
