import pandas as pd
import random
from datetime import datetime

# Simulated PM data patterns for different powders
powder_profiles = {
    "Talcum": {"PM1.0": (5, 10), "PM2.5": (15, 25), "PM10": (130, 170)},  # High PM10
    "Baking_Powder": {"PM1.0": (40, 60), "PM2.5": (70, 90), "PM10": (20, 40)}  # High PM1.0/PM2.5
}

data = []
samples_per_powder = 10  # Generate 10 samples per powder

for powder, ranges in powder_profiles.items():
    for _ in range(samples_per_powder):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pm1 = random.uniform(*ranges["PM1.0"])
        pm2_5 = random.uniform(*ranges["PM2.5"])
        pm10 = random.uniform(*ranges["PM10"])
        data.append([timestamp, pm1, pm2_5, pm10, powder])
        print(f"Generated {powder}: PM1.0={pm1:.1f}, PM2.5={pm2_5:.1f}, PM10={pm10:.1f}")

# Save to CSV
df = pd.DataFrame(data, columns=["Timestamp", "PM1.0", "PM2.5", "PM10", "Label"])
df.to_csv("powder_data.csv", index=False)
print("\nSaved simulated data to powder_data.csv")
