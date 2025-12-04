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


def run_test():
    """Main test loop"""
    global current_floor, target_floor, elevator_status, is_moving

    print("\n" + "=" * 50)
    print("ELEVATOR TEST MODE - Simulated Hardware")
    print("=" * 50)

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

    print("\n" + "=" * 50)
    print("[Test] SYSTEM READY - Test the web interface!")
    print("=" * 50 + "\n")

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
init()