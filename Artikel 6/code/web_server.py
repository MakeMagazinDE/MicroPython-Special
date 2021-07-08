import picoweb, network, time
import ulogging as logging
from machine import I2C, Pin
from scd30 import SCD30

SSID = "<SSID EINFÜGEN>"
PASSWORD = "<PASSWORT EINFÜGEN>"

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
app = picoweb.WebApp(__name__)

@app.route("/")
def index(req, resp):
  data = { 'co2': get_sensor_data()[0] }
  yield from picoweb.start_response(resp)
  yield from app.render_template(resp, "index.tpl", (data,))

logging.basicConfig(level = logging.INFO)
app.run(debug = True, host = wlan.ifconfig()[0])
