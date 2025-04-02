import serial
import pandas as pd
from datetime import datetime

try:
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    print(f"Connected to {ser.name}")
    data = []
    
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            print(f"Raw data: {line}")  # Debug print
            
            if "PM1.0" in line and "PM2.5" in line and "PM10" in line:
                pm1 = float(line.split("PM1.0: ")[1].split(",")[0])
                pm2_5 = float(line.split("PM2.5: ")[1].split(",")[0])
                pm10 = float(line.split("PM10: ")[1])
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                data.append([timestamp, pm1, pm2_5, pm10])
                print(f"Logged: {timestamp} | PM1.0: {pm1}, PM2.5: {pm2_5}, PM10: {pm10}")

except Exception as e:
    print(f"Error: {e}")
finally:
    if 'ser' in locals():
        ser.close()
    if data:
        df = pd.DataFrame(data, columns=["Timestamp", "PM1.0", "PM2.5", "PM10"])
        df.to_csv("powder_data.csv", index=False)
        print(f"Saved {len(df)} samples to powder_data.csv")
