import random
import json
import os

def messure() -> int:
    return random.randint(0, 10000)

def saving(etage, distance):
    if os.path.exists("./data.json"):
        with open('data.json', "r") as file:
            data = json.load(file)
    else:
        data = {}
    data.update({etage: distance})

    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

def floor():
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print("No data.json file found yet.")

def get_floor(etage) -> int:
    distance = ...
    # raise error when no data.json file
    return distance

def main():
    while True:
        etage = input('Etage du vil på: ')
        distence = messure()
        saving(etage, distence)
        print('data saved')
        print('floor er are on')
        for etage, distance in floor().items():
            print(f"{etage}: {distance}")
        
main()


