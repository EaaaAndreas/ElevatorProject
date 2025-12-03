import random
import json
import os

def measure() -> int:
    return random.randint(0, 10000)

def saving(etage, distance):
    if os.path.exists("./data.json"):
        with open('data.json', "r") as file:
            data = json.load(file)
    else:
        data = {}
    data.update({etage: distance})

    with open('./data.json', 'w') as f:
        json.dump(data, f)

def floor():
    try:
        with open("./data.json", "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print("No data.json file found yet.")

def get_floor(etage) -> int:
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)

        if etage in data:
            return data[etage]
        else:
            raise KeyError(f"Etage {etage} not found in data.json")

    except FileNotFoundError:
        raise FileNotFoundError("No data.json file found yet.")

    # raise error when no data.json file
    return distance

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
        
if __name__ == '__main__':
    calibrate()


