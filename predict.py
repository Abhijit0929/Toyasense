import joblib
import pandas as pd

MODEL_FILE = "models/valve_health_model.pkl"

FEATURES = [
    "dispense_duration_sec",
    "volume_ml",
    "ir_confidence_pct",
    "tof_confidence_pct",
    "valve_cycle_count",
    "valve_latency_sec",
    "flow_rate_ml_per_s"
]

# Load saved file
loaded_data = joblib.load(MODEL_FILE)

# Extract model if saved inside a dictionary
if isinstance(loaded_data, dict):
    print("Loaded model package.")
    print("Available keys:", loaded_data.keys())

    if "model" in loaded_data:
        model = loaded_data["model"]
    elif "classifier" in loaded_data:
        model = loaded_data["classifier"]
    else:
        raise ValueError(
            "Dictionary does not contain 'model' or 'classifier'."
        )
else:
    model = loaded_data

# Check whether the loaded object supports prediction
if not hasattr(model, "predict"):
    raise TypeError(
        f"Loaded object cannot predict. Object type: {type(model)}"
    )

print("\nToyaSense Valve Health Prediction")
print("----------------------------------")

dispense_duration = float(
    input("Dispense duration: ")
)

volume_ml = float(
    input("Volume: ")
)

ir_confidence = float(
    input("IR confidence: ")
)

tof_confidence = float(
    input("ToF confidence: ")
)

valve_cycle_count = int(
    input("Valve cycle count: ")
)

valve_latency = float(
    input("Valve latency: ")
)

flow_rate = float(
    input("Flow rate: ")
)

# Create input with exactly the same feature names
input_data = pd.DataFrame([{
    "dispense_duration_sec": dispense_duration,
    "volume_ml": volume_ml,
    "ir_confidence_pct": ir_confidence,
    "tof_confidence_pct": tof_confidence,
    "valve_cycle_count": valve_cycle_count,
    "valve_latency_sec": valve_latency,
    "flow_rate_ml_per_s": flow_rate
}])

# Ensure feature order is correct
input_data = input_data[FEATURES]

print("\nInput data:")
print(input_data)

prediction = model.predict(input_data)[0]

print("\nPredicted Valve Status:", prediction)

# Show prediction probabilities if available
if hasattr(model, "predict_proba"):
    probabilities = model.predict_proba(input_data)[0]

    print("\nPrediction probabilities:")

    for class_name, probability in zip(
        model.classes_,
        probabilities
    ):
        print(f"{class_name}: {probability:.2%}")

if prediction == "healthy":
    print("\nValve is operating normally.")

elif prediction == "warning":
    print("\nWarning: Valve may require inspection.")

elif prediction == "faulty":
    print("\nAlert: Possible valve fault detected.")