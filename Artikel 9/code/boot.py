from machine import SDCard, Pin

sd = SDCard(
  slot = 2,
  sck = Pin(18),
  mosi = Pin(23),
  miso = Pin(19),
  cs = Pin(5))
uos.mount(sd, '/sd')
