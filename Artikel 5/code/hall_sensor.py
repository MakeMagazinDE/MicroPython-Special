import esp32
from time import sleep

while True:
    print(esp32.hall_sensor())
    sleep(0.5)
