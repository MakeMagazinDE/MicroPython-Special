import esp32, time

SAMPLES = 1000

while True:
  value = 0;
  for i in range(SAMPLES):
    value += esp32.hall_sensor()
    time.sleep_us(100)
  print(value // SAMPLES)
