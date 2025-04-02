import serial
import csv
import struct
from datetime import datetime

def read_pm5003_data(ser):
    while True:
        # Wait for start bytes (0x42 0x4D)
        if ser.read(1) == b'\x42':
            if ser.read(1) == b'\x4D':
                # Read remaining 30 bytes
                packet = ser.read(30)
                if len(packet) != 30:
                    continue
                
                # Unpack data (big-endian)
                data = struct.unpack('>HHHHHHHHHHHHHHH', packet)
                
                # Validate checksum (sum of bytes 0-29)
                checksum = (data[-2] << 8) | data[-1]
                calculated = sum(struct.pack('>HHHHHHHHHHHHHH', *data[:-1]))
                if checksum != calculated:
                    print("Checksum error!")
                    continue
                
                # Extract PM values (standard units)
                return {
                    'pm1_0': data[2],
                    'pm2_5': data[3],
                    'pm10': data[4]
                }

def main():
    try:
        ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)
        print("PM5003 connected. Logging data...")
        
        with open('powder_data.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if csvfile.tell() == 0:  # Write header if file is empty
                writer.writerow(['PM1.0', 'PM2.5', 'PM10', 'Label', 'Timestamp'])
            
            while True:
                data = read_pm5003_data(ser)
                label = input(f"PM1.0={data['pm1_0']}, PM2.5={data['pm2_5']}, PM10={data['pm10']} - Enter label: ")
                writer.writerow([
                    data['pm1_0'],
                    data['pm2_5'],
                    data['pm10'],
                    label,
                    datetime.now().isoformat()
                ])
                print("Data saved!")
                
    except KeyboardInterrupt:
        print("\nLogging stopped.")
    finally:
        if 'ser' in locals():
            ser.close()

if __name__ == "__main__":
    main()
