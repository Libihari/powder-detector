from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import joblib

# Load your dataset
df = pd.read_csv("powder_data.csv")
X = df[["PM1.0", "PM2.5", "PM10"]]
y = df["Label"]  # Column with "Talcum", "Baking Soda", etc.

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# Save for deployment
joblib.dump(model, "powder_classifier.pkl")
