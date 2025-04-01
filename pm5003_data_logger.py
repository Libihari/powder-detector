import serial
import struct

def read_pms5003(port='/dev/ttyUSB0'):
    ser = serial.Serial(port, baudrate=9600, timeout=1)
    while True:
        data = ser.read(32)
        if len(data) == 32 and data[0] == 0x42 and data[1] == 0x4D:
            # Unpack all data (16-bit big-endian)
            frame = struct.unpack('>16H', data)
            checksum = sum(data[:-2])  # Sum all bytes except last 2
            
            if checksum == (frame[-1] << 8) + frame[-2]:
                print(f"""
                CF=1 Standard Particles:
                PM1.0: {frame[2]} μg/m³
                PM2.5: {frame[3]} μg/m³
                PM10:  {frame[4]} μg/m³
                
                Atmospheric Environment:
                PM1.0: {frame[5]} μg/m³
                PM2.5: {frame[6]} μg/m³
                PM10:  {frame[7]} μg/m³
                
                Particle Count (0.1L):
                >0.3μm: {frame[8]}
                >0.5μm: {frame[9]}
                >1.0μm: {frame[10]}
                >2.5μm: {frame[11]}
                """)
            else:
                print("Checksum failed!")
        else:
            print("Invalid frame header")

if __name__ == '__main__':
    read_pms5003()
