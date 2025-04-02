import serial
import csv
import time

# Initialize serial connection
ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)

# CSV file setup
with open('powder_data.csv', 'a', newline='') as csv_file:
    writer = csv.writer(csv_file)
    
    # Write header if file is empty
    if csv_file.tell() == 0:
        writer.writerow(['PM1.0', 'PM2.5', 'PM10', 'Label'])

    try:
        print("Logging data... Press Ctrl+C to stop.")
        while True:
            if ser.in_waiting > 0:  # CORRECTED: Using in_waiting instead of 'i'
                # Read until we get start bytes (0x42 0x4D)
                if ser.read() == b'\x42':
                    if ser.read() == b'\x4D':
                        # Read remaining 30 bytes
                        packet = ser.read(30)
                        
                        # Parse data (big-endian)
                        pm1_0 = (packet[4] << 8) | packet[5]
                        pm2_5 = (packet[6] << 8) | packet[7]
                        pm10 = (packet[8] << 8) | packet[9]
                        
                        # Get label from user
                        label = input(f"Detected PM1.0={pm1_0}, PM2.5={pm2_5}, PM10={pm10}. Enter label: ")
                        
                        # Write to CSV
                        writer.writerow([pm1_0, pm2_5, pm10, label])
                        print(f"Logged: {pm1_0}, {pm2_5}, {pm10}, {label}")

    except KeyboardInterrupt:
        print("\nData collection stopped.")
    finally:
        ser.close()
