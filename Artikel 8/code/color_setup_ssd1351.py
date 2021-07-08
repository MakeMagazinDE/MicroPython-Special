from machine import SPI, Pin
import gc
from drivers.ssd1351.ssd1351_generic import SSD1351 as SSD

HEIGHT = 128

pdc = Pin(27, Pin.OUT, value = 0)
pcs = Pin(25, Pin.OUT, value = 1)
prst = Pin(26, Pin.OUT, value = 1)
spi = SPI(1, 10_000_000, sck = Pin(14), mosi = Pin(13))

gc.collect()

ssd = SSD(spi, pcs, pdc, prst, height = HEIGHT)
