import _thread as th
from time import sleep
from machine import Pin

led1 = Pin(18, Pin.OUT)
led2 = Pin(19, Pin.OUT)

thread1_running = True
thread2_running = True

def blink_led1(delay):
  while thread1_running:
    led1.value(not led1.value())
    sleep(delay)

def blink_led2(delay):
  while thread2_running:
    led2.value(not led2.value())
    sleep(delay)

th.start_new_thread(blink_led1, (.1,))
th.start_new_thread(blink_led2, (1,))

sleep(10)

thread1_running = False
thread2_running = False
