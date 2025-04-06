# PicoPanel
A tool for controlling the physical power and reset buttons of a PC using a Pi Pico and a web interface
PicoPanel - Web-Based PC Control by Norman Love

PicoPanel is a simple script for a Raspberry Pi Pico W (works on pico 2 W also) that will allow the physical control
of your PC's power and reset buttons but from a web based interface instead of using the physical buttons. As long
as the Pico is powered, this will work when your PC is off/cold state. If you have a motherboard that has a setting
to porivde usb power whilst the PC is off then you can power this from your motherboard easily, if not then an
external solution will need to be provided.

Hardware Needed

Raspberry Pi Pico W/Pico2 W (Pico WH/Pico 2 WH recommended so no soldering required)
4x Female DuPoint wires (female both ends, if you're using WH versions of pico or have headers soldered on)
a micro USB > 9-pin USB motherboard cable or 2x extra dupont female wires if powering from header on board instead
or just a micro usb cable to connect to a USB port for power

Hardware Setup

Power Connection
Simple USB Method:

Connect Pico W directly to any available USB 2.0/3.0 port on your PC case - This is the Safest option for beginners

Advanced Power Connection (Motherboard)
For permanent installations (Advanced Users):

Pico W VSYS (Pin 39) → 5V (USB header pin 1 - usually red wire)
Pico W GND (Pin 38) → GND (USB header pin 10 - usually black wire)
Warning: Verify your motherboard USB header pinout before connecting

Ground (GND) Connections
Essential GND pins on Pico W:

Primary GND (Pin 3) → Motherboard POWER- header
Secondary GND (Pin 8) → Motherboard RESET- header 

Control Signal Connections
Copy
Pico W GP0 (Pin 1/GP0)  → Motherboard POWER+ header
Pico W GP1 (Pin 2/GP1)  → Motherboard RESET+ header


Software Installation

Thonny Setup
Install from thonny.org

Configure interpreter:

Tools > Options > Interpreter

Select: MicroPython (Raspberry Pi Pico)

Port: Auto-detected when Pico is connected via USB

Deployment
Open script in Thonny

Set WiFi credentials:

SSID = "YOUR_NETWORK"  # 2.4GHz networks recommended
PASSWORD = "YOUR_PASSWORD"
Save to Pico as main.py for auto-run

Usage
Connect via case USB port (recommended)

Monitor Thonny shell for IP address (e.g., http://192.168.1.100)


