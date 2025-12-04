from machine import Pin, PWM
from time import sleep
from .tof import measure
from utils.sevensegment import update_display

__all__ = ["ACCURACY", "motor_forward", "motor_backward", "motor_stop", "move_to", "ramp_up", "ramp_down", "go_up", "go_down"]

UP = 1 # These decide the direction of the motor. Swap them to go the other way.
DOWN = 2

ACCURACY = 3 # mm - How precise the elevator has to be when parking
SLOW = 100 # How long before the designated floor does the elevator need to stop slowing down

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


def move_to(destination) -> None:
    """
    Moves the elevator to the specified distance
    :param destination: The defined
    :type destination:
    :return:
    :rtype:
    """
    where_i_am = measure()
    if where_i_am < destination:
        go_up(destination)
    elif where_i_am > destination:
        go_down(destination)
    # If we have doors: Make 'else: open doors'
        
        
def ramp_up(speed:int, direction:int) -> int:
    if direction == 1:
        if speed > 65336:
            sleep(0.005)
            speed += duty_step
    elif direction == 2:
        if speed > 65336:
            sleep(0.005)
            speed += duty_step
    else:
        raise ValueError("direction must be 1 or 2")
    return speed

        
def ramp_down(speed:int, direction:int) -> int:
    """
    Calculates a new PWM duty cycle for ramping down the motors movement
    :param speed: The current PWM duty cycle
    :type speed: int
    :param direction: The direction of the motor
    :type direction: int
    :return: The new PWM value
    :rtype: int
    """
    if direction == 1:
        if speed < 65336:
            sleep(0.005)  
            speed += duty_step
    elif direction == 2:
        if speed < 65336:
            sleep(0.005) 
            speed += duty_step
    else:
        raise ValueError("direction must be 1 or 2")
    return speed # The speed will stay constant if max speed is reached
    
def go_up(destination:int) -> None:
    """
    Makes the elevator go UP to a specified floor
    :param destination: Where the elevator needs to go
    :type destination: int
    :return: None
    """
    speed = 0
    while measure() < destination + ACCURACY:
        # Removed redundant assignment of "where_i_am" variable. Moved directly to 'while' statement.
        speed = ramp_up(speed, UP) # Make the motor move
        update_display()

    while measure() < destination:
        speed = ramp_down(speed, DOWN)
        update_display()

def go_down(destination:int) -> None:
    """
        Makes the elevator go DOWN to a specified floor
        :param destination: Where the elevator needs to go
        :type destination: int
        :return: None
    """
    speed = 0
    while measure() > destination - ACCURACY:
        speed = ramp_up(speed, DOWN)
        update_display()

    while measure() > destination:
        speed = ramp_down(speed, UP)
        update_display()

