
import pandas as pd
import joblib

from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

# -----------------------------------------
# 1. Load train and test data
# -----------------------------------------

train_df = pd.read_csv("data/train.csv")
test_df = pd.read_csv("data/test.csv")

# -----------------------------------------
# 2. Feature columns
# -----------------------------------------

FEATURES = [
    "dispense_duration_sec",
    "volume_ml",
    "ir_confidence_pct",
    "tof_confidence_pct",
    "valve_cycle_count",
    "valve_latency_sec",
    "flow_rate_ml_per_s"
]

TARGET = "valve_status"

X_train = train_df[FEATURES]
y_train = train_df[TARGET]

X_test = test_df[FEATURES]
y_test = test_df[TARGET]

# -----------------------------------------
# 3. Check classes
# -----------------------------------------

print("Training classes:")
print(y_train.value_counts())

print("\nTesting classes:")
print(y_test.value_counts())

# -----------------------------------------
# 4. Create Random Forest
# -----------------------------------------

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=8,
    min_samples_leaf=3,
    random_state=42,
    class_weight="balanced"
)

# -----------------------------------------
# 5. Train
# -----------------------------------------

model.fit(X_train, y_train)

print("\nTraining completed!")

# -----------------------------------------
# 6. Test
# -----------------------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("\nAccuracy:", accuracy)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)

print("\nConfusion Matrix:")
print(
    confusion_matrix(
        y_test,
        predictions
    )
)

# -----------------------------------------
# 7. Save model
# -----------------------------------------

Path("models").mkdir(exist_ok=True)

joblib.dump(
    {
        "model": model,
        "features": FEATURES
    },
    "models/valve_health_model.pkl"
)

print("\nModel saved!")