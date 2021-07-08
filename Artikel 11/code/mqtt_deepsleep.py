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

wlan = connect_to_wifi(SSID, PASSWORD)
client = MQTTClient('sleeptest', MQTT_SERVER)
client.connect()
client.publish('test/lightsleep', str(time.ticks_ms()))
time.sleep(5)
machine.deepsleep(5000)
