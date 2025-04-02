import serial
import csv
import struct
from datetime import datetime

def read_pm5003_packet(ser):
    """Read and validate a complete PM5003 packet"""
    while True:
        # Wait for start bytes 0x42 and 0x4D
        if ser.read(1) == b'\x42' and ser.read(1) == b'\x4D':
            # Read remaining 30 bytes
            packet = ser.read(30)
            if len(packet) == 30:
                return packet

def parse_pm5003_data(packet):
    """Parse PM5003 data packet and validate checksum"""
    # Unpack all fields (big-endian unsigned shorts)
    fields = struct.unpack('>15H', packet)
    
    # Calculate checksum (sum of first 14 fields)
    checksum = sum(packet[:28])  # Sum of first 28 bytes (14 fields)
    if checksum != fields[14]:  # Compare with received checksum
        raise ValueError("Checksum mismatch")
    
    return {
        'pm1_0': fields[2],  # PM1.0 standard
        'pm2_5': fields[3],  # PM2.5 standard
        'pm10': fields[4]    # PM10 standard
    }

def main():
    try:
        # Initialize serial connection
        ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)
        print("PM5003 connected. Logging data (Ctrl+C to stop)...")
        
        # Prepare CSV file
        with open('powder_data.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header if file is empty
            if csvfile.tell() == 0:
                writer.writerow(['PM1.0', 'PM2.5', 'PM10', 'Label', 'Timestamp'])
            
            # Main data collection loop
            while True:
                try:
                    packet = read_pm5003_packet(ser)
                    data = parse_pm5003_data(packet)
                    
                    # Get user input for labeling
                    label = input(
                        f"PM1.0={data['pm1_0']}, PM2.5={data['pm2_5']}, PM10={data['pm10']} "
                        "Enter powder label: "
                    )
                    
                    # Write to CSV
                    writer.writerow([
                        data['pm1_0'],
                        data['pm2_5'],
                        data['pm10'],
                        label,
                        datetime.now().isoformat()
                    ])
                    print("✓ Data saved")
                    
                except ValueError as e:
                    print(f"! Bad data: {e}")
                    continue
                    
    except KeyboardInterrupt:
        print("\nData collection stopped.")
    finally:
        if 'ser' in locals():
            ser.close()

if __name__ == "__main__":
    main()
