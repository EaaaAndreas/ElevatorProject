# src/motor/movement
from .motor import *
from measurements.main import floor

def get_current_floor():
    """
    Returns the current floor of the elevator (Only if the elevator is parked at a certain floor).
    :return:
    :rtype:
    """
    floors = floor()
    cur_dist = measure()
    for fl, dist in floors.items():
        if abs(cur_dist - dist) <= ACCURACY:
            return fl
    raise ValueError("Could not determine the current floor")

def go_to_floor(fl:int):
    pass
