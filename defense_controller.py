import pandas as pd
import numpy as np
import time
import os
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Load saved centroids from first iteration
centroids = np.load("centroids.npy", allow_pickle=True).item()

# Define the features used
features = ["entropy_ip", "entropy_endpoint", "entropy_method", "request_size"]

# Configuration
CSV_FILE = "NoRateLimitData.csv"
WINDOW_MINUTES = 15
CHECK_INTERVAL_SECONDS = 120
EPS = 0.8
MIN_SAMPLES = 1000

# Entropy calculation
def calculate_entropy(values):
    counts = values.value_counts()
    probabilities = counts / counts.sum()
    return -np.sum(probabilities * np.log2(probabilities))

# Main defense loop
def defense_monitor():
    print("\U0001F6A8 Real-time DDoS Defense Monitor started...")

    while True:
        if not os.path.exists(CSV_FILE):
            print("\u26A0\ufe0f No data file found. Waiting...")
            time.sleep(CHECK_INTERVAL_SECONDS)
            continue

        df = pd.read_csv(CSV_FILE)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit='s')

        # Filter last N minutes
        now = pd.to_datetime(int(time.time()), unit='s')
        time_threshold = now - timedelta(minutes=WINDOW_MINUTES)
        df = (df[df["timestamp"] >= time_threshold].sort_values("timestamp").reset_index(drop=True).copy())
        
        if len(df) < 10:
            print("\U0001F4C9 Not enough data to analyze. Waiting...")
            time.sleep(CHECK_INTERVAL_SECONDS)
            continue

        # Entropy calculations
        entropy_ip = []
        entropy_endpoint = []
        entropy_method = []

        for i in range(len(df)):
            start = df.loc[i, "timestamp"]
            end = start + timedelta(seconds=5)
            window = df[(df["timestamp"] >= start) & (df["timestamp"] < end)]

            entropy_ip.append(calculate_entropy(window["ip"]))
            entropy_endpoint.append(calculate_entropy(window["endpoint"]))
            entropy_method.append(calculate_entropy(window["method"]))

        df["entropy_ip"] = entropy_ip
        df["entropy_endpoint"] = entropy_endpoint
        df["entropy_method"] = entropy_method

        X = df[features].fillna(0)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        dbscan = DBSCAN(eps=EPS, min_samples=MIN_SAMPLES)
        labels = dbscan.fit_predict(X_scaled)
        df["cluster"] = labels

        attack_centroid = centroids["attack"]
        cluster_centroids = {
            cluster: X_scaled[df["cluster"] == cluster].mean(axis=0)
            for cluster in np.unique(labels)
            if cluster != -1
        }

        predicted_labels = {}
        for cid, centroid in cluster_centroids.items():
            distance = np.linalg.norm(centroid - attack_centroid)
            predicted_labels[cid] = "attack" if distance < 4 else "normal"

        df["predicted"] = df["cluster"].map(predicted_labels).fillna("normal")

        if "compromised" in df.columns:
            df["actual_attack"] = df["compromised"]
            df["predicted_attack"] = df["predicted"] == "attack"
            y_true = df["actual_attack"]
            y_pred = df["predicted_attack"]

            print("\n\U0001F4CA Performance Metrics:")
            print("Accuracy:", accuracy_score(y_true, y_pred))
            print("Precision:", precision_score(y_true, y_pred))
            print("Recall:", recall_score(y_true, y_pred))
            print("F1 Score:", f1_score(y_true, y_pred))

            print("\n\U0001F522 Confusion Matrix:")
            print(confusion_matrix(y_true, y_pred))
        else:
            print("\u26A0\ufe0f 'compromised' column not found. Skipping metrics.")

        attack_clusters = [cid for cid, label in predicted_labels.items() if label == "attack"]
        if attack_clusters:
            for cluster_id in attack_clusters:
                print(f"\U0001F6A8 ALERT: Potential DDoS attack detected in cluster {cluster_id}!")
        else:
            print("No attack clusters detected.")

        print(f"Waiting {CHECK_INTERVAL_SECONDS} seconds before next check...")
        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    defense_monitor()