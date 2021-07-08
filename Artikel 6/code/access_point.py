import usocket as socket
import network

SSID = 'MicroPython-AP'
WEB_PAGE = '<h1>Hello, World!</h1>'

wlan = network.WLAN(network.AP_IF)
wlan.active(True)
wlan.config(essid = SSID, authmode = network.AUTH_OPEN)

while not wlan.active():
  pass

print(wlan.ifconfig())

server = socket.socket()
server.bind(('', 80))
server.listen(5)

while True:
  connection, address = server.accept()
  print('Anfrage von %s' % str(address))
  request = connection.recv(1024)
  print('Anfrage = %s' % str(request))
  connection.send(WEB_PAGE)
  connection.close()
