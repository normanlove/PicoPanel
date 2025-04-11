import network
import socket
from machine import Pin
import time


PULSE_DURATION = 0.25  
MAX_PULSE = 45.0       
LED_PIN = "LED"        


power_relay = Pin(6, Pin.OUT, value=0)  
reset_relay = Pin(7, Pin.OUT, value=0)   


SSID = "YOUR_SSID" # <- CHANGE THIS TO YOUR WIFI SSID NAME, IN QUOTES
PASSWORD = "YOUR_WIFI_PASSWORD" # <- CHANGE THIS TO YOUR WIFI PASSWORD, IN QUOTES


html_template = """<!DOCTYPE html>
<html>
<head>
    <title>PicoPanel</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root {{
            --primary: #4361ee;
            --danger: #f72585;
            --success: #4cc9f0;
            --dark: #2b2d42;
            --light: #f8f9fa;
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        body {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            padding: 2rem;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        header {{
            background: var(--dark);
            color: white;
            padding: 1.5rem;
            text-align: center;
        }}
        
        h1 {{
            font-weight: 300;
            letter-spacing: 1px;
        }}
        
        .panel {{
            padding: 2rem;
            border-bottom: 1px solid #eee;
        }}
        
        .panel-title {{
            color: var(--primary);
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .btn-group {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            margin-bottom: 1.5rem;
        }}
        
        .btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 12px 24px;
            border: none;
            border-radius: 50px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            gap: 8px;
            min-width: 180px;
        }}
        
        .btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .btn:active {{
            transform: translateY(0);
        }}
        
        .btn-power {{
            background: var(--danger);
            color: white;
        }}
        
        .btn-reset {{
            background: var(--primary);
            color: white;
        }}
        
        .btn-save {{
            background: var(--success);
            color: white;
        }}
        
        .form-group {{
            display: flex;
            align-items: center;
            margin-bottom: 1.5rem;
        }}
        
        input[type="number"] {{
            padding: 12px 15px;
            border: 2px solid #ddd;
            border-radius: 50px;
            font-size: 16px;
            transition: all 0.3s;
            width: 100px;
        }}
        
        input[type="number"]:focus {{
            border-color: var(--primary);
            outline: none;
            box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.2);
        }}
        
        .status-card {{
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 10px;
            margin-top: 1.5rem;
        }}
        
        .pulse-display {{
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--primary);
        }}
        
        @media (max-width: 600px) {{
            .btn-group {{
                flex-direction: column;
            }}
            
            .btn {{
                width: 100%;
            }}
        }}
        
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
            100% {{ transform: scale(1); }}
        }}
        
        .pulse {{
            animation: pulse 0.5s ease;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>PicoPanel Control Center</h1>
        </header>
        
        <div class="panel">
            <h2 class="panel-title">Quick Actions</h2>
            
            <div class="btn-group">
                <form action="/power" class="pulse-form">
                    <button type="submit" class="btn btn-power">Power ({0}s)</button>
                </form>
                
                <form action="/reset" class="pulse-form">
                    <button type="submit" class="btn btn-reset">Reset ({0}s)</button>
                </form>
            </div>
        </div>
        
        <div class="panel">
            <h2 class="panel-title">Pulse Settings</h2>
            
            <form action="/set_pulse" method="get">
                <div class="form-group">
                    <input type="number" name="duration" step="0.1" min="0.1" max="{1}" value="{0}" required>
                    <button type="submit" class="btn btn-save">Set Duration</button>
                </div>
            </form>
            
            <div class="status-card">
                Current pulse duration: <span class="pulse-display">{0} seconds</span>
                <div><small>Relay will activate for this duration when triggered</small></div>
            </div>
        </div>
    </div>
    
    <script>
        document.querySelectorAll('.pulse-form').forEach(form => {{
            form.addEventListener('submit', function() {{
                this.querySelector('button').classList.add('pulse');
                setTimeout(() => {{
                    this.querySelector('button').classList.remove('pulse');
                }}, 500);
            }});
        }});
    </script>
</body>
</html>
"""


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Connecting to Wi-Fi...")
while not wlan.isconnected():
    time.sleep(1)
    print(".", end="")

ip_address = wlan.ifconfig()[0]
print("\nConnected to Wi-Fi!")
print(f"Web server IP: http://{ip_address}")

def pulse_led(duration):
    """Visual feedback with onboard LED"""
    led = Pin(LED_PIN, Pin.OUT)
    led.on()
    time.sleep(duration)
    led.off()

def activate_relay(relay, duration):
    """Activate relay for specified duration (active LOW)"""
    relay.value(1)  # Turn relay ON
    pulse_led(duration)
    relay.value(0)  # Turn relay OFF

def handle_request(client):
    global PULSE_DURATION
    request = client.recv(1024).decode()
    
    if "GET /power" in request:
        activate_relay(power_relay, PULSE_DURATION)
    elif "GET /reset" in request:
        activate_relay(reset_relay, PULSE_DURATION)
    elif "GET /set_pulse?" in request:
        try:
            new_duration = float(request.split('duration=')[1].split(' ')[0])
            if 0.1 <= new_duration <= MAX_PULSE:
                PULSE_DURATION = new_duration
        except:
            pass
    
    html = html_template.format(PULSE_DURATION, MAX_PULSE)
    client.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
    client.send(html)
    client.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 80))
server.listen(5)

print(f"Server running! Open http://{ip_address} in your browser.")
try:
    while True:
        client, addr = server.accept()
        handle_request(client)
except KeyboardInterrupt:
    print("\nServer stopped")
    server.close()
