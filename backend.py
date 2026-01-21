import serial
import time
import threading
from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='.', static_url_path='')

BAUD_RATE = 9600
ser = None
SERIAL_PORT = None

def find_arduino_port():
    """Auto-detect Arduino on available COM ports"""
    import serial.tools.list_ports
    try:
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if 'Arduino' in port.description or 'CH340' in port.description or 'USB' in port.description:
                return port.device
        # If no Arduino-specific port found, try first available
        if ports:
            return ports[0].device
    except:
        pass
    return None

def open_serial_port():
    global ser, SERIAL_PORT
    try:
        if ser is not None and ser.is_open:
            ser.close()
        
        # Try to find Arduino port automatically
        port = find_arduino_port()
        if port is None:
            # Fallback to trying common ports
            for p in ['COM3', 'COM4', 'COM5', 'COM1', 'COM2']:
                try:
                    test_ser = serial.Serial(p, BAUD_RATE, timeout=0.5)
                    test_ser.close()
                    port = p
                    break
                except:
                    continue
        
        if port is None:
            print("No serial port found. Running in demo mode")
            return False
        
        ser = serial.Serial(port, BAUD_RATE, timeout=1)
        SERIAL_PORT = port
        print(f"Serial port {port} opened successfully")
        return True
    except Exception as e:
        print(f"Error opening serial port: {e}")
        ser = None
        return False

open_serial_port()

latest_data = {'sensor_value': 0, 'aqi_status': 'UNKNOWN'}

def read_serial():
    global ser
    while True:
        try:
            if ser is not None and ser.is_open:
                if ser.in_waiting > 0:
                    try:
                        line = ser.readline().decode('utf-8').strip()
                        # Parse line like "112,GOOD"
                        if ',' in line:
                            parts = line.split(',')
                            if len(parts) == 2:
                                try:
                                    sensor_value = int(parts[0])
                                    status = parts[1].strip()
                                    latest_data['sensor_value'] = sensor_value
                                    latest_data['aqi_status'] = status
                                    print(f"Data received: {sensor_value}, {status}")
                                except ValueError:
                                    pass
                    except UnicodeDecodeError:
                        pass
        except (serial.SerialException, AttributeError) as e:
            if ser is not None and ser.is_open:
                try:
                    ser.close()
                except:
                    pass
            ser = None
            time.sleep(2)
            open_serial_port()
        time.sleep(0.1)

# Start serial reading thread
thread = threading.Thread(target=read_serial, daemon=True)
thread.start()

@app.route('/data')
def get_data():
    if ser is None or not ser.is_open:
        return jsonify({'sensor_value': latest_data['sensor_value'], 'aqi_status': 'DISCONNECTED'})
    return jsonify(latest_data)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/config', methods=['GET'])
def get_config():
    return jsonify({'port': SERIAL_PORT, 'baud_rate': BAUD_RATE, 'connected': ser is not None and ser.is_open})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)