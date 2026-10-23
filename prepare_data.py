
import pandas as pd
from pathlib import Path

# -----------------------------------------
# 1. Load your actual CSV
# -----------------------------------------

INPUT_FILE = "data/valve_telemetry_augmented.csv"

df = pd.read_csv(INPUT_FILE)

print("Original dataset shape:", df.shape)

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

# -----------------------------------------
# 3. Check columns
# -----------------------------------------

required = FEATURES + [TARGET]

missing = [
    col for col in required
    if col not in df.columns
]

if missing:
    print("\nMissing columns:")
    print(missing)

    raise ValueError(
        "Add valve_status labels before training."
    )

# -----------------------------------------
# 4. Remove missing values
# -----------------------------------------

df = df.dropna(subset=required)

# -----------------------------------------
# 5. Sort by valve cycle count
# -----------------------------------------

df = df.sort_values(
    "valve_cycle_count"
).reset_index(drop=True)

# -----------------------------------------
# 6. Time-based 80/20 split
# -----------------------------------------

split_index = int(len(df) * 0.80)

train_df = df.iloc[:split_index].copy()
test_df = df.iloc[split_index:].copy()

# -----------------------------------------
# 7. Save datasets
# -----------------------------------------

Path("data").mkdir(exist_ok=True)

train_df.to_csv(
    "data/train.csv",
    index=False
)

test_df.to_csv(
    "data/test.csv",
    index=False
)

print("\nTraining records:", len(train_df))
print("Testing records:", len(test_df))

print("\nTraining labels:")
print(train_df[TARGET].value_counts())

print("\nTesting labels:")
print(test_df[TARGET].value_counts())

print("\nData preparation complete!")