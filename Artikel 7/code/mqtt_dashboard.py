import paho.mqtt.client as mqtt
from guizero import App, Text
from emoji import emojize

MQTT_SERVER = '192.168.188.82'
MQTT_PORT = 1883

def on_connect(client, userdata, flags, rc):
  print('Verbunden mit MQTT-Broker %s.' % MQTT_SERVER)
  client.subscribe('schlafzimmer/+')

def on_message(client, userdata, message):
  content = str(message.payload.decode('utf-8'))
  topic = message.topic
  print('Nachricht (%s) in Topic %s.' % (content, topic))
  if topic.endswith('co2'):
    set_co2(float(content))
  elif topic.endswith('temperatur'):
    set_temperature(float(content))
  elif topic.endswith('luftfeuchtigkeit'):
    set_humidity(float(content))

def set_co2(co2):
  if co2 <= 1000:
    co2_value.value = emojize(':slightly_smiling_face:')
  elif co2 <= 2000:
    co2_value.value = emojize(':worried_face:')
  elif co2 <= 5000:
    co2_value.value = emojize(':nauseated_face:')
  else:
    co2_value.value = emojize(':knocked-out_face:')

def set_temperature(temperature):
  if temperature < 19:
    temperature_value.value = emojize(':cold_face:')
  elif temperature < 21:
    temperature_value.value = emojize(':slightly_smiling_face:')
  else:
    temperature_value.value = emojize(':hot_face:')	

def set_humidity(humidity):
  if humidity < 40:
    humidity_value.value = emojize(':desert:')
  elif humidity < 61:
    humidity_value.value = emojize(':OK_hand:')
  else:
    humidity_value.value = emojize(':sweat_droplets:')

app = App(title = 'Sensor-Dashboard')
co2_value = Text(app, size = 48, text = '')
temperature_value = Text(app, size = 48, text = '')
humidity_value = Text(app, size = 48, text = '')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, MQTT_PORT)
client.loop_start()

app.display()
