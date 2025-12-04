"""
picoweb - WiFi connectivity and web interface module for elevator control
FIXED VERSION with non-blocking socket
"""
import network
import socket
import time

# Module state variables
wlan = None
server_socket = None
is_connected = False
ip_address = None
AUTOREFRESH = 2 # seconds

# Configuration
SSID = 'ITEK 1st'
PASSWORD = 'itekf25v'
PORT = 80

# Callback function - will be set by main.py
command_callback = {}

def init_wifi(ssid=None, password=None):
    """
    Initialize and connect to WiFi
    Returns: True if connected, False otherwise
    """
    global wlan, is_connected, ip_address, SSID, PASSWORD
    
    if ssid:
        SSID = ssid
    if password:
        PASSWORD = password
    
    print('[WiFi] Initializing...')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print(f'[WiFi] Connecting to {SSID}...')
        wlan.connect(SSID, PASSWORD)
        
        # Wait for connection (10 second timeout)
        max_wait = 10
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            max_wait -= 1
            print('[WiFi] Waiting for connection...')
            time.sleep(1)
    
    # Check connection status
    if wlan.status() != 3:
        print('[WiFi] Connection failed!')
        is_connected = False
        return False
    else:
        is_connected = True
        status = wlan.ifconfig()
        ip_address = status[0]
        print(f'[WiFi] Connected! IP: {ip_address}')
        return True

def get_ip_address():
    """Returns the current IP address or None if not connected"""
    return ip_address

def is_wifi_connected():
    """Check if WiFi is currently connected"""
    return is_connected and wlan and wlan.isconnected()

def set_command_callback(callback):
    """
    Set the callback function to handle elevator commands
    Callback should accept (command, *values) parameters
    Example: callback('goto_floor_3', function, 3) or callback('stop', None)
    """
    global command_callback
    name, fn, *values = callback
    command_callback.update({name: (fn, values)})
    print(f'[Web Server] Command callback registered: {name}')

def get_command_callback(name):
    """Execute a registered callback by name"""
    callback = command_callback.get(name)
    if callback:
        return callback[0](*callback[1])
    else:
        print(f'[Web Server] Warning: No callback registered for {name}')

def generate_webpage(current_floor="Unknown", status="Ready"):
    """Generate the HTML page with current elevator state"""
    # Dynamic refresh: faster when moving, slower when idle
    refresh_rate = 1 if "Moving" in status else AUTOREFRESH
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Elevator Control</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="refresh" content="{refresh_rate}">
    <style>
        body {{
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 400px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        h1 {{
            color: #333;
            margin-bottom: 10px;
        }}
        .status {{
            font-size: 18px;
            color: #666;
            margin-bottom: 15px;
            padding: 10px;
            background: #f0f0f0;
            border-radius: 8px;
        }}
        .floor-info {{
            font-size: 16px;
            color: #888;
            margin-bottom: 30px;
            padding: 8px;
            background: #fafafa;
            border-radius: 8px;
        }}
        .floor-buttons {{
            display: flex;
            flex-direction: column;
            gap: 15px;
            margin-top: 20px;
        }}
        button {{
            padding: 25px;
            font-size: 24px;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
            color: white;
        }}
        button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }}
        button:active {{
            transform: translateY(0);
        }}
        .floor-1 {{ background: #f39c12; }}
        .floor-2 {{ background: #e74c3c; }}
        .floor-3 {{ background: #3498db; }}
        .floor-4 {{ background: #2ecc71; }}
        .emergency {{
            margin-top: 20px;
            background: #c0392b;
            padding: 15px;
            font-size: 18px;
        }}
        .footer {{
            margin-top: 20px;
            font-size: 12px;
            color: #999;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Elevator Control</h1>
        <div class="status">Status: <strong>{status}</strong></div>
        <div class="floor-info">Current Floor: <strong>{current_floor}</strong></div>
        
        <div class="floor-buttons">
            <button class="floor-1" onclick="location.href='/?floor=1'">Floor 1</button>
            <button class="floor-2" onclick="location.href='/?floor=2'">Floor 2</button>
            <button class="floor-3" onclick="location.href='/?floor=3'">Floor 3</button>
            <button class="floor-4" onclick="location.href='/?floor=4'">Floor 4</button>
        </div>
        
        <button class="emergency" onclick="location.href='/?cmd=stop'">EMERGENCY STOP</button>
        
        <div class="footer">Auto-refresh: {refresh_rate}s | IP: {ip_address}</div>
    </div>
</body>
</html>"""
    return html

def start_server():
    """
    Start the web server socket
    Call this once during initialization
    """
    global server_socket
    
    if not is_wifi_connected():
        print('[Web Server] Cannot start - not connected to WiFi')
        return False
    
    try:
        addr = socket.getaddrinfo('0.0.0.0', PORT)[0][-1]
        server_socket = socket.socket()
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(addr)
        server_socket.listen(1)  # FIXED: Added parameter
        server_socket.setblocking(False)  # CRITICAL FIX: Non-blocking mode
        
        print(f'[Web Server] Listening on {ip_address}:{PORT}')
        print(f'[Web Server] Access at: http://{ip_address}')
        return True
    except Exception as e:
        print(f'[Web Server] Failed to start: {e}')
        return False

def check_requests(current_floor="Unknown", status="Ready"):
    """
    Check for incoming web requests (non-blocking)
    Call this regularly in your main loop
    
    Args:
        current_floor: Current floor number to display
        status: Status message to display (e.g., "Moving", "Ready", "Stopped")
    
    Returns:
        None
    """
    if not server_socket:
        return
    
    cl = None
    try:
        cl, addr = server_socket.accept()
        cl.settimeout(2.0)  # 2 second timeout for slow connections
        
        request = cl.recv(1024)
        request_str = str(request)
        
        # Parse the request
        if '/?floor=1' in request_str and current_floor != 1:
            if command_callback:
                get_command_callback("goto_1")
                print("[Web] Command: Go to floor 1")
        elif '/?floor=2' in request_str and current_floor != 2:
            if command_callback:
                get_command_callback('goto_2')
                print("[Web] Command: Go to floor 2")
        elif '/?floor=3' in request_str and current_floor != 3:
            if command_callback:
                get_command_callback('goto_3')
                print("[Web] Command: Go to floor 3")
        elif '/?floor=4' in request_str and current_floor != 4:
            if command_callback:
                get_command_callback('goto_4')
                print("[Web] Command: Go to floor 4")
        elif '/?cmd=stop' in request_str:
            if command_callback:
                get_command_callback('stop')
                print("[Web] Command: EMERGENCY STOP")
        
        # Generate and send response
        response = generate_webpage(str(current_floor), status)
        cl.send('HTTP/1.1 200 OK\r\n')
        cl.send('Content-Type: text/html; charset=UTF-8\r\n')
        cl.send('Connection: close\r\n\r\n')
        cl.sendall(response)
        
    except OSError as e:
        # No incoming connection (non-blocking) - this is normal and expected
        if e.errno not in [11, 110, 128]:  # EAGAIN, ETIMEDOUT, ENOTCONN
            print(f'[Web Server] OSError: {e}')
    except Exception as e:
        print(f'[Web Server] Unexpected error: {e}')
    finally:
        if cl:
            try:
                cl.close()
            except:
                pass

def get_server_status():
    """
    Returns a dictionary with server status information
    Useful for debugging
    """
    return {
        'wifi_connected': is_wifi_connected(),
        'ip_address': ip_address,
        'server_running': server_socket is not None,
        'registered_callbacks': list(command_callback.keys())
    }

def stop_server():
    """Stop the web server and close socket"""
    global server_socket
    
    if server_socket:
        server_socket.close()
        server_socket = None
        print('[Web Server] Stopped')

def disconnect_wifi():
    """Disconnect from WiFi"""
    global wlan, is_connected, ip_address
    
    if wlan:
        wlan.disconnect()
        wlan.active(False)
        is_connected = False
        ip_address = None
        print('[WiFi] Disconnected')