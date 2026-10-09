import requests
import random
import time
session = requests.Session()

BASE_URL = "http://127.0.0.1:8080"
ENDPOINTS = [
    "/",
    "/search?q=test"
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Linux; Android 11; SM-A107F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/114.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 10; en-US; SM-G970F Build/QP1A.190711.020) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36"
]

def send_request(compromised=False):
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "X-Fake-IP": f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}",
        "X-Compromised": str(compromised)
    }
    try:
        # 5% chance of simulating login
        if random.random() < 0.05:
            url = BASE_URL + "/login"
            data = {"username": "test_user", "password": "secure123"}
            response = session.post(url, headers=headers, data=data, timeout=2)
        else:
            url = BASE_URL + random.choice(ENDPOINTS)
            response = session.get(url, headers=headers, timeout=2)
        req_size = len(response.request.body or "") + sum(len(k)+len(v) for k, v in response.request.headers.items())
        print(f"Sent {response.request.method} to {url} — Size: {req_size} bytes — Status {response.status_code}")
    except Exception as e:
        print(f"Normal client error")

    

def run_normal_client(run_time=660):
    start_time = time.time()
    while time.time() - start_time < run_time:
        send_request(compromised=False)
        time.sleep(random.uniform(1.5, 3.5))

