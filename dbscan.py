import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

# Load the dataset with entropy and request_size
df = pd.read_csv("nolimiter_with_entropy.csv")

# Select features for clustering
features = ["entropy_ip", "entropy_endpoint", "entropy_method", "request_size"]
X = df[features].copy()

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Run DBSCAN
dbscan = DBSCAN(eps=0.8, min_samples=10)  
labels = dbscan.fit_predict(X_scaled)

# Add cluster labels to dataframe
df["cluster"] = labels

# Classify each cluster in FIRST ITERATION to use in future clustering
cluster_labels = {}
cluster_centroids = {}

for cluster_id in np.unique(labels):
    if cluster_id == -1:
        continue  # skip noise

    cluster_data = df[df["cluster"] == cluster_id]
    majority_label = cluster_data["compromised"].mode()[0]

    # Assign human-readable label
    label_name = "attack" if majority_label else "normal"
    cluster_labels[cluster_id] = label_name

    # Compute centroid
    cluster_scaled = X_scaled[df["cluster"] == cluster_id]
    centroid = cluster_scaled.mean(axis=0)
    cluster_centroids[label_name] = centroid

# Save centroids for real-time classification
np.save("centroids.npy", cluster_centroids)
print("Centroids saved.")

cluster_summary = df.groupby("cluster")["compromised"].value_counts(normalize=True).unstack().fillna(0)
print(cluster_summary)

# Save the labeled dataset
df.to_csv("dbscan_clusters.csv", index=False)
print("Clustering complete.")

