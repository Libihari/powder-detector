import serial
import pandas as pd

ser = serial.Serial('/dev/ttyUSB0', 9600)  # PM5003 on USB-UART
data = []

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if "PM1.0" in line:
            pm1 = float(line.split(": ")[1].split(",")[0])
            pm2_5 = float(line.split("PM2.5: ")[1].split(",")[0])
            pm10 = float(line.split("PM10: ")[1])
            data.append([pm1, pm2_5, pm10])
            print(f"PM1.0: {pm1}, PM2.5: {pm2_5}, PM10: {pm10}")
except KeyboardInterrupt:
    df = pd.DataFrame(data, columns=["PM1.0", "PM2.5", "PM10"])
    df.to_csv("powder_data.csv", index=False)
    print("Data saved!")
