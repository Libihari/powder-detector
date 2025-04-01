import serial
import struct
import csv
from datetime import datetime

def read_pms5003():
    with serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1) as ser:
        print("Logging data...")
        with open('powder_data.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp','pm1.0','pm2.5','pm10'])
            
            while True:
                data = ser.read(32)
                if len(data) == 32 and data[0] == 0x42 and data[1] == 0x4D:
                    frame = struct.unpack('>16H', data)
                    if sum(data[:-2]) == (frame[-1] << 8) + frame[-2]:
                        writer.writerow([
                            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            frame[2], frame[3], frame[4]
                        ])
                        f.flush()
                        print(f"Sample: PM2.5={frame[3]} μg/m³", end='\r')

if __name__ == '__main__':
    try:
        read_pms5003()
    except KeyboardInterrupt:
        print("\nData collection stopped")
