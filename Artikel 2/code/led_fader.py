from guizero import App, Slider, Text
from gpiozero import PWMLED

def slider_changed(slider_value):
    led.value = int(slider_value) / 100.0

led = PWMLED(13)
app = App(title = "LED-Dimmer")
message = Text(app, text = "Der Slider dimmt die LED.")
slider = Slider(app, command = slider_changed)
app.display()
