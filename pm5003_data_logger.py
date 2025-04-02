import serial
import csv
from datetime import datetime

# Initialize serial connection
ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)

# CSV file setup
csv_file = open('powder_data.csv', 'a', newline='')
writer = csv.writer(csv_file)

try:
    print("Logging data... Press Ctrl+C to stop.")
    while True:
        if ser.in_waiting:  # Corrected from ser.i to ser.in_waiting
            # Read PM5003 data (32-byte packets starting with 0x42)
            packet = ser.read(32)
            
            # Parse data (example structure - adjust for your sensor)
            pm1_0 = int.from_bytes(packet[4:6], byteorder='big')  # PM1.0
            pm2_5 = int.from_bytes(packet[6:8], byteorder='big')  # PM2.5
            pm10 = int.from_bytes(packet[8:10], byteorder='big')  # PM10
            
            # Get label from user
            label = input(f"Enter label for PM1.0={pm1_0}, PM2.5={pm2_5}, PM10={pm10}: ")
            
            # Write to CSV
            writer.writerow([pm1_0, pm2_5, pm10, label])
            print(f"Logged: {pm1_0}, {pm2_5}, {pm10}, {label}")

except KeyboardInterrupt:
    print("\nData collection stopped.")
finally:
    csv_file.close()
    ser.close()
