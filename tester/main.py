"""
test_elevator.py - Test elevator system without actual hardware
Simulates ToF sensor, motor, and display
Run this on your Pico to test the web interface
"""
from time import sleep_ms
import gc

# Mock implementations (replace hardware calls)
class MockToF:
    """Simulates ToF sensor"""
    def __init__(self):
        self.position = 50  # Start at floor 1
        
    def value(self):
        return self.position
    
    def move_to(self, target):
        """Simulate smooth movement"""
        while abs(self.position - target) > 5:
            if self.position < target:
                self.position += 10
            else:
                self.position -= 10
            sleep_ms(100)  # Simulate movement time
        self.position = target

# Global mock sensor
mock_sensor = MockToF()

# Floor positions (same as real tof.py)
FLOOR_POSITIONS = {
    1: 50,
    2: 350,
    3: 650,
    4: 950
}

def measure():
    """Mock measure function"""
    return mock_sensor.value()

def get_current_floor():
    """Determine current floor from mock sensor"""
    distance = measure()
    closest_floor = None
    closest_distance = float('inf')
    
    for floor, position in FLOOR_POSITIONS.items():
        diff = abs(distance - position)
        if diff < closest_distance:
            closest_distance = diff
            closest_floor = floor
    
    return closest_floor

def go_to_floor(floor_number):
    """Mock go_to_floor - simulates movement"""
    destination = FLOOR_POSITIONS.get(floor_number)
    if destination is None:
        print(f"Error: Floor {floor_number} does not exist")
        return
    
    print(f"[MOCK] Moving to floor {floor_number} (position: {destination}mm)")
    mock_sensor.move_to(destination)
    print(f"[MOCK] Arrived at floor {floor_number}")

def motor_stop():
    """Mock motor stop"""
    print("[MOCK] Motor stopped")

def update_display():
    """Mock display update"""
    pass  # Do nothing

# Import web server (the REAL one)
from web.picoweb import (init_wifi, start_server, check_requests, 
                         stop_server, disconnect_wifi, set_command_callback,
                         get_server_status)

# Global state
current_floor = 1
target_floor = 1
elevator_status = "Ready"
is_moving = False

def handle_goto_floor(floor_number):
    """Callback for web interface floor commands"""
    global target_floor, elevator_status, is_moving
    
    print(f"[Test] Request to go to floor {floor_number}")
    target_floor = floor_number
    elevator_status = f"Moving to floor {floor_number}"
    is_moving = True

def handle_emergency_stop():
    """Callback for web interface emergency stop"""
    global elevator_status, is_moving
    
    print("[Test] EMERGENCY STOP activated")
    motor_stop()
    elevator_status = "Emergency Stop"
    is_moving = False

def register_web_callbacks():
    """Register all web interface callbacks"""
    set_command_callback(("goto_1", handle_goto_floor, 1))
    set_command_callback(("goto_2", handle_goto_floor, 2))
    set_command_callback(("goto_3", handle_goto_floor, 3))
    set_command_callback(("goto_4", handle_goto_floor, 4))
    set_command_callback(("stop", handle_emergency_stop))
    print("[Test] Web callbacks registered")

def run_test():
    """Main test loop"""
    global current_floor, target_floor, elevator_status, is_moving
    
    print("\n" + "="*50)
    print("ELEVATOR TEST MODE - Simulated Hardware")
    print("="*50)
    
    # Initialize WiFi
    if init_wifi():
        print(f"[Test] WiFi connected successfully")
        
        # Register callbacks
        register_web_callbacks()
        
        # Start web server
        if start_server():
            status = get_server_status()
            print(f"[Test] Web interface: http://{status['ip_address']}")
            print("[Test] Open this in your browser to test!")
        else:
            print("[Test] Warning: Web server failed to start")
            return
    else:
        print("[Test] Warning: WiFi connection failed")
        return
    
    print("\n" + "="*50)
    print("[Test] SYSTEM READY - Test the web interface!")
    print("="*50 + "\n")
    
    loop_counter = 0
    gc_counter = 0
    
    try:
        while True:
            # 1. Read current floor from mock sensor
            sensor_floor = get_current_floor()
            if sensor_floor != current_floor:
                current_floor = sensor_floor
                print(f"[Test] Floor changed: Now at floor {current_floor}")
            
            # 2. Check for web requests
            check_requests(current_floor, elevator_status)
            
            # 3. Handle simulated movement
            if is_moving and target_floor != current_floor:
                print(f"[Test] Simulating movement to floor {target_floor}...")
                go_to_floor(target_floor)
                
                # Update status after movement
                is_moving = False
                elevator_status = "Ready"
                current_floor = get_current_floor()
                print(f"[Test] Arrived at floor {current_floor}")
                
            elif is_moving and target_floor == current_floor:
                is_moving = False
                elevator_status = "Ready"
                print(f"[Test] Already at floor {target_floor}")
            
            # 4. Update mock display
            update_display()
            
            # 5. Garbage collection
            gc_counter += 1
            if gc_counter >= 100:
                gc.collect()
                gc_counter = 0
            
            # 6. Status print
            if loop_counter % 50 == 0:
                print(f"[Status] Floor: {current_floor} | Target: {target_floor} | Status: {elevator_status}")
            
            loop_counter += 1
            sleep_ms(50)
            
    except KeyboardInterrupt:
        print("\n[Test] Stopping test...")
    finally:
        motor_stop()
        stop_server()
        disconnect_wifi()
        print("[Test] Test complete")

if __name__ == '__main__':
    run_test()