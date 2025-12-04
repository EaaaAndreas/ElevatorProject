# src/web/main
from .picoweb import *
from motor.movement import *
from time import sleep


def register_web_callbacks(accuracy:int|float):
    set_command_callback(('goto_1', go_to_floor, 1, accuracy))
    set_command_callback(('goto_2', go_to_floor, 2, accuracy))
    set_command_callback(('goto_3', go_to_floor, 3, accuracy))
    set_command_callback(('goto_4', go_to_floor, 4, accuracy))
    set_command_callback(('stop', motor_stop, ))

