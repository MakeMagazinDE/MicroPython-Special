import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('SSID', 'PASSWORT')

while not wlan.isconnected():
  pass

print('Verbunden!')
print(wlan.ifconfig())
