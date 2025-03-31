import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Load labeled data (add your labels manually to the CSV first!)
df = pd.read_csv("powder_data.csv")

# Features (PM values) and Labels (must exist in CSV)
X = df[["PM1.0", "PM2.5", "PM10"]]
y = df["Label"]  # Column with values like "Talcum", "Baking_Soda", etc.

# Split data into training/testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
accuracy = model.score(X_test, y_test)
print(f"Model trained! Accuracy: {accuracy:.2f}")

# Save model for later use
joblib.dump(model, "powder_classifier.pkl")
print("Model saved as powder_classifier.pkl")
