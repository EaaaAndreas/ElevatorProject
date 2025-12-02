try:
  import usocket as socket
except:
  import socket

from machine import Pin, PWM
import network

from time import sleep

import gc
gc.collect()

# Set pins

"""
Jeg har lavet en placeholder, så du kan kalde:
```
from .motor import *
go_to_floor(x) # Flytter elevatoren til "x" etage.
"""

# handles network connection 
ssid = 'ITEK 1st'
password = 'itekf25v'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass
# checks if connected and prints if it is
print('Connection successful')
print(station.ifconfig())

state = "first"

# Html for webpage
def web_page():
    html = """<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css"
     integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
        html {
            font-family: Arial;
            display: inline-block;
            margin: 0px auto;
            text-align: center;
        }

        .button {
            background-color: #ce1b0e;
            border: none;
            color: rgb(255, 255, 255);
            padding: 16px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 24px;
            margin: 4px 6px;
            cursor: pointer;
        }

        .button1 {
            background-color: #d4ff00;
        }

        .button2 {
            background-color: #00ff15;
        }

        .button3 {
            background-color: #1d1c1d;
        }

        .button4 {
        background-color: #ffff40;
        }

    </style>
</head>

<body>
    <h2>Nothing too special!</h2>
    <p>Last used button: <strong>""" + first + """</strong></p>
    <p>
        <i class="fas fa-lightbulb fa-3x" style="color:#c81919;"></i>
        <a href=\"first\"><button class="button">RED LED ON</button></a>
    </p>
    <p>
        <i class="fas fa-lightbulb fa-3x" style="color:#f6ff00;"></i>
        <a href=\"second\"><button class="button button1">YELLOW LED ON</button></a>
    </p>
    <p>
        <i class="fas fa-lightbulb fa-3x" style="color:#00ff15;"></i>
        <a href=\"third\"><button class="button button2">GREEN LED ON</button></a>
    </p>
    <p>
        <i class="fas fa-lightbulb fa-3x" style="color:#00ff15;"></i>
        <a href=\"forth\"><button class="button button2">GREEN LED ON</button></a>
    </p>
    <form>
        <label for="Username" style="margin-right: 48px;">Enter Username:</label><br>
        <input type="text" id="Username" name="Username"><br>
        <label for="Password" style="margin-right: 54px;">Enter Password:</label><br>
        <input type="password" id="Password" name="Password"><br>
        <input type="submit" style="margin-top: 10px; margin-right: 115px;"> 

    </form>
    
    <form>
        <label for="compiler" style="margin-left: 8px;"> Do you have compiler</label>
        <input type="checkbox" id="compiler" name="do you" value="compiler">
    </form>
    
</body>

</html>"""
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

# setting Pins and PWM
V1motor = Pin(24)
V2motor = Pin(25)
V1motor_pwm = PWM(V1motor)
V2motor_pwm = PWM(V2motor)
duty_step = 129

frequency = 5000
V1motor_pwm.freq(frequency)
V2motor_pwm.freq(frequency)


        
        
# functions for movement    
def first_to_second():    
    for duty_cycle in range(0, 21788, duty_step):
            V1motor_pwm.duty_u16(duty_cycle)
            sleep(0.005)
            
def second_to_third():
    for duty_cycle in range(21788, 43557, duty_step):
            V1motor_pwm.duty_u16(duty_cycle)
            sleep(0.005)
            
def third_to_forth():
    for duty_cycle in range(43558, 65336, duty_step):    
            V1motor_pwm.duty_u16(duty_cycle)
            sleep(0.005)
            
def second_to_first():    
    for duty_cycle in range(21788, 0 -duty_step):
            V2motor_pwm.duty_u16(duty_cycle)
            sleep(0.005)
            
def third_to_second():
    for duty_cycle in range(21788, 43557, -duty_step):
            V2motor_pwm.duty_u16(duty_cycle)
            sleep(0.005)
            
def forth_to_third():
    for duty_cycle in range(65336, 43558, -duty_step):    
            V2motor_pwm.duty_u16(duty_cycle)
            sleep(0.005)


