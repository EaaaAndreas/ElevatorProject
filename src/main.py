# src/main
from time import sleep_ms

from motor import go_to_floor
from web.main import create_server
from web.picoweb import check_requests, stop_server, disconnect_wifi
from utils.sevensegment import update_display

current_floor = 1
def init():
    while True:
        print("Type 'run' to run elevator program")
        sleep_ms(50)
        print("Type 'cal' to calibrate elevator")
        sleep_ms(50)
        print("Type 'wrp' to setup webrepl")
        inp = input().strip().lower()

        if inp == "run":
            return run_elevator()
        elif inp == "cal":
            print("Calibration not implemented yet")
        elif inp == "wrp":
            import webrepl_setup
        else:
            print("Invalid input")

# TODO: Make work with motor
def run_elevator():
    sleep_ms(50)
    print("Updating display")
    update_display()
    print("Starting loop")
    while True:
        print("What floor?")
        inp = int(input().strip())
        if 0 < inp <= 4:
            go_to_floor(inp)
        else:
            print("Floor", inp, "does not exist.")
    """create_server()
    try:
        while True:
            check_requests(current_floor)
    finally:
        stop_server()
        disconnect_wifi()"""


init()