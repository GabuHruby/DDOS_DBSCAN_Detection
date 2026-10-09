import pandas as pd
import matplotlib.pyplot as plt

# Load the logs
df_no_limit = pd.read_csv("noLimiter.csv")
df_with_limit = pd.read_csv("Limiter.csv")

# Convert UNIX timestamps to readable datetime format
df_no_limit['datetime'] = pd.to_datetime(df_no_limit['timestamp'], unit='s')
df_with_limit['datetime'] = pd.to_datetime(df_with_limit['timestamp'], unit='s')
df_no_limit['compromised'] = df_no_limit['compromised'].astype(str).str.strip().str.upper()
df_with_limit['compromised'] = df_with_limit['compromised'].astype(str).str.strip().str.upper()


'''
# Function to group and count malicious (compromised = TRUE) over time
def plot_malicious_traffic(df, label, color):
    df['timestamp_rounded'] = df['datetime'].dt.floor('10s')  # group by 10 seconds
    count = df[df['compromised'] == "TRUE"].groupby('timestamp_rounded').size()
    plt.plot(count.index, count.values, label=label, color=color)

# Plot both
plt.figure(figsize=(12, 6))
plot_malicious_traffic(df_no_limit, "No Rate Limiting", "red")
plot_malicious_traffic(df_with_limit, "With Rate Limiting", "green")

plt.title("Malicious Traffic Over Time")
plt.xlabel("Time")
plt.ylabel("Number of Requests (per 10s)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
'''

# Calculate totals and malicious counts
total_no_limit = len(df_no_limit)
malicious_no_limit = len(df_no_limit[df_no_limit['compromised'] == 'TRUE'])
normal_no_limit = total_no_limit - malicious_no_limit

total_with_limit = len(df_with_limit)
malicious_with_limit = len(df_with_limit[df_with_limit['compromised'] == 'TRUE'])
normal_with_limit = total_with_limit - malicious_with_limit

# === Figure 1: Malicious in one vs the other ===
labels = ['No Limiting', 'With Limiting']
malicious = [malicious_no_limit, malicious_with_limit]

x = range(len(labels))
plt.figure(figsize=(8, 5))
plt.bar(x, malicious, label="Malicious", color='red')
plt.xticks(x, labels)
plt.ylabel("Number of Requests")
plt.title("Figure 1: Total vs Malicious Requests")
plt.legend()
plt.tight_layout()
plt.show()

# === Figure 2: Normal Requests ===
normals = [normal_no_limit, normal_with_limit]
plt.figure(figsize=(8, 5))
plt.bar(x, normals, color='green')
plt.xticks(x, labels)
plt.ylabel("Number of Requests")
plt.title("Figure 2: Normal Requests That Passed")
plt.tight_layout()
plt.show()