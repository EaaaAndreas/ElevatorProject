# src/motor/movement
from .motor import *
from measurements.main import what_way_to_go
def go_to_floor(fl:int):
    """
    Makes the elevator move to the specified floor
    :param fl: The floor you want to go to
    :type fl: int
    :return: None
    """
    fl = int(fl) if fl else None
    directions = what_way_to_go(fl)
    if directions == 'already there':
        print(f'the elevator is all ready at {fl}')

    if directions == "up":
        print("Going up")
        go_down(fl)
    elif directions == "down":
        print("Going down")
        go_up(fl)
