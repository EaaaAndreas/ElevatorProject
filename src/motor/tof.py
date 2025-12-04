import time
from machine import Pin

gy53 = Pin(16, Pin.IN) # Initialize GY-53 I2C pin


def measure(readout = False):
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
    # To get distance in mm, use (endtime - starttime) / 10
    cm = (endtime - starttime) / 10
    if readout:
        print("Time elapsed: ", cm, "cm")

    return cm


if __name__ == "__main__":
    while True:
        measure(True)
        time.sleep(0.25)
