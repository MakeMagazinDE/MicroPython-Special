import time
from machine import I2C, Pin
from scd30 import SCD30

i2c = I2C(1, scl = Pin(22), sda = Pin(21), freq = 10000)
scd30 = SCD30(i2c, 0x61)

while True:
  # Warten auf Sensor-Daten...
  while scd30.get_status_ready() != 1:
    time.sleep_ms(200)
  print(scd30.read_measurement())
