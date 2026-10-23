
import pandas as pd

# -----------------------------------------
# 1. Load original CSV
# -----------------------------------------

INPUT_FILE = "data/valve_telemetry_labeled.csv"

df = pd.read_csv(INPUT_FILE)

# -----------------------------------------
# 2. Create temporary valve health labels
# -----------------------------------------

def assign_status(row):

    flow = row["flow_rate_ml_per_s"]
    latency = row["valve_latency_sec"]

    # Temporary demonstration thresholds
    if flow < 300 or latency > 1.0:
        return "faulty"

    elif flow < 400 or latency > 0.5:
        return "warning"

    else:
        return "healthy"


df["valve_status"] = df.apply(
    assign_status,
    axis=1
)

# -----------------------------------------
# 3. Display label distribution
# -----------------------------------------

print("Valve status distribution:")
print(df["valve_status"].value_counts())

# -----------------------------------------
# 4. Save new labeled dataset
# -----------------------------------------

df.to_csv(
    "data/valve_telemetry_labeled.csv",
    index=False
)

print("\nLabeled dataset saved!")