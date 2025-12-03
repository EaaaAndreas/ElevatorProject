# src/main/sevensegment
from machine import Pin

CURRENT_NUMBER = None

pins = {
    "A": Pin(8, Pin.OUT, value=0),
    "B": Pin(9, Pin.OUT, value=0),
    "C": Pin(10, Pin.OUT, value=0),
    "D": Pin(12, Pin.OUT, value=0),
    "E": Pin(13, Pin.OUT, value=0),
    "F": Pin(15, Pin.OUT, value=0),
    "G": Pin(14, Pin.OUT, value=0),
    "DP": Pin(11, Pin.OUT, value=0)
}

numbers = [
    {"A": 1, "B": 1, "C": 1, "D": 1, "E": 1, "F": 1, "G": 0, "DP": 0},  # 0
    {"A": 0, "B": 1, "C": 1, "D": 0, "E": 0, "F": 0, "G": 0, "DP": 0},  # 1
    {"A": 1, "B": 1, "C": 0, "D": 1, "E": 1, "F": 0, "G": 1, "DP": 0},  # 2
    {"A": 1, "B": 1, "C": 1, "D": 1, "E": 0, "F": 0, "G": 1, "DP": 0},  # 3
    {"A": 0, "B": 1, "C": 1, "D": 0, "E": 0, "F": 1, "G": 1, "DP": 0},  # 4
    {"A": 1, "B": 0, "C": 1, "D": 1, "E": 0, "F": 1, "G": 1, "DP": 0},  # 5
    {"A": 1, "B": 0, "C": 1, "D": 1, "E": 1, "F": 1, "G": 1, "DP": 1},  # 6
    {"A": 1, "B": 1, "C": 1, "D": 0, "E": 0, "F": 0, "G": 0, "DP": 0},  # 7
    {"A": 1, "B": 1, "C": 1, "D": 1, "E": 1, "F": 1, "G": 1, "DP": 0},  # 8
    {"A": 1, "B": 1, "C": 1, "D": 1, "E": 0, "F": 1, "G": 1, "DP": 1}  # 9
]

def show_number(n:int):
    """
    Shows the given number on the seven segment display
    :param n: The number to be displayed. Must be 0 <= n <= 9
    :type n: int
    :return: None
    """
    global CURRENT_NUMBER
    if 0 <= n <= 9:
        CURRENT_NUMBER = n
        for key, value in numbers[n].items():
            pins[key].value(value)
    else:
        raise ValueError("The number must be between 0 and 9")

def clear_display():
    global CURRENT_NUMBER
    CURRENT_NUMBER = None
    for pin in pins.values():
        pin.off()
