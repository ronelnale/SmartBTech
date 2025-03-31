SMT.py 

import socketio
import json
import time
from decimal import Decimal
import logging
import serial
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import modbus_tk.exceptions
from gpiozero import LED, Device
from gpiozero.pins.rpigpio import RPiGPIOFactory
import tkinter as tk
from threading import Thread

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set the GPIO pin factory
Device.pin_factory = RPiGPIOFactory()

# Initialize GPIO for relay control
relays = {
    "relay1": {"gpio": 17, "state": True, "led": None, "last_state": None},
    "relay2": {"gpio": 27, "state": True, "led": None, "last_state": None},
    "relay3": {"gpio": 22, "state": True, "led": None, "last_state": None}
}

# Track relay status (whether each relay is on or off)
relay_status = {"relay1": True, "relay2": True, "relay3": True}

# Define the functions for turning the relay on or off
def turn_relay_on(relay):
    try:
        relays[relay]["led"].on()
        logger.info(f"{relay} is turned ON")
    except Exception as e:
        logger.error(f"Error turning {relay} on: {e}")

def turn_relay_off(relay):
    try:
        relays[relay]["led"].off()
        logger.info(f"{relay} is turned OFF")
    except Exception as e:
        logger.error(f"Error turning {relay} off: {e}")

# Now initialize the GPIO for relays and ensure they are ON at the start
try:
    for relay in relays:
        relays[relay]["led"] = LED(relays[relay]["gpio"])
        turn_relay_on(relay)  # Ensure relays are on at the start
except Exception as e:
    logger.error(f"Error initializing GPIO: {e}")

def toggle_relay_state(relay):
    if relays[relay]["state"]:
        turn_relay_off(relay)
        relay_status[relay] = False  # Relay turned off, stop running time
    else:
        turn_relay_on(relay)
        relay_status[relay] = True  # Relay turned on, resume running time
    relays[relay]["state"] = not relays[relay]["state"]

def send_via_websocket(sio, power, voltage, current, energy, watt_seconds, running_time, sensor_id):
    data = {
        "sensorId": sensor_id,
        "power": Decimal(power).quantize(Decimal('0.00')),
        "voltage": Decimal(voltage).quantize(Decimal('0.00')),
        "current": Decimal(current).quantize(Decimal('0.00')),
        "energy": Decimal(energy).quantize(Decimal('0.000')),
        "watt_seconds": Decimal(watt_seconds).quantize(Decimal('0.00')),
        "running_time": running_time
        
       
        
    }
    #myfile = open("test.log","a")
    #myfile.write(str(Decimal(power).quantize(Decimal('0.00'))) + "\n") 
    #myfile.close()
    
    logger.info("Message: %s", data)
    sio.emit('message', json.dumps(data, cls=DecimalEncoder))

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

class Pzem004T:
    def __init__(self, port):
        self.serial = serial.Serial(
            port=port,
            baudrate=9600,
            bytesize=8,
            parity='N',
            stopbits=1,
            xonxoff=0
        )
        self.master = modbus_rtu.RtuMaster(self.serial)
        self.master.set_timeout(2.0)
        self.master.set_verbose(True)

    def pzem_sensor_data_read(self):
        try:
            self.serial.close()
            self.serial.open()
            data = self.master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)
            voltage = data[0] / 10.0  # [V]
            current = (data[1] + (data[2] << 16)) / 1000.0  # [A]
            power = (data[3] + (data[4] << 16)) / 10.0  # [W]
            return voltage, current, power
        except modbus_tk.exceptions.ModbusInvalidResponseError as e:
            logger.error("Pzem Reader Error: %s", e)
            return None, None, None

# Define the websocket host and port
WEBSOCKET_HOST = '192.168.1.61'
WEBSOCKET_PORT = 5000

# Energy and watt-second accumulators
energy_accumulator = {"sensor1": 0.0, "sensor2": 0.0, "sensor3": 0.0}
watt_seconds_accumulator = {"sensor1": 0.0, "sensor2": 0.0, "sensor3": 0.0}
running_time = {"sensor1": 0, "sensor2": 0, "sensor3": 0}  # in seconds

def relay_control():
    sio = socketio.Client()
    sio.connect(f"http://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}")

    # Initialize the three PZEM sensors
    sensors = [
        Pzem004T(port='/dev/ttyUSB0'),
        Pzem004T(port='/dev/ttyUSB1'),
        Pzem004T(port='/dev/ttyUSB2')
    ]

    # Track the time to ensure real-time behavior
    last_time = time.time()

    try:
        while True:
            current_time = time.time()
            elapsed_time = current_time - last_time
            last_time = current_time

            for i, sensor in enumerate(sensors):
                voltage, current, power = sensor.pzem_sensor_data_read()
                if voltage is not None and current is not None and power is not None:
                    sensor_key = f"sensor{i+1}"
                    # Only accumulate running time if the relay is ON
                    if relay_status[f"relay{i+1}"]:
                        energy_accumulator[sensor_key] += (power / 1000) * (elapsed_time / 3600)
                        watt_seconds_accumulator[sensor_key] += power * elapsed_time
                        running_time[sensor_key] += int(elapsed_time)

                    formatted_time = f"{running_time[sensor_key] // 3600}h " \
                                     f"{(running_time[sensor_key] % 3600) // 60}m " \
                                     f"{running_time[sensor_key] % 60}s"

                    send_via_websocket(
                        sio, power, voltage, current,
                        energy_accumulator[sensor_key],
                        watt_seconds_accumulator[sensor_key],
                        formatted_time,
                        sensor_id=i
                    )

            time.sleep(1)
    finally:
        sio.disconnect()

def start_relay_thread():
    thread = Thread(target=relay_control)
    thread.daemon = True
    thread.start()

def create_gui():
    root = tk.Tk()
    root.title("Relay Control")

    frame = tk.Frame(root)
    frame.pack(pady=20, padx=20)

    for relay in relays:
        btn_toggle = tk.Button(frame, text=f"Toggle {relay.capitalize()}", command=lambda r=relay: toggle_relay_state(r))
        btn_toggle.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    start_relay_thread()
    create_gui()
