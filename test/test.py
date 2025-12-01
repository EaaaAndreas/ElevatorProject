from machine import Pin, PWM
from time import sleep

led = Pin("LED", Pin.OUT)
in1 = Pin(18, Pin.OUT)
in2 = Pin(19, Pin.OUT)

def motor_forward():
    in1.on()
    in2.off()
    
def motor_backward():
    in1.off()
    in2.on()
    
def motor_stop():
    in1.off()
    in2.off()

try:    
    while True:
        led.on()
        print("moving forward")
        motor_forward()
        sleep(1)
        print("moving backwards")
        motor_backward()
        sleep(1)
        print("stopping")
        motor_stop()
        led.off()
        sleep(1)
except KeyboardInterrupt:
    motor_stop()
    print("stopping")
    
