# DDoS Detection with Entropy Features and DBSCAN

Real-time detection of HTTP flood (DDoS) attacks using Shannon entropy features and unsupervised clustering, compared against a traditional IP-based rate limiter.

Built as my high school senior research paper (IB Extended Essay, 2025–2026).

## Results

| Method | Precision | Recall |
|---|---|---|
| IP-based token-bucket rate limiter (baseline) | — | 29.3% |
| Entropy features + DBSCAN | **100%** | **97.5%** |

The rate limiter only catches attackers that send too many requests from a single IP. Clustering on traffic entropy also catches distributed attacks spread across many addresses.

## How it works

1. **Traffic simulation.** A Flask server receives requests from simulated legitimate clients and malicious clients, producing two labeled datasets of ~87,000 requests: one with no protection, one behind a rate limiter.
2. **Baseline.** An IP-based token-bucket rate limiter blocks clients that exceed a request budget.
3. **Feature engineering.** Shannon entropy is computed over rolling 5-second windows of traffic (e.g. how spread out source IPs and request patterns are).
4. **Clustering.** DBSCAN groups traffic windows into clusters. Reference centroids for normal and attack traffic are tuned offline and saved (`centroids.npy`).
5. **Real-time classification.** New clusters from live traffic are matched to the nearest reference centroid and labeled as normal or attack.

## Files

| File | Purpose |
|---|---|
| `server_noLimit.py` | Flask server with no protection |
| `server_rateLimit.py` | Flask server behind the token-bucket rate limiter |
| `normal_client.py` | Simulated legitimate client |
| `attacker.py` | Simulated attacking client |
| `controller.py` / `defense_controller.py` | Runs the experiment and the DBSCAN-based defense |
| `find_entropy.py` / `preprocessing.py` | Entropy feature extraction and data cleaning |
| `dbscan.py` | DBSCAN clustering and centroid tuning |
| `rateLimit_metrics.py` | Baseline precision/recall |
| `comparison_visualization.py` / `visualizing_rateLimit.py` | Charts |
| `*.csv`, `centroids.npy` | Collected datasets and tuned centroids |

## Running it

```bash
pip install flask scikit-learn numpy pandas matplotlib requests
```

1. Start a server: `python server_noLimit.py` (or `server_rateLimit.py`)
2. In separate terminals, run `python normal_client.py` and `python attacker.py`
3. Run the analysis: `python find_entropy.py`, then `python dbscan.py`
4. Generate charts: `python comparison_visualization.py`

## Tech

Python, Flask, scikit-learn, NumPy, pandas, Matplotlib
