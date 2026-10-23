import pandas as pd
import numpy as np
from pathlib import Path

INPUT_FILE = "data/valve_telemetry_labeled.csv"
OUTPUT_FILE = "data/valve_telemetry_augmented.csv"

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# Load existing labeled data
df = pd.read_csv(INPUT_FILE)

print("Original dataset shape:", df.shape)
print("\nOriginal labels:")
print(df["valve_status"].value_counts())

# Number of synthetic records
HEALTHY_COUNT = 300
WARNING_COUNT = 300


def generate_healthy_records(count):
    records = []

    for i in range(count):
        dispense_duration = np.random.uniform(1.0, 6.0)

        flow_rate = np.random.uniform(75, 120)
        volume_ml = dispense_duration * flow_rate

        record = {
            "id": f"synthetic_healthy_{i}",
            "device_id": "synthetic_device",
            "boot_offset_ms": np.random.randint(1000, 100000),
            "device_timestamp_ms": np.nan,
            "dispense_duration_sec": round(dispense_duration, 3),
            "volume_ml": round(volume_ml, 2),
            "ir_confidence_pct": round(np.random.uniform(92, 100), 2),
            "tof_confidence_pct": round(np.random.uniform(92, 100), 2),
            "valve_cycle_count": np.random.randint(1, 200),
            "valve_latency_sec": round(np.random.uniform(0.03, 0.20), 3),
            "flow_rate_ml_per_s": round(flow_rate, 2),
            "event_timestamp": pd.Timestamp.now(),
            "created_at": pd.Timestamp.now(),
            "valve_status": "healthy",
            "is_synthetic": True
        }

        records.append(record)

    return pd.DataFrame(records)


def generate_warning_records(count):
    records = []

    for i in range(count):
        dispense_duration = np.random.uniform(0.5, 8.0)

        flow_rate = np.random.uniform(25, 75)
        volume_ml = dispense_duration * flow_rate

        record = {
            "id": f"synthetic_warning_{i}",
            "device_id": "synthetic_device",
            "boot_offset_ms": np.random.randint(1000, 100000),
            "device_timestamp_ms": np.nan,
            "dispense_duration_sec": round(dispense_duration, 3),
            "volume_ml": round(volume_ml, 2),
            "ir_confidence_pct": round(np.random.uniform(80, 96), 2),
            "tof_confidence_pct": round(np.random.uniform(80, 96), 2),
            "valve_cycle_count": np.random.randint(1, 250),
            "valve_latency_sec": round(np.random.uniform(0.25, 1.0), 3),
            "flow_rate_ml_per_s": round(flow_rate, 2),
            "event_timestamp": pd.Timestamp.now(),
            "created_at": pd.Timestamp.now(),
            "valve_status": "warning",
            "is_synthetic": True
        }

        records.append(record)

    return pd.DataFrame(records)


# Generate synthetic records
healthy_df = generate_healthy_records(HEALTHY_COUNT)
warning_df = generate_warning_records(WARNING_COUNT)

# Mark original records as real
df["is_synthetic"] = False

# Combine original and synthetic data
augmented_df = pd.concat(
    [df, healthy_df, warning_df],
    ignore_index=True
)

# Shuffle the dataset
augmented_df = augmented_df.sample(
    frac=1,
    random_state=RANDOM_SEED
).reset_index(drop=True)

# Save augmented dataset
Path("data").mkdir(exist_ok=True)

augmented_df.to_csv(OUTPUT_FILE, index=False)

print("\nSynthetic records created:")
print("Healthy:", HEALTHY_COUNT)
print("Warning:", WARNING_COUNT)

print("\nFinal dataset shape:", augmented_df.shape)

print("\nFinal label distribution:")
print(augmented_df["valve_status"].value_counts())

print("\nSaved to:", OUTPUT_FILE)