import serial
import csv
import struct
from datetime import datetime

def read_pm_data(ser):
    """Read a complete PM5003 data packet"""
    while True:
        # Wait for start bytes (0x42 0x4D)
        if ser.read(1) == b'\x42':
            if ser.read(1) == b'\x4D':
                # Read remaining 30 bytes
                packet = ser.read(30)
                if len(packet) == 30:
                    return packet

def parse_pm_packet(packet):
    """Parse PM5003 data packet"""
    # Unpack all fields (big-endian unsigned shorts)
    data = struct.unpack('>15H', packet)
    
    # Verify checksum (sum of first 28 bytes)
    checksum = sum(packet[:28])
    if checksum != data[14]:
        raise ValueError("Checksum mismatch")
    
    return {
        'pm1_0': data[2],  # PM1.0 standard
        'pm2_5': data[3],  # PM2.5 standard
        'pm10': data[4]    # PM10 standard
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
                    packet = read_pm_data(ser)
                    pm_data = parse_pm_packet(packet)
                    
                    # Get user input
                    label = input(
                        f"Detected - PM1.0: {pm_data['pm1_0']}, PM2.5: {pm_data['pm2_5']}, PM10: {pm_data['pm10']}\n"
                        "Enter powder label: "
                    )
                    
                    # Write to CSV
                    writer.writerow([
                        pm_data['pm1_0'],
                        pm_data['pm2_5'],
                        pm_data['pm10'],
                        label,
                        datetime.now().isoformat()
                    ])
                    print("✓ Data saved")
                    
                except ValueError as e:
                    print(f"! Error: {e} - Skipping packet")
                    continue
                    
    except serial.SerialException as e:
        print(f"Serial port error: {e}")
    except KeyboardInterrupt:
        print("\nData collection stopped.")
    finally:
        if 'ser' in locals():
            ser.close()

if __name__ == "__main__":
    main()
