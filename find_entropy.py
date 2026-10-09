import pandas as pd
import numpy as np
from math import log2

# Load preprocessed data
df = pd.read_csv("processed_nolimiter.csv")

# Load original raw data to get the original (not scaled/encoded) fields
raw_df = pd.read_csv("NoLimiter.csv")

# Merge timestamp and original fields into processed dataframe
df["timestamp"] = pd.to_datetime(raw_df["timestamp"])
df["ip"] = raw_df["ip"]
df["endpoint_raw"] = raw_df["endpoint"]
df["method_raw"] = raw_df["method"]

# Sort by time
df = df.sort_values("timestamp").reset_index(drop=True)

# Define entropy function
def calculate_entropy(values):
    counts = values.value_counts()
    probabilities = counts / counts.sum()
    entropy = -np.sum(probabilities * np.log2(probabilities))
    return entropy

# Define time window (in seconds)
window_size = 5

# Create empty lists to store entropy values
entropy_ip = []
entropy_endpoint = []
entropy_method = []

# Rolling entropy over 5-second windows
for i in range(len(df)):
    start_time = df.loc[i, "timestamp"]
    end_time = start_time + pd.Timedelta(seconds=window_size)
    window = df[(df["timestamp"] >= start_time) & (df["timestamp"] < end_time)]

    entropy_ip.append(calculate_entropy(window["ip"]))
    entropy_endpoint.append(calculate_entropy(window["endpoint_raw"]))
    entropy_method.append(calculate_entropy(window["method_raw"]))

# Add entropy features to dataframe
df["entropy_ip"] = entropy_ip
df["entropy_endpoint"] = entropy_endpoint
df["entropy_method"] = entropy_method

df.drop(columns=["ip", "endpoint_raw", "method_raw"], inplace=True)

# Save enriched dataset
df.to_csv("nolimiter_with_entropy.csv", index=False)
print("Entropy features added")

