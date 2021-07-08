import esp32, time
from machine import Pin

SAMPLES = 1000
THRESHOLD = 40

led = Pin(2, Pin.OUT)

def clean_hall_read():
  value = 0;
  for i in range(SAMPLES):
    value += esp32.hall_sensor()
    time.sleep_us(100)
  return value // SAMPLES

while True:
  if abs(clean_hall_read()) > THRESHOLD:
    led.on()
  else:
    led.off()
