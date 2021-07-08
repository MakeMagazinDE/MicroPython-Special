import network, time
from machine import I2C, Pin
from scd30 import SCD30
from umqtt.simple import MQTTClient

SSID = '<SSID EINFÜGEN>'
PASSWORD = '<PASSWORT EINFÜGEN>'
MQTT_SERVER = '<IP-ADRESSE MQTT-BROKER EINFÜGEN>'

def init_scd30():
  i2c = I2C(1, scl = Pin(22), sda = Pin(21), freq = 10000)
  return SCD30(i2c, 0x61)

def get_sensor_data():
  while scd30.get_status_ready() != 1:
    time.sleep_ms(200)
  return scd30.read_measurement()

def connect_to_wifi(ssid, password):
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.connect(ssid, password)

  while not wlan.isconnected():
    pass
  return wlan

scd30 = init_scd30()
wlan = connect_to_wifi(SSID, PASSWORD)

client = MQTTClient('scd30_schlafzimmer', MQTT_SERVER)
client.connect()
while True:
  co2, temperature, humidity = get_sensor_data()
  client.publish('schlafzimmer/co2', str(co2))
  client.publish('schlafzimmer/temperatur', str(temperature))
  client.publish('schlafzimmer/luftfeuchtigkeit', str(humidity))
  time.sleep(10)
