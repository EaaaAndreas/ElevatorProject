# src/main
from time import sleep_ms
from motor import go_to_floor, motor_stop
from motor.tof import get_current_floor
from web.picoweb import (init_wifi, start_server, check_requests, 
                         stop_server, disconnect_wifi, set_command_callback,
                         get_server_status)
from utils.sevensegment import update_display
import gc

# Global state
current_floor = 1
target_floor = 1
elevator_status = "Ready"
is_moving = False

def handle_goto_floor(floor_number):
    """
    Callback for web interface floor commands
    Sets the target floor and initiates movement
    """
    global target_floor, elevator_status, is_moving
    
    print(f"[Main] Request to go to floor {floor_number}")
    target_floor = floor_number
    elevator_status = f"Moving to floor {floor_number}"
    is_moving = True

def handle_emergency_stop():
    """
    Callback for web interface emergency stop
    """
    global elevator_status, is_moving
    
    print("[Main] EMERGENCY STOP activated")
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
    print("[Main] Web callbacks registered")

def init():
    """Initialization menu"""
    while True:
        print("\n" + "="*50)
        print("ELEVATOR CONTROL SYSTEM")
        print("="*50)
        print("Type 'run' to run elevator program")
        print("Type 'cal' to calibrate elevator")
        print("Type 'wrp' to setup webrepl")
        print("="*50)
        
        inp = input("Choose option: ").strip().lower()
        
        if inp == "run":
            return run_elevator()
        elif inp == "cal":
            print("Calibration not implemented yet")
        elif inp == "wrp":
            import webrepl_setup
        else:
            print("Invalid input")

def run_elevator():
    """
    Main elevator control loop with web interface integration
    """
    global current_floor, target_floor, elevator_status, is_moving
    
    print("\n[Main] Initializing elevator system...")
    
    # Initialize WiFi
    if init_wifi():
        print(f"[Main] WiFi connected successfully")
        
        # Register callbacks
        register_web_callbacks()
        
        # Start web server
        if start_server():
            print(f"[Main] Web interface available at: http://{get_server_status()['ip_address']}")
        else:
            print("[Main] Warning: Web server failed to start")
    else:
        print("[Main] Warning: Running without web interface")
    
    # Initialize display
    print("[Main] Initializing display...")
    update_display()
    
    print("\n" + "="*50)
    print("[Main] SYSTEM READY - Entering main loop")
    print("="*50 + "\n")
    
    # Main control loop
    loop_counter = 0
    gc_counter = 0
    
    try:
        while True:
            # 1. Read current floor from ToF sensor
            try:
                sensor_floor = get_current_floor()
                if sensor_floor != current_floor:
                    current_floor = sensor_floor
                    print(f"[Main] Floor changed: Now at floor {current_floor}")
            except Exception as e:
                print(f"[Main] Sensor error: {e}")
            
            # 2. Check for web requests (non-blocking)
            try:
                check_requests(current_floor, elevator_status)
            except Exception as e:
                print(f"[Main] Web server error: {e}")
            
            # 3. Handle elevator movement
            if is_moving and target_floor != current_floor:
                try:
                    print(f"[Main] Moving elevator to floor {target_floor}...")
                    go_to_floor(target_floor)
                    
                    # Update status after movement completes
                    is_moving = False
                    elevator_status = "Ready"
                    current_floor = get_current_floor()
                    print(f"[Main] Arrived at floor {current_floor}")
                    
                except Exception as e:
                    print(f"[Main] Movement error: {e}")
                    motor_stop()
                    is_moving = False
                    elevator_status = "Error"
            
            elif is_moving and target_floor == current_floor:
                # Already at target floor
                is_moving = False
                elevator_status = "Ready"
                print(f"[Main] Already at floor {target_floor}")
            
            # 4. Update display
            try:
                update_display()
            except Exception as e:
                print(f"[Main] Display error: {e}")
            
            # 5. Periodic garbage collection (every ~10 seconds)
            gc_counter += 1
            if gc_counter >= 100:
                gc.collect()
                gc_counter = 0
            
            # 6. Status print every 5 seconds
            if loop_counter % 50 == 0:
                print(f"[Status] Floor: {current_floor} | Target: {target_floor} | Status: {elevator_status}")
            
            loop_counter += 1
            
            # Small delay to prevent CPU hogging
            # Adjust based on responsiveness needs: 50ms = 20 checks/sec
            sleep_ms(50)
            
    except KeyboardInterrupt:
        print("\n[Main] Keyboard interrupt detected - shutting down...")
    except Exception as e:
        print(f"\n[Main] Unexpected error: {e}")
    finally:
        # Cleanup
        print("[Main] Stopping motor...")
        motor_stop()
        
        print("[Main] Stopping web server...")
        stop_server()
        disconnect_wifi()
        
        print("[Main] Shutdown complete")

if __name__ == '__main__':
    init()