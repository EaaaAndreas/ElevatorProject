from machine import Pin, PWM
from time import sleep
from .tof import messure

UP = 1 # These decide the direction of the motor. Swap them to go the other way.
DOWN = 2

ACCURACY = 3 # mm - How precise the elevator has to be when parking

motorUp = Pin(18, Pin.OUT)
motorDown = Pin(19, Pin.OUT)
motor_PWM = PWM(Pin(20))
motor_PWM.freq(5000)
duty_step = 10889.33

def motor_forward(speed) -> None:
    """
        Sets the speed of the motor in the forward direction.
        :param speed: The PWM duty cycle determining the speed of the motor
        :type speed: int
        :return: None
    """
    motorUp.on()
    motorDown.off()
    motor_PWM.duty_u16(speed)
    
    
def motor_backward(speed) -> None:
    """
        Sets the speed of the motor in the reverse direction.
        :param speed: The PWM duty cycle determining the speed of the motor
        :type speed: int
        :return: None
    """
    motorUp.off()
    motorDown.on()
    motor_PWM.duty_u16(speed)


def motor_stop() -> None:
    """
    Stops the motor
    :return: None
    """
    motorUp.off()
    motorDown.off()
    motor_PWM.duty_u16(0)


def moveTo(destination) -> None:
    """
    Moves the elevator to the specified distance
    :param destination: The defined
    :type destination:
    :return:
    :rtype:
    """
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
    
def go_up(destination:int, where_i_am:float) -> None:
    """
    Makes the elevator go UP to a specified floor
    :param destination: Where the elevator needs to go
    :type destination: int
    :param where_i_am: Where the elevator currently is (readout from ToF sensor)
    :type where_i_am: float
    :param v: ???
    :type v: int
    :return: None
    """
    speed = 0
    while where_i_am < destination + accuracy:
        speed = rampUp(speed, 1)
        where_i_am = messure()
        
    while where_i_am < destination:                
        speed = rampDown(speed, 2)
        where_i_am = messure()    

def goingDown(destination:int, where_i_am:float, v:int) -> None:
    speed = 0
    while where_i_am > destination - accuracy:
        speed = rampUp(speed, v)
        where_i_am = messure()
    while where_i_am > destination:    
        speed = rampDown(speed, v)
        where_i_am = messure()

