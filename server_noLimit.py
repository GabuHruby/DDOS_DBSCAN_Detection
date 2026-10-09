from flask import Flask, request
import pandas as pd
import time
import os

app = Flask(__name__)

LOG_FILE = "NoRateLimitData.csv"
if not os.path.exists(LOG_FILE):
    df = pd.DataFrame(columns=["ip", "endpoint", "method", 
    "user_agent", "timestamp", "request_size", "compromised"])
    df.to_csv(LOG_FILE, index=False)

@app.route("/", defaults={"path": ""}, methods=["GET", "POST"])
@app.route("/<path:path>", methods=["GET", "POST"])
def log_request(path):
    ip = request.headers.get("X-Fake-IP", request.remote_addr)
    endpoint = f"/{path}"
    method = request.method
    user_agent = request.headers.get("User-Agent", "Unknown")
    timestamp = int(time.time())
    compromised = request.headers.get("X-Compromised", "unknown")

    # Calculate request size
    headers_size = 0
    for x, y in request.headers.items():
        headers_size += len(x) + len(y)

    try:
        body = request.get_data()
    except:
        body = b""
    body_size = len(body)
    request_line_size = len(method) + len(request.full_path)
    request_size = headers_size + body_size + request_line_size

    # Log to CSV
    new_row = pd.DataFrame([{
        "ip": ip,
        "endpoint": endpoint,
        "method": method,
        "user_agent": user_agent,
        "timestamp": timestamp,
        "request_size": request_size,
        "compromised": compromised
    }])
    new_row.to_csv(LOG_FILE, mode='a', header=False, index=False)
    return "Logged", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)



    