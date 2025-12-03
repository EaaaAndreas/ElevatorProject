# src/motor/movement
from .motor import *
from measurements.main import get_current_floor

def go_to_floor(fl:int):
    fl = int(fl) if fl else None
    curr = get_current_floor() # FIXME: get_current_floor() can return none if undetermined. Add functionality to get around this.
                               #    Some heavy quick-test-patching going on here.
    curr = int(curr) if curr else None
    print(curr)
    if curr is None: # TODO: JUST FOR TESTING! Remove before flight
        print("Goint up")
        go_up(fl)
        return
    if fl > curr:
        print("Going up")
        go_down(fl)
    elif fl < curr:
        print("Going down")
        go_up(fl)
