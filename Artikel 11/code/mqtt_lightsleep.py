import network, machine, time
from umqtt.simple import MQTTClient

SSID = '<SSID EINFÜGEN>'
PASSWORD = '<PASSWORT EINFÜGEN>'
MQTT_SERVER = '<IP-ADRESSE MQTT-BROKER EINFÜGEN>'

def connect_to_wifi(ssid, password):
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.connect(ssid, password)

  while not wlan.isconnected():
    pass
  return wlan

while True:
  try:
    gc.collect()
    wlan = connect_to_wifi(SSID, PASSWORD)
    if wlan.isconnected():
      client = MQTTClient('sleeptest', MQTT_SERVER)
      client.connect()
      client.publish('test/lightsleep', str(time.ticks_ms()))
      time.sleep(1)
    machine.lightsleep(5000)
  except (Exception) as e:
    print('Exception: {} {}'.format(type(e).__name__, e))
