import time
import random

# Simulated powder detection times
DETECTION_TIMES = {
    "Talcum": 40,      # First detection at 40 seconds
    "Baking Soda": 80  # Second detection at 80 seconds
}

# Simulated PM value ranges for each powder
POWDER_PROFILES = {
    "Talcum": {"PM1.0": (1, 10), "PM2.5": (15, 30), "PM10": (100, 200)},
    "Baking Soda": {"PM1.0": (40, 60), "PM2.5": (70, 90), "PM10": (20, 40)}
}

def generate_pm_values(powder_type):
    """Generate random PM values within powder-specific ranges"""
    profile = POWDER_PROFILES[powder_type]
    return {
        "PM1.0": random.randint(*profile["PM1.0"]),
        "PM2.5": random.randint(*profile["PM2.5"]),
        "PM10": random.randint(*profile["PM10"])
    }

def main():
    start_time = time.time()
    print("Starting powder detection simulation...")
    
    while True:
        current_time = time.time() - start_time
        
        # Check if it's time to detect any powder
        for powder, detect_time in DETECTION_TIMES.items():
            if current_time >= detect_time and not hasattr(main, f"detected_{powder}"):
                pm_values = generate_pm_values(powder)
                print(f"\nDetected: {powder}")
                print(f"PM1.0: {pm_values['PM1.0']}")
                print(f"PM2.5: {pm_values['PM2.5']}")
                print(f"PM10: {pm_values['PM10']}")
                setattr(main, f"detected_{powder}", True)
                
                # If all powders detected, exit
                if all(getattr(main, f"detected_{p}", False) for p in DETECTION_TIMES):
                    print("\nSimulation complete!")
                    return
        
        time.sleep(0.1)  # Small delay to reduce CPU usage

if __name__ == "__main__":
    main()
