import time
from machine import Pin
#gy53 = Pin(16, Pin.IN) # Initialize GY-53 I2C pin
from tests.hardware import ToF
gy53 = ToF()

# FLOOR POSITIONS - Adjust these values based on your actual measurements
# Values in mm
FLOOR_POSITIONS = {
    1: 50,    # Floor 1 - bottom (adjust this)
    2: 350,   # Floor 2 (adjust this)
    3: 650,   # Floor 3 (adjust this)
    4: 950    # Floor 4 - top (adjust this)
}

# How close to a floor position counts as "at that floor" (in mm)
FLOOR_TOLERANCE = 30  # ±30mm

def _measure():
    """Internal measurement function"""
    val = gy53.value()
    print("Measurement:", val)
    return val

def measure(readout=False):
    """
    Get current distance from ToF sensor
    Returns: distance in mm
    """
    return _measure()
    # Old blocking code below - keeping in case you need it later
    while gy53.value(): # Wait for the GY-53 to become ready
        pass
    while not gy53.value(): # Read the GY-53 data
        pass
    starttime = time.ticks_us()
    while gy53.value(): # Wait for the GY-53 to finish reading
        pass
    endtime = time.ticks_us()
    if readout:
        print("Time elapsed: ", (endtime - starttime) / 1000, "ms")
        print("Centimeters: ", (endtime - starttime) / 1000 / 1000, "cm")
    cm = endtime - starttime / 1000 / 1000
    return cm

def get_current_floor():
    """
    Determine which floor the elevator is currently at (or closest to)
    Returns: floor number (1-4) or None if position is invalid
    """
    distance = measure()
    
    # Find the closest floor
    closest_floor = None
    closest_distance = float('inf')
    
    for floor, position in FLOOR_POSITIONS.items():
        diff = abs(distance - position)
        if diff < closest_distance:
            closest_distance = diff
            closest_floor = floor
    
    return closest_floor

def is_at_floor(floor_number):
    """
    Check if elevator is currently at a specific floor
    Args:
        floor_number: The floor to check (1-4)
    Returns: True if at that floor (within tolerance), False otherwise
    """
    distance = measure()
    target_position = FLOOR_POSITIONS.get(floor_number)
    
    if target_position is None:
        return False
    
    return abs(distance - target_position) <= FLOOR_TOLERANCE

def get_floor_position(floor_number):
    """
    Get the distance (in mm) for a specific floor
    Args:
        floor_number: The floor number (1-4)
    Returns: distance in mm, or None if invalid floor
    """
    return FLOOR_POSITIONS.get(floor_number)