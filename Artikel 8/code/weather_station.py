import network, urequests, ujson, time
from color_setup import ssd
from gui.core.nanogui import refresh
from gui.widgets.label import Label
from gui.widgets.textbox import Textbox
from gui.core.writer import CWriter
import gui.fonts.arial10
from gui.core.colors import *

SSID = '<SSID EINFÜGEN>'
PASSWORD = '<PASSWORT EINFÜGEN>'
API_KEY = '<API-KEY EINFÜGEN>'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'
LOCATION = 'Hannover,de'

def connect_to_wifi(ssid, password):
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.connect(ssid, password)

  while not wlan.isconnected():
    pass
  return wlan

def get_weather(location):
  url = BASE_URL + '?q=' + location + '&'
  url += 'units=metric&lang=de&APPID=' + API_KEY

  response = urequests.get(url)
  return ujson.loads(response.text)

def translate_umlauts(s):
  result = s.replace('ä', 'ae')
  result = result.replace('Ä', 'Ae')
  result = result.replace('ö', 'oe')
  result = result.replace('Ö', 'Oe')
  result = result.replace('ü', 'ue')
  result = result.replace('Ü', 'Ue')
  result = result.replace('ß', 'ss')
  return result
  
def display_weather(weather):
  description = translate_umlauts(weather['weather'][0]['description'])
  lb_location.value(LOCATION)
  tb_description.clear()
  tb_description.append(description)
  lb_temperature.value('Temperatur: %s C' % weather['main']['temp'])
  lb_humidity.value('Luftfeuchtigkeit: %s %%' % weather['main']['humidity'])
  lb_pressure.value('Luftdruck: %s hPa' % weather['main']['pressure'])
  refresh(ssd)
  
wlan = connect_to_wifi(SSID, PASSWORD)

CWriter.set_textpos(ssd, 0, 0)
writer = CWriter(ssd, gui.fonts.arial10, GREEN, BLACK, verbose = False)
writer.set_clip(True, True, False)
lb_location = Label(writer, 2, 2, 124, bdcolor = YELLOW)
tb_description = Textbox(writer, 20, 2, 124, 5, clip = False)
lb_temperature = Label(writer, 76, 0, 124)
lb_humidity = Label(writer, 88, 0, 124)
lb_pressure = Label(writer, 100, 0, 124)
refresh(ssd, True)

while True:
  weather = get_weather(LOCATION)
  display_weather(weather)
  time.sleep(10)
