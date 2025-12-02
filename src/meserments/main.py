import random
import json 

def messure():
    return random.randint(0, 10000)

def saving(etage, distence):
    data = {
        'etage': etage,
        'distence': distence
    }

    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    
    return

def floor():
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
            for i in data:
                floor = i['etage']
                afstand = i['distence']
            return floor, afstand
    except FileNotFoundError:
        print("No data.json file found yet.")

def main():
    while True:
        etage = input('Etage du vil på: ')
        distence = messure()
        saving(etage, distence)
        print('data saved')
        print('floor er are on')
        info = floor()
        print(info)
        
main()


