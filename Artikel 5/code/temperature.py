import esp32, time

while True:
  f = esp32.raw_temperature()
  c = (f - 32) / 1.8
  print(c)
  time.sleep(1)
