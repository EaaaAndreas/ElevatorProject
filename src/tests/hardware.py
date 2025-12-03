# src/tests/hardware

DISTANCE = 10
PWM = 10

class ToF:
    @staticmethod
    def value():
        return DISTANCE

class Motor:
    def __init__(self, tof_test:ToF, direction:int):
        self._tof = tof_test
        if not (direction == 1 or direction == -1):
            raise ValueError("Direction must be '1' or '-1'")
        self._direction = direction
        self.state = "stopped"

    def on(self):
        print("Motor on")
        global DISTANCE
        DISTANCE += self._direction * PWM

    def off(self):
        print("Motor off")
        pass


class MotorPWM:
    @staticmethod
    def duty_u16(d:int):
        global PWM
        print("Setting PWM:", d)
        PWM = d / 500
