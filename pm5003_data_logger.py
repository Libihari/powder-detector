import serial
import pandas as pd
from datetime import datetime

# Initialize serial connection to PM5003
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Adjust port if needed
data = []

try:
    print("Logging data... Press Ctrl+C to stop.")
    while True:
        if ser.in_waiting > 0:  # Corrected from 'ser.i'
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            
            # Parse PM data (example format: "PM1.0: 5, PM2.5: 10, PM10: 20")
            if "PM1.0" in line and "PM2.5" in line and "PM10" in line:
                pm1 = float(line.split("PM1.0: ")[1].split(",")[0])
                pm2_5 = float(line.split("PM2.5: ")[1].split(",")[0])
                pm10 = float(line.split("PM10: ")[1])
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                data.append([timestamp, pm1, pm2_5, pm10])
                print(f"{timestamp} | PM1.0: {pm1}, PM2.5: {pm2_5}, PM10: {pm10}")

except KeyboardInterrupt:
    # Save to CSV when stopped
    df = pd.DataFrame(data, columns=["Timestamp", "PM1.0", "PM2.5", "PM10"])
    df.to_csv("powder_data.csv", index=False)
    print(f"\nData saved to powder_data.csv (Total samples: {len(df)})")
finally:
    ser.close()
