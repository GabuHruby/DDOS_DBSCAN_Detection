import matplotlib.pyplot as plt
import numpy as np

# Example metric values (replace with your actual results)
metrics = ["Precision", "Recall", "F1 Score", "Accuracy"]
rate_limiting_values = [99.99, 29.28, 45.30, 32.22]  # in percent
ml_values = [100, 97.47, 98.72, 97.72]  # in percent

x = np.arange(len(metrics))  # label locations
width = 0.35  # bar width

fig, ax = plt.subplots(figsize=(8, 5))
bars1 = ax.bar(x - width/2, rate_limiting_values, width, label="Rate Limiting", color="#4C72B0")
bars2 = ax.bar(x + width/2, ml_values, width, label="Machine Learning", color="#55A868")

# Labels & titles
ax.set_ylabel("Performance (%)")
ax.set_title("Comparison of Rate Limiting vs. Machine Learning", pad=20)
ax.set_xticks(x)
ax.set_xticklabels(metrics)
ax.set_ylim(0, 100)
ax.legend()

# Annotate bars with values
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}%', 
                    xy=(bar.get_x() + bar.get_width() / 2, height - 5),
                    xytext=(0, 2),  # 2 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontweight='bold', fontsize=9)

plt.subplots_adjust(top=0.88)
plt.tight_layout()
plt.show()

