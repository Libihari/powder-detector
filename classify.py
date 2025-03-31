import serial
import joblib
import time

# Load trained model
model = joblib.load("powder_classifier.pkl")

# Initialize PM5003 sensor
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

def classify_powder(pm1, pm2_5, pm10):
    prediction = model.predict([[pm1, pm2_5, pm10]])
    return prediction[0]

try:
    print("Real-time classification running...")
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            
            if "PM1.0" in line and "PM2.5" in line and "PM10" in line:
                pm1 = float(line.split("PM1.0: ")[1].split(",")[0])
                pm2_5 = float(line.split("PM2.5: ")[1].split(",")[0])
                pm10 = float(line.split("PM10: ")[1])
                
                powder_type = classify_powder(pm1, pm2_5, pm10)
                print(f"Detected: {powder_type} | PM1.0: {pm1}, PM2.5: {pm2_5}, PM10: {pm10}")
        
        time.sleep(1)  # Reduce CPU usage

except KeyboardInterrupt:
    print("\nStopped by user")
finally:
    ser.close()
