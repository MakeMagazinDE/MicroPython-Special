from machine import Pin, Timer
from time import sleep
import micropython

led1 = Pin(18, Pin.OUT)
led2 = Pin(19, Pin.OUT)

led1_timer = Timer(0)
led2_timer = Timer(1)

def blink_led1(timer):
  led1.value(not led1.value())

def blink_led2(timer):
  led2.value(not led2.value())

led1_timer.init(
  period = 100,
  mode = Timer.PERIODIC,
  callback = lambda timer: micropython.schedule(blink_led1, timer))

led2_timer.init(
  period = 1000,
  mode = Timer.PERIODIC,
  callback = lambda timer: micropython.schedule(blink_led2, timer))

sleep(10)

led1_timer.deinit()
led2_timer.deinit()
