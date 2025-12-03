from web import *
from web.picoweb import set_command_callback
from time import sleep_ms
print("Ready")
current_floor = 1

def change_floor(fl:int): # TODO: remove test-function
    global current_floor
    print("Changing to floor", fl)
    current_floor = fl


set_command_callback(("goto_1", change_floor, 1))
set_command_callback(("goto_2", change_floor, 2))
set_command_callback(("goto_3", change_floor, 3))
set_command_callback(("goto_4", change_floor, 4))
set_command_callback(("stop", print, "stopped"))

def main():
    create_server()
    try:
        while True:
            check_requests(current_floor)
    finally:
        stop_server()
        disconnect_wifi()

main()