from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import joblib
import time

def train_and_save_model():
    print("Starting powder detection model training...")
    
    # Load dataset
    try:
        df = pd.read_csv("powder_data.csv")
        X = df[["PM1.0", "PM2.5", "PM10"]]
        y = df["Label"]
        
        print("\nDataset loaded successfully")
        print(f"Training samples: {len(X)}")
        print(f"Powder types: {', '.join(y.unique())}")
        
        # Train model
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X, y)
        
        # Save model
        joblib.dump(model, "powder_classifier.pkl")
        print("\nModel trained and saved as powder_classifier.pkl")
            
    except FileNotFoundError:
        print("\nError: powder_data.csv not found")
def simulate_detections(model):
    print("\nStarting powder detection...")
    
    # Simulated detection times
    detection_times = {"Talcum": 40, "Baking Soda": 80}
    start_time = time.time()
    
    while True:
        current_time = time.time() - start_time
        
        for powder, detect_time in detection_times.items():
            if current_time >= detect_time and not hasattr(detections, f"detected_{powder}"):
                # Generate realistic PM values
                pm_values = {
                    "Talcum": {"PM1.0": random.randint(1, 10), 
                              "PM2.5": random.randint(15, 30), 
                              "PM10": random.randint(100, 200)},
                    "Baking Soda": {"PM1.0": random.randint(40, 60),
                                   "PM2.5": random.randint(70, 90),
                                   "PM10": random.randint(20, 40)}
                }[powder]
                
                # Format output like the simulation
                print(f"\nDetected: {powder}")
                print(f"PM1.0: {pm_values['PM1.0']}")
                print(f"PM2.5: {pm_values['PM2.5']}")
                print(f"PM10: {pm_values['PM10']}")
                
                setattr(detections, f"detected_{powder}", True)
                
                if all(getattr(detections, f"detected_{p}", False) for p in detection_times):
                    print("\nDetection complete!")
                    return
        
        time.sleep(0.1)

def run_simulation_mode():
    print("\nStarting powder detection ...")
    
    detection_times = {"Talcum": 40, "Baking Soda": 80}
    start_time = time.time()
    
    while True:
        current_time = time.time() - start_time
        
        for powder, detect_time in detection_times.items():
            if current_time >= detect_time and not hasattr(run_simulation_mode, f"detected_{powder}"):
                pm_values = {
                    "Talcum": {"PM1.0": random.randint(1, 10), 
                              "PM2.5": random.randint(15, 30), 
                              "PM10": random.randint(100, 200)},
                    "Baking Soda": {"PM1.0": random.randint(40, 60),
                                  "PM2.5": random.randint(70, 90),
                                  "PM10": random.randint(20, 40)}
                }[powder]
                
                print(f"\nDetected: {powder}")
                print(f"PM1.0: {pm_values['PM1.0']}")
                print(f"PM2.5: {pm_values['PM2.5']}")
                print(f"PM10: {pm_values['PM10']}")
                
                setattr(f"detected_{powder}", True)
                
                if all(getattr(run_simulation_mode, f"detected_{p}", False) for p in detection_times):
                    print("\ complete!")
                    return
        
        time.sleep(0.1)

if __name__ == "__main__":
    train_and_save_model()
