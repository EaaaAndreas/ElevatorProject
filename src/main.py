# src/main
import measurements
import measurements as mes
import motor
import utils
import web
from time import sleep_ms
import gc

ACCURACY = 3 # mm

CURRENT_FLOOR = measurements.get_current_floor(ACCURACY)
TARGET_FLOOR = CURRENT_FLOOR
ELEVATOR_STATUS = "Ready"
IS_MOVING = False

def init():
    while True:
        print("Type 'cal' to calibrate elevator")
        sleep_ms(50)
        print("Leave empty to run elevator")
        sleep_ms(50)
        print("Type 'wrp' to setup webrepl")
        inp = input().strip().lower()
        try:
            if inp == "cal":
                calibrate()
            elif inp == "wrp":
                import webrepl_setup
            else:
                run()
        finally:
            motor.motor_stop()
            web.stop_server()
            web.disconnect_wifi()
            print("[Test] Test complete")

def calibrate():
    mes.calibrate()


def run():
    """Main test loop"""
    global CURRENT_FLOOR, TARGET_FLOOR, ELEVATOR_STATUS, IS_MOVING

    print("\n" + "=" * 50)
    print("ELEVATOR TEST MODE - Simulated Hardware")
    print("=" * 50)

    # Initialize WiFi
    if web.init_wifi():
        print(f"[Test] WiFi connected successfully")

        # Register callbacks
        web.register_web_callbacks(ACCURACY)

        # Start web server
        if web.start_server():
            status = web.get_server_status()
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


    # ====== Main Loop ======
    try:
        while True:
            # 1. Read current floor from mock sensor
            sensor_floor = mes.get_current_floor(ACCURACY)
            if sensor_floor != CURRENT_FLOOR:
                CURRENT_FLOOR = sensor_floor
                print(f"[Test] Floor changed: Now at floor {CURRENT_FLOOR} | dist: {mes.measure()}")

            # 2. Check for web requests
            web.check_requests(CURRENT_FLOOR, ELEVATOR_STATUS)

            # 3. Handle simulated movement
            if not IS_MOVING and TARGET_FLOOR != CURRENT_FLOOR:
                # TODO: Jeg har forsøgt at fixe dér, hvor chatten sagde at vi ikke opdaterer ELEVATOR_STATUS. Men ved
                #   ikke om det virker.
                print(f"[Run] Move to floor {TARGET_FLOOR}...")
                motor.go_to_floor(TARGET_FLOOR, ACCURACY)

                # Update status after movement
                IS_MOVING = True
                ELEVATOR_STATUS = "Ready"
                CURRENT_FLOOR = mes.get_current_floor(ACCURACY)
                print(f"[Run] Arrived at floor {CURRENT_FLOOR}")

            elif IS_MOVING and TARGET_FLOOR == CURRENT_FLOOR:
                IS_MOVING = False
                ELEVATOR_STATUS = "Ready"
                print(f"[Run] Already at floor {TARGET_FLOOR}")

            # 4. Update mock display
            utils.update_display(CURRENT_FLOOR)

            # 5. Garbage collection
            gc_counter += 1
            if gc_counter >= 100:
                gc.collect()
                gc_counter = 0

            # 6. Status print
            if loop_counter % 50 == 0:
                print(f"[Status] Floor: {CURRENT_FLOOR} | Target: {TARGET_FLOOR} | Status: {ELEVATOR_STATUS} | Distance: {mes.measure()}")

            loop_counter += 1
            sleep_ms(50)

    except KeyboardInterrupt:
        print("\n[Test] Stopping test...")
print("Running init")
init()