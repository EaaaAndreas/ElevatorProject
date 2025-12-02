# src/motor/movement
from .motor import *
from meserments.main import floors

def get_current_floor():
    """
    Returns the current floor of the elevator (Only if the elevator is parked at a certain floor).
    :return:
    :rtype:
    """
    stops = floors()
    cur_dist = measure()
    for floor, dist in stops.items():
        if abs(cur_dist - dist) <= ACCURACY:
            return floor
    raise ValueError("Could not determine the current floor")

def go_to_floor(floor:int):
    pass
