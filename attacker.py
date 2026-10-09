import requests
import threading
import random
import time

session = requests.Session()

# Base URL of your Flask server
BASE_URL = "http://127.0.0.1:8080"

# Endpoints to simulate
ENDPOINTS = [
    "/login",
    "/data"
]

ATTACK_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
    "Mozilla/5.0 (Linux; Android 9; SM-J530F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.110 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36", #compromiosed
    "Mozilla/5.0 (Linux; U; Android 10; en-US; SM-G970F Build/QP1A.190711.020) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36" #compromiosed
]

def send_request(run_time=300):  # run_time in seconds
    start_time = time.time()
    while time.time() - start_time < run_time:
        endpoint = random.choice(ENDPOINTS)
        url = BASE_URL + endpoint
        headers = {
            "User-Agent": random.choice(ATTACK_USER_AGENTS),
            "X-Compromised": "TRUE",
            "X-Fake-IP": f"192.168.0.{random.randint(1, 254)}"
        }

        try:
            payload = {
                "username": "admin" + "A" * 1000,
                "password": "password" + "B" * 3000,
                "bio": "C" * 5000
            }
            response = session.post(url, headers=headers, data=payload, timeout=2)

            req_size = len(response.request.body or "") + sum(len(k)+len(v) for k, v in response.request.headers.items())
            print(f"Sent {response.request.method} to {url} — Size: {req_size} bytes — Status {response.status_code}")
        except Exception as e:
            print(f"Attack error")

        time.sleep(random.uniform(0.1, 0.2))

# Launch many threads to simulate volume
threads = []
for _ in range(20):
    t = threading.Thread(target=send_request, args=(300,), daemon=True)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

 