import random
import json
import os
from motor import *
from motor.tof import measure

ACCURACY = 3
# TODO: We have to add a 'what way to go' function to tell the `go_to_floor` function what to do.
#   The `get_current_floor` function is inadequate if the elevator is not parked at a certain floor.
#   The function has to either completely replace `get_current_floor` or be added to `go_to_floor`, along with a test
#   for if `get_current_floor` returns `None`

def saving(etage, distance):
    if os.path.exists("./measurements/data.json"):
        with open('data.json', "r") as file:
            data = json.load(file)
    else:
        data = {}
    data.update({etage: distance})

    with open('./measurements/data.json', 'w') as f:
        json.dump(data, f)

def floor():
    try:
        with open("./measurements/data.json", "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print("No data.json file found yet.")

def get_floor(etage) -> int:
    try:
        with open('./measurements/data.json', 'r') as file:
            data = json.load(file)

        if etage in data:
            return data[etage]
        else:
            raise KeyError(f"Etage {etage} not found in data.json")

    except FileNotFoundError:
        raise FileNotFoundError("No data.json file found yet.")

def closest_floor(dist) -> int:
    floors = floor()
    return floors

def calibrate():
    while True:
        etage = input('Skriv etage nr.: ')
        distance = measure()
        saving(etage, distance)
        print('data saved')
        print('floor you are on')
        for etage, distance in floor().items():
            print(f"{etage}: {distance}")


def get_current_floor():
    """
    Returns the current floor of the elevator (Only if the elevator is parked at a certain floor).
    :return:
    :rtype:
    """
    print("Getting all floors")
    floors = floor()
    print("Getting distance")
    cur_dist = measure()
    print("Comparing")
    for fl, dist in floors.items():
        if abs(cur_dist - dist) <= ACCURACY:
            return fl
    raise ValueError("Could not determine the current floor")

def what_way_to_go(target_floor: str|int) -> str:
    target_floor = str(target_floor)
    floors = floor()
    if target_floor not in floors:
        raise  KeyError(f'the target floor {target_floor} is not found in data')
    
    cur_disk = measure()
    target_dist = floors[target_floor]
    
    if abs(cur_disk - target_floor <= ACCURACY):
        return 'already there'
    elif cur_disk < target_dist:
        return 'up'
    else:
        return 'down'


if __name__ == '__main__':
    calibrate()


