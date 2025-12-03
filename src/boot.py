# src/boot.py
from web.picoweb import init_wifi, disconnect_wifi, is_wifi_connected
from time import sleep, sleep_ms
from machine import Pin
import webrepl

# Board led for on status
led = Pin("LED", Pin.OUT, value=1)

#Connect to WiFi
try:
    while not init_wifi():
        led.toggle()
        sleep(5)
except:
    if is_wifi_connected():
        disconnect_wifi()

# Blink LED to indicate ready
for _ in range(5):
    led.on()
    sleep_ms(100)
    led.off()
    sleep_ms(100)

# Start webrepl
try:
    webrepl.start()
    sleep_ms(500)
    led.on()
except:
    pass

