import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load dataset
df = pd.read_csv("NoLimiter.csv")

# Drop unnecessary columns for ML model
df_model = df[["endpoint", "method", "timestamp", "request_size", "compromised"]].copy()

# Encode categorical variables
le_endpoint = LabelEncoder()
le_method = LabelEncoder()

df_model["endpoint"] = le_endpoint.fit_transform(df_model["endpoint"])
df_model["method"] = le_method.fit_transform(df_model["method"])

# Separate features and label (optional, for testing performance)
X = df_model.drop(columns=["compromised"])
y = df_model["compromised"]

# Scale features (important for DBSCAN and clustering)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Save for reuse
processed_df = pd.DataFrame(X_scaled, columns=X.columns)
processed_df["compromised"] = y

# Save processed version for later
processed_df.to_csv("processed_nolimiter.csv", index=False)

print("Data preprocessing complete.")

