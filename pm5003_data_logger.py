import serial
import time

def connect_pm5003():
    while True:
        try:
            ser = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=1)
            print("PM5003 connected!")
            return ser
        except serial.SerialException:
            print("Waiting for PM5003... Retrying in 5s")
            time.sleep(5)

ser = connect_pm5003()

try:
    while True:
        try:
            data = ser.readline()  # Or your binary packet reading logic
            print(data)
        except serial.SerialException:
            print("Disconnected! Reconnecting...")
            ser.close()
            ser = connect_pm5003()
except KeyboardInterrupt:
    ser.close()
