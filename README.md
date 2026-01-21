# Smart Air Quality Monitoring System

This project implements a real-time air quality monitoring dashboard that displays data from an Arduino-based sensor via a web interface.

## Components

- **Arduino Firmware**: Reads MQ-135 sensor data and transmits it over serial.
- **Python Backend**: Uses PySerial to read serial data and serves it via Flask web server.
- **Web Dashboard**: HTML/CSS/JavaScript frontend that displays live air quality data.

## Setup

1. **Arduino Setup**:
   - Upload the provided Arduino code to your Arduino UNO/Nano.
   - Connect MQ-135 sensor to A0, LEDs to pins 4,5,6, buzzer to 7, LCD to I2C.
   - Note the COM port (e.g., COM3 on Windows).

2. **Python Backend**:
   - Ensure Python 3.7+ is installed.
   - Install dependencies: `pip install pyserial flask`
   - Update `SERIAL_PORT` in `backend.py` to match your Arduino's COM port.
   - Run: `python backend.py`

3. **Dashboard**:
   - Open a browser and go to `http://127.0.0.1:5000`
   - The dashboard will display sensor value and AQI status, updating every 2 seconds.

## Usage

- Connect the Arduino to your computer via USB.
- Run the backend server.
- Open the dashboard in your browser.
- Monitor air quality in real-time.

## Notes

- If the serial port is not available, the dashboard will show "Disconnected".
- AQI statuses: GOOD (green), MODERATE (yellow), POOR (red).