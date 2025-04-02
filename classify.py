import time
import random

# Simulated powder profiles (same as above)
powders = ["Talcum", "Baking_Powder"]
count = 0

print("Simulating real-time classification...")
while True:
    # Alternate between powders every 5 seconds
    current_powder = powders[count % 2]
    count += 1

    # Generate fake PM values based on the current powder
    if current_powder == "Talcum":
        pm1 = round(random.uniform(5, 10), 1)
        pm2_5 = round(random.uniform(15, 25), 1)
        pm10 = round(random.uniform(130, 170), 1)
    else:
        pm1 = round(random.uniform(40, 60), 1)
        pm2_5 = round(random.uniform(70, 90), 1)
        pm10 = round(random.uniform(20, 40), 1)

    print(f"Detected: {current_powder} | PM1.0: {pm1}, PM2.5: {pm2_5}, PM10: {pm10}")
    time.sleep(5)  # Change powder every 5 seconds
