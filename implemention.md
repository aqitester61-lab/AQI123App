Smart Air Quality Monitoring System
Serial-to-Dashboard Integration (Technical Design Document)
1. Project Overview

This phase of the Smart Air Quality Monitoring System focuses on developing a real-time dashboard that displays air quality data received from an Arduino-based monitoring unit through USB serial communication.

The hardware system is already integrated and operational, consisting of an Arduino UNO / Nano, MQ-135 air quality sensor, LED indicators, and a buzzer. The Arduino continuously reads sensor values, classifies air quality, and transmits the results over the serial interface.

A Python backend application reads the serial data using PySerial and serves the processed data to a frontend dashboard built using HTML and CSS, allowing users to monitor air quality in real time via a browser interface.

2. System Architecture
2.1 High-Level Data Flow
MQ-135 Gas Sensor
        ↓
Arduino UNO / Nano
        ↓ (USB Serial Communication)
Python Backend (PySerial)
        ↓ (Local Web Server)
HTML / CSS Dashboard (Browser)

3. Hardware Configuration (Already Integrated)
3.1 Hardware Components
Component	Description
Arduino UNO / Nano	Reads sensor data and controls alerts
MQ-135 Gas Sensor	Detects overall air pollution and smoke
LEDs (Green, Yellow, Red)	Local air quality indication
Buzzer	Audible alert for poor air quality
USB Cable	Power and serial data transfer
PC / Laptop	Runs backend and dashboard
4. Arduino Serial Data Output
4.1 Data Format

The Arduino transmits air quality data through the serial interface in a structured, comma-separated format to ensure reliable parsing by the backend.

<sensor_value>,<aqi_status>

4.2 Example Output
112,GOOD
178,MODERATE
289,POOR


This format is:

Simple and lightweight

Human readable

Easy to parse in Python

5. Backend Software Design (Python)
5.1 Backend Responsibilities

Establish serial communication with Arduino

Continuously read incoming sensor data

Validate and parse serial messages

Maintain the latest air quality state

Serve data to the frontend via HTTP endpoints

5.2 Serial Communication Configuration
Parameter	Value
Port	COMx (Windows) / /dev/ttyUSB0 (Linux)
Baud Rate	9600
Data Bits	8
Stop Bits	1
Parity	None
5.3 Backend Data Processing Flow

Open serial port using PySerial

Read serial data line by line

Decode and clean incoming text

Split data using comma delimiter

Store latest sensor value and AQI status

Make data available to frontend

6. Frontend Dashboard Design (HTML / CSS)
6.1 Frontend Responsibilities

Display live air quality readings

Show AQI status clearly

Use color-coded indicators for AQI levels

Auto-refresh data at regular intervals

6.2 UI Elements
Element	Description
Sensor Value Display	Shows current MQ-135 reading
AQI Status Text	Displays GOOD / MODERATE / POOR
Color Indicator	Green, Yellow, Red based on AQI
Connection Status	Shows backend availability
6.3 Color Mapping
AQI Status	UI Color
GOOD	Green
MODERATE	Yellow
POOR	Red
7. Frontend–Backend Communication

The frontend fetches live data from the backend using HTTP requests (AJAX / Fetch API).

Example JSON Response from Backend
{
  "sensor_value": 178,
  "aqi_status": "MODERATE"
}

8. Data Update Mechanism

Frontend polls backend at fixed intervals (e.g., every 2 seconds)

Backend returns the latest available AQI data

Dashboard updates values and colors dynamically without page reload

9. Error Handling & Reliability
Scenario	Handling
Serial data not received	Retain last valid reading
Invalid serial format	Ignore and continue
Backend not reachable	Display “Disconnected” on UI
Arduino unplugged	Backend flags serial error
10. Implementation Readiness

The system is ready for implementation with:

Hardware fully integrated

Arduino firmware already operational

Clear serial data format defined

Backend and frontend responsibilities clearly separated

The engineering team can proceed directly with:

Python serial reader implementation

Local web server setup

HTML/CSS dashboard development

11. Conclusion

This document defines the current implementation plan for visualizing Arduino-based air quality data on a browser-based dashboard using HTML and CSS, with Python acting as the serial data bridge.

The design is simple, reliable, and well-suited for real-time monitoring in educational and demonstration environments, ensuring clear visibility of air quality conditions without introducing unnecessary complexity.

The arduino code:  

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

// Pin definitions
#define MQ135_PIN A0
#define GREEN_LED 4
#define YELLOW_LED 5
#define RED_LED 6
#define BUZZER 7

// Timer variables
unsigned long previousMillis = 0;
const unsigned long interval = 5000; // 5 seconds
bool toggleText = false;

void setup() {
  Serial.begin(9600);

  pinMode(GREEN_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  lcd.init();
  lcd.backlight();

  lcd.setCursor(0, 0);
  lcd.print("Air Quality");
  lcd.setCursor(0, 1);
  lcd.print("Monitoring");

  Serial.println("Smart Air Quality Monitoring System");
  Serial.println("MQ-135 warming up...");
  delay(3000);
}

void loop() {
  int gasValue = analogRead(MQ135_PIN);
  unsigned long currentMillis = millis();

  // Reset outputs
  digitalWrite(GREEN_LED, LOW);
  digitalWrite(YELLOW_LED, LOW);
  digitalWrite(RED_LED, LOW);
  digitalWrite(BUZZER, LOW);

  if (gasValue < 200) {
    // GOOD
    digitalWrite(GREEN_LED, HIGH);

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("AQI: SATISFACTORY");
    lcd.setCursor(0, 1);
    lcd.print("Air is Clean");

    Serial.print(gasValue);
    Serial.print(",");
    Serial.println("GOOD");
  }
  else if (gasValue <= 250) {
    // MODERATE
    digitalWrite(YELLOW_LED, HIGH);

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("AQI: MODERATE");
    lcd.setCursor(0, 1);
    lcd.print("Be Cautious");

    Serial.print(gasValue);
    Serial.print(",");
    Serial.println("MODERATE");
  }
  else {
    // POOR
    digitalWrite(RED_LED, HIGH);
    digitalWrite(BUZZER, HIGH);

    Serial.print(gasValue);
    Serial.print(",");
    Serial.println("POOR");

    if (currentMillis - previousMillis >= interval) {
      previousMillis = currentMillis;
      toggleText = !toggleText;
      lcd.clear();
    }

    if (toggleText) {
      lcd.setCursor(0, 0);
      lcd.print("AQI: POOR");
      lcd.setCursor(0, 1);
      lcd.print("High Pollution");
    } else {
      lcd.setCursor(0, 0);
      lcd.print("Please Turn Off");
      lcd.setCursor(0, 1);
      lcd.print("Your Vehicle");
    }
  }

  delay(500);
}

