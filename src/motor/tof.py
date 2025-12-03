import time
from machine import Pin



#gy53 = Pin(16, Pin.IN) # Initialize GY-53 I2C pin
from tests.hardware import ToF
gy53 = ToF()

def _measure():
    val = gy53.value()
    print("Measurement:", val)
    return val

def measure(readout = False):
    return _measure()
    while gy53.value(): # Wait for the GY-53 to become ready
        #print("Waiting for GY-53 to become ready...")
        pass
    while not gy53.value(): # Read the GY-53 data
        #print("Reading GY-53 data...")
        pass
    starttime = time.ticks_us()
    while gy53.value(): # Wait for the GY-53 to finish reading
        #print("Waiting for GY-53 to finish reading...")
        pass
    endtime = time.ticks_us()
    if readout:
        print("Time elapsed: ", (endtime - starttime) / 1000, "ms")
        print("Centimeters: ", (endtime - starttime) / 1000 / 1000, "cm")
    cm = endtime - starttime / 1000 / 1000
    return cm



