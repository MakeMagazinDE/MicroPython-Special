import paho.mqtt.client as mqtt
 
MQTT_SERVER = 'localhost'
MQTT_PORT = 1883
CO2_TOPIC = 'schlafzimmer/co2'
 
def on_connect(client, userdata, flags, rc):
  print('Verbunden mit MQTT-Broker %s.' % MQTT_SERVER)
  client.subscribe(CO2_TOPIC)
 
def on_message(client, userdata, message):
  msg = str(message.payload.decode('utf-8'))
  print('Nachricht (%s) in Topic %s.' % (msg, message.topic))
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, MQTT_PORT)
client.loop_forever()
