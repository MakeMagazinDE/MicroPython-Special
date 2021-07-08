from time import sleep
from machine import Pin, TouchPad

touch0 = TouchPad(Pin(4))

while True:
  print(touch0.read())
  sleep(0.2)
