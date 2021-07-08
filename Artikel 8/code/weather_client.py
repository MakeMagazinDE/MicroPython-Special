import network, urequests, ujson

SSID = '<SSID EINFÜGEN>'
PASSWORD = '<PASSWORT EINFÜGEN>'
API_KEY = '<API-KEY EINFÜGEN>'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

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

wlan = connect_to_wifi(SSID, PASSWORD)
weather = get_weather('Hannover,de')
print('Temperatur: %s °C' % weather['main']['temp'])
