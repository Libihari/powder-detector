import serial
import struct
import csv
from datetime import datetime
import time

def read_pms5003(port='/dev/ttyUSB0', output_file='powder_data.csv'):
    # CSV header
    header = [
        'timestamp',
        'pm1_0_cf1', 'pm2_5_cf1', 'pm10_cf1',
        'pm1_0_atm', 'pm2_5_atm', 'pm10_atm',
        'particles_0_3um', 'particles_0_5um',
        'particles_1_0um', 'particles_2_5um',
        'label'  # You'll manually add labels later
    ]
    
    # Initialize CSV file
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
    
    # Serial connection
    ser = serial.Serial(port, baudrate=9600, timeout=1)
    print("Logging data... Press Ctrl+C to stop.")
    
    try:
        while True:
            data = ser.read(32)
            if len(data) == 32 and data[0] == 0x42 and data[1] == 0x4D:
                frame = struct.unpack('>16H', data)
                checksum = sum(data[:-2])
                
                if checksum == (frame[-1] << 8) + frame[-2]:
                    # Prepare data row
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    row = [
                        timestamp,
                        frame[2], frame[3], frame[4],  # CF=1
                        frame[5], frame[6], frame[7],  # Atmospheric
                        frame[8], frame[9],           # Particle counts
                        frame[10], frame[11],
                        ''  # Empty label for manual entry
                    ]
                    
                    # Write to CSV
                    with open(output_file, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(row)
                    
                    # Print sample count
                    with open(output_file, 'r') as f:
                        sample_count = sum(1 for _ in f) - 1  # Subtract header
                    print(f"\rSamples collected: {sample_count}", end='')
                    
                else:
                    print("Checksum failed - skipping frame")
            else:
                print("Invalid frame header - resetting connection")
                ser.reset_input_buffer()
                
            time.sleep(1)  # Adjust based on sensor update rate
            
    except KeyboardInterrupt:
        print("\nData collection stopped.")
    finally:
        ser.close()
        sample_count = sum(1 for line in open(output_file)) - 1
        print(f"Data saved to {output_file} (Total samples: {sample_count})")

if __name__ == '__main__':
    read_pms5003()
