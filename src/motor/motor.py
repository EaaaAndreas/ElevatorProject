from machine import Pin, PWM
from time import sleep
from .tof import messure

motorUp = Pin(18, Pin.OUT)
motorDown = Pin(19, Pin.OUT)
motor_PWM = PWM(Pin(20))
motor_PWM.freq(5000)
duty_step = 10889.33

first = 0
second = 1
third = 2
forth = 3
accuracy = 0.3


def motor_forward(speed):
    motorUp.on()
    motorDown.off()
    motor_PWM.duty_u16(speed)
    
    
def motor_backward(speed):
    motorUp.off()
    motorDown.on()
    motor_PWM.duty_u16(speed)


def motor_stop():
    motorUp.off()
    motorDown.off()
    motor_PWM.duty_u16(0)


def moveTo(destination):
    where_i_am = messure()
    if where_i_am < destination:
        v = 1
        goingUp(destination, where_i_am, v)
    elif where_i_am > destination:
        v = 2
        goingDown(destination, where_i_am, v)
        
        
def rampUp(speed, v):
    if v == 1:
        if speed > 65336:
            
            sleep(0.005)
            speed += duty_step
            return speed
    if v == 2:
        if speed > 65336:
            
            sleep(0.005)
            speed += duty_step
            return(speed)

        
def rampDown(speed, v):
    if v == 1:      
        if speed < 65336:
            
            sleep(0.005)  
            speed += duty_step
            return speed
    if v == 2:
        if speed < 65336:
            
            sleep(0.005) 
            speed += duty_step
            return speed
    
def goingUp(destination, where_i_am, v):
    speed = 0
    while where_i_am < destination + accuracy:
        speed = rampUp(speed, v)
        where_i_am = messure()
        
    while where_i_am < destination:                
        speed = rampDown(speed, v)
        where_i_am = messure()    

def goingDown(destination, where_i_am, v):
    speed = 0
    while where_i_am > destination - accuracy:
        speed = rampUp(speed, v)
        where_i_am = messure()
    while where_i_am > destination:    
        speed = rampDown(speed, v)
        where_i_am = messure()

