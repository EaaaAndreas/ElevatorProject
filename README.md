[Google Drive](https://drive.google.com/drive/folders/1Uri08akYiCBdeghpYPs9yWkT8C0TnRwp?usp=drive_link)


# Dependencies

# TODOS
- [x] Make a GitHub Repo
- [ ] Lern how to use GitHub
  - Commits
  - Branches


# Requirements
- ToF
- Web server
- H-bro
  - Kan med fordel styres med **PWM**

# Intro
- Der er præsentation fredag, hvor vi skal fortælle hvordan det virker
- Der skal uploades en rapport og 2 diagrammer på Canvas
  - Elektrisk diagram
  - Flowchart
  - Opgaven skal være præcist beskrevet
## Specks for DC-motor
working v 12 <br>
normal v 12 <br>
free run speed at 12 v 130 rpm/ 250rpm <br>
stack torque at 12v 20Kg/8,8Kg <br>
redactor size 23mm  <br>
length 6mm  <br>
shaft 4mm <br>
weight 60g <br>

## H-bro
Der skal meget strøm (og stor energi) til at drive en elektrisk motor. En del mere end de 5mA vores controller kan levere.

## L298 specks

L298N Module Pinout Configuration
|Pin Name|Description
|:---|:---
|IN1 & IN2|Motor A input pins. Used to control the spinning direction of Motor A
|IN3 & IN4|Motor B input pins. Used to control the spinning direction of Motor B
|ENA|Enables PWM signal for Motor A
|ENB|Enables PWM signal for Motor B
|OUT1 & OUT2|Output pins of Motor A
|OUT3 & OUT4|Output pins of Motor B
|12V|12V input from DC power Source
|5V|Supplies power for the switching logic circuitry inside L298N IC
|GND|Ground pin

 

|Features|Specifications
|:---|:---
|Driver Model| L298N 2A
|Driver Chip| Double H Bridge L298N
|Motor Supply Voltage (Maximum)| 46V
|Motor Supply Current (Maximum)| 2A
|Logic Voltage| 5V
|Driver Voltage| 5-35V
|Driver Current|2A
|Logical Current|0-36mA
|Maximum Power (W)| 25W
|Current Sense for each motor
|Heatsink for better performance
|Power-On LED indicator

<img width="750" height="500" alt="image" src="https://github.com/user-attachments/assets/527074fe-625e-4e02-9b99-26912e505805" />

Website with further information: https://components101.com/modules/l293n-motor-driver-module


Vi skal bruge en DC motor, som er gearet til at skrue ned for hastigheden og op for momentet.

|       Variable       |   Værdi    |
|---------------------:|:----------:|
|   Working voltage    |    12V     |
|   Nominal voltage    |    12V     |
| Free-run speed @ 12V | 130/250RPM |
|  Stall Torque @ 12V  |    ...     |