# main function for elevator 
while True:
    try:
        conn, addr = s.accept()
        conn.settimeout(3.0)
        print('Received HTTP GET connection request from %s' % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        print('GET Rquest Content = %s' % request)
        first = request.find('/first')
        second = request.find('/second')
        third = request.find('/third')
        forth = request.find('/forth')
        if first == 6:
            too = "first"
            if state != "first":
                where_to(state, too)
                state = "first"

        if second == 6:
            too = "second"
            if state != "second":
                where_to(state, too)
                state = "second"

        if third == 6:
            too = "third"
            if state != "third":
                where_to(state, too)
                state = "third"
            
        if forth == 6:
            too = "forth"
            if state != "forth":
                where_to(state, too)
                state = "forth"

        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    # Closes connection
    except OSError as e:
        conn.close()
        print('Connection closed')
        

###

V1motor = Pin(24)
V2motor = Pin(25)
V1motor_pwm = PWM(V1motor)
V2motor_pwm = PWM(V2motor)
duty_step = 129

frequency = 5000
V1motor_pwm.freq(frequency)
V2motor_pwm.freq(frequency)

try:
    while True:
        for duty_cycle in range(0, 65336, duty_step):
            motor_pwm.duty_u16(duty_cycle)
            sleep(0.005)

        for duty_cycle in range(65336, 0, -duty_step):
            motor_pwm.duty_u16(duty_cycle)
            sleep(0.005)
except KeyboardInterrupt:
    print("Keyboard Interrupt")
    motor_pwm.duty_u16(0)
    print(motor_pwm)
    motor_pwm.deinit()
    
motor = Pin(4)
motor_pwm = PWM(motor)
duty_step = 129
frequency = 5000

motor_pwm.freq(frequency)



V1motor = Pin(24)
V2motor = Pin(25)
V1motor_pwm = PWM(V1motor)
V2motor_pwm = PWM(V2motor)
duty_step = 129

frequency = 5000
V1motor_pwm.freq(frequency)
V2motor_pwm.freq(frequency)

def where_to(state, too):
    if state == "first":
        if too == "second":
            first_to_second()
            state = "second"            
        if too == "third":
            first_to_second()
            second_to_third()
            state = "third"
        if too == "forth":
            first_to_second()
            second_to_third()
            third_to_forth()
            state = "forth"
        return state
    
    elif state == "second":
        if too == "first":
            second_to_first()
            state = "first"
        if too == "third":
            second_to_third()
            state = "third"
        if too == "forth":
            second_to_third()
            second_to_forth()
            state = "forth"
        return state
    
    elif state == "third":
        if too == "first":
            third_to_second()
            second_to_first()
            state = "first"
        if too == "second":
            third_to_second()
            state = "second"
            
        if too == "forth":
            third_to_forth()
            state = "forth"
        return state
    
    elif state == "forth":
        if too == "first":
            forth_to_third()
            third_to_second()
            second_to_first()
            state = "first"
        if too == "second":
            forth_to_third()
            third_to_second()
            state = "second"
        if too == "third":
            forth_to_third()
            state = "third"
        return state
        
    
def first_to_second():    
    for duty_cycle in range(0, 21788, duty_step):
            V1motor_pwm.duty_u16(duty_cycle)
            sleep(0.005)
            
def second_to_third():
    for duty_cycle in range(21788, 43557, duty_step):
            V1motor_pwm.duty_u16(duty_cycle)
            sleep(0.005)
            
def third_to_forth():
    for duty_cycle in range(43558, 65336, duty_step):    
            V1motor_pwm.duty_u16(duty_cycle)
            sleep(0.005)
            
def second_to_first():    
    for duty_cycle in range(21788, 0 -duty_step):
            V2motor_pwm.duty_u16(duty_cycle)
            sleep(0.005)
            
def third_to_second():
    for duty_cycle in range(21788, 43557, -duty_step):
            V2motor_pwm.duty_u16(duty_cycle)
            sleep(0.005)
            
def forth_to_third():
    for duty_cycle in range(65336, 43558, -duty_step):    
            V2motor_pwm.duty_u16(duty_cycle)
            sleep(0.005)

###