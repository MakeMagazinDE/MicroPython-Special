import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("SSID", "Passwort")
