import json
import os
from motor.tof import measure


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

#def closest_floor(dist) -> int:
#    floors = floor()
#    return floors

def calibrate():
    while True:
        etage = input('Skriv etage nr.: ')
        distance = measure()
        saving(etage, distance)
        print('data saved')
        print('floor you are on')
        for etage, distance in floor().items():
            print(f"{etage}: {distance}")


def get_current_floor(accuracy:int|float) -> int|None:
    """
    Returns the current floor of the elevator (Only if the elevator is parked at a certain floor).
    :return: The floor that the elevator is parked at. None if not within accuracy
    :rtype: int|None
    """
    floors = floor()
    cur_dist = measure()
    for fl, dist in floors.items():
        if abs(cur_dist - dist) <= accuracy:
            return int(fl)
    return None

def what_way_to_go(target_floor: int|str, accuracy: int|float) -> str:
    target_floor = str(target_floor)
    floors = floor()
    if target_floor not in floors:
        raise  KeyError(f'the target floor {target_floor} is not found in data')
    
    cur_dist = measure()
    target_dist = floors[target_floor]
    
    if abs(cur_dist - target_dist <= accuracy):
        return 'already there'
    elif cur_dist < target_dist:
        return 'up'
    else:
        return 'down'


if __name__ == '__main__':
    calibrate()


