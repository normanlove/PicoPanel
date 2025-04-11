# PicoPanel
A tool for controlling the physical power and reset buttons of a PC using a Pi Pico and a web interface
PicoPanel - Web-Based PC Control by Norman Love

PicoPanel is a simple script for a Raspberry Pi Pico W (works on pico 2 W also) that will allow the physical control
of your PC's power and reset buttons but from a web based interface instead of using the physical buttons. As long
as the Pico is powered, this will work when your PC is off/cold state. If you have a motherboard that has a setting
to porivde usb power whilst the PC is off then you can power this from your motherboard easily, if not then an
external solution will need to be provided.

You can view a short video of PicoPanel operating here - https://www.youtube.com/shorts/cYf7eWVLETs

Hardware Needed

Raspberry Pi Pico WH/Pico2 WH - https://thepihut.com/products/raspberry-pi-pico-w?srsltid=AfmBOopHFCOey5r9MEC8z6exq6pL8QwCFH5AHIJgByZxxQt8hs8o0ljc&variant=41952994787523

sb components 3.3v relay HAT for pico - https://shop.sb-components.co.uk/collections/pico-hats/products/pico-3v-relay-hat

micro usb cable/power source

4x DuPont Male/Female (but just female will do if you want to cut the wires. - https://amzn.eu/d/3m8cm1M

Hardware Setup

Simply plug the relay HAT into the pico W, pay attention tot he underside nof the relay hat for the correct orientation. Then, connect the male side of the dupont wires
to the NO and CON terminals on each end of the pi (NO = negative, CON = positive). Then, connec tthe other side of these wires (the female side) to the power and reset 
front panel connectors on your motherboard. the relay on the same side as the usb connector is for the power switch, the opposite for the reset. all done!

Software Installation

Thonny Setup
Install from thonny.org

Configure interpreter:

Tools > Options > Interpreter

Select: MicroPython (Raspberry Pi Pico)

Port: Auto-detected when Pico is connected via USB

Deployment

Open script in Thonny, add your SSID and wifi passsword into the code below (it should appear at the top)

Set WiFi credentials:

SSID = "YOUR_NETWORK" 
PASSWORD = "YOUR_PASSWORD"
Save to Pico as main.py for auto-run

it is recommended you un the script through thonny first to check it works, as it will also output the IP address you will use to access your web interface.

Usage

Make sure the pico is connected to a power source that is on constantly. you can usually set your motherboard BIOS to provide usb power even in an OFF state. This
way you can just power the pico from the PC itself.

Once on and connected. Connect to the IP address that was displayed in the thonny console on your web browser and you will be able to control your power and reset buttons
from your device! simply just hit whichever button you wish to activate. If you wish to change how long you press the button for, for example incase of a hard crash you need
to long press the power button to switch off, simple change the pulse duration of the button press in the prompt below and this will change how long the button of choice is
pressed for, up to a maximum of 45 seconds.


Feel free to mess around with the code and change stuff to your liking. This was a learning to code project for me so there could be things done incorrectly or inefficiently.
Feel free to change the default pulse time of the button presses to what is most commonly useful for your situation or increase/reduce the maximum pulse time if needed.

IT IS HIGHLY RECOMMENDED YOU DO NOT EXPOSE THIS WEB INTERFACE TO THE OPEN INTERNET. there is no security system preventing anyone from using the webpage so anyone with access to the
page itself will be able to control your PC power buttons. if you wish for this to be used on the open internet, please add some redimentary security (such as a password)
system first for obvious reasons. Or, alternatively wait until i learn how to do it myself and add it in a future version.


