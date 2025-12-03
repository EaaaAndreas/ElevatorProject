# src/web/main

from .picoweb import *
from time import sleep


def create_server():
    if not is_wifi_connected():
        while not init_wifi():
            sleep(5)
    """set_command_callback(('goto_1', go_to_floor, 1))
    set_command_callback(('goto_2', go_to_floor, 2))
    set_command_callback(('goto_3', go_to_floor, 3))
    set_command_callback(('goto_4', go_to_floor, 4))
    set_command_callback(('stop', motor_stop, ))"""
    try:
        start_server()
    except:
        stop_server()
        disconnect_wifi()