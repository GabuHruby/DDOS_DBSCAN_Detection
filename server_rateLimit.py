from flask import Flask, request
import pandas as pd
import time
import os
from collections import defaultdict
import threading

app = Flask(__name__)

# Rate limit settings
TOKENS_PER_SECOND = 1
BURST_CAPACITY = 10

# Token buckets: {ip: [tokens, last_refill_time]}
def create_token_bucket():
    return [BURST_CAPACITY, time.time()]

token_buckets = defaultdict(create_token_bucket)
lock = threading.Lock()

def is_request_allowed(ip):
    with lock:
        tokens, last_refill = token_buckets[ip]
        current_time = time.time()

        elapsed = current_time - last_refill
        new_tokens = min(BURST_CAPACITY, tokens + elapsed * TOKENS_PER_SECOND)
        token_buckets[ip] = [new_tokens, current_time]

        if new_tokens >= 1:
            token_buckets[ip][0] -= 1
            return True, new_tokens, token_buckets[ip][0] 
        else:
            return False, new_tokens, new_tokens 

# Initialize CSV file
LOG_FILE = "RateLimitData.csv"
if not os.path.exists(LOG_FILE):
    df = pd.DataFrame(columns=[
        "ip","endpoint","method","user_agent","timestamp","request_size",
        "compromised","allowed","status_code","tokens_before","tokens_after"
    ])
    df.to_csv(LOG_FILE, index=False)

@app.route("/", defaults={"path": ""}, methods=["GET", "POST"])
@app.route("/<path:path>", methods=["GET", "POST"])
def log_request(path):
    # Metadata
    ip = request.headers.get("X-Fake-IP", request.remote_addr)
    endpoint = f"/{path}"
    method = request.method
    user_agent = request.headers.get("User-Agent", "Unknown")
    timestamp = int(time.time())
    compromised_header = str(request.headers.get("X-Compromised", "False")).strip().lower()
    compromised = True if compromised_header in ("true","1","yes") else False

    # Request size (approx)
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

    # Rate limit decision
    allowed, tokens_before, tokens_after = is_request_allowed(ip)
    status_code = 200 if allowed else 429

    # Log ONE row for every request (allowed or blocked)
    new_row = pd.DataFrame([{
        "ip": ip,
        "endpoint": endpoint,
        "method": method,
        "user_agent": user_agent,
        "timestamp": timestamp,
        "request_size": request_size,
        "compromised": compromised,
        "allowed": allowed,
        "status_code": status_code,
        "tokens_before": int(tokens_before),
        "tokens_after": int(tokens_after)
    }])
    new_row.to_csv(LOG_FILE, mode='a', header=False, index=False)

    # Respond
    if allowed:
        return "Logged", 200
    else:
        return "Rate limit exceeded", 429

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)