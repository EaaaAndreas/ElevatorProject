# src/motor/movement
from .motor import *
from measurements.main import what_way_to_go

def go_to_floor(fl:int, accuracy:int|float):
    """
    Makes the elevator move to the specified floor
    :param fl: The floor you want to go to
    :type fl: int
    :param accuracy: The accuracy, that the floor position is measured with.
    :type accuracy: int|float
    :return: None
    """
    fl = int(fl) if fl else None
    print("[Motor.Move] Going to floor", fl)
    directions = what_way_to_go(fl, accuracy)
    if directions == 'already there':
        print(f'the elevator is all ready at {fl}')

    if directions == "up":
        print("Going up")
        go_up(fl)
    elif directions == "down":
        print("Going down")
        go_down(fl)
