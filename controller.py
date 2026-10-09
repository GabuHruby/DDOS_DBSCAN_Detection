import threading
import time
import subprocess
import random
import normal_client 

NORMAL_CLIENTS = 20
ATTACK_CLIENTS = 10

normal_threads = []
attack_threads = []

# Launch normal clients
print("Starting normal clients...")
for _ in range(NORMAL_CLIENTS):
    t = threading.Thread(target=normal_client.run_normal_client, args=(660,))
    t.start()
    normal_threads.append(t)
    time.sleep(random.uniform(0.1, 0.3))

# Wait before attack
attack_delay = 300
print(f"Waiting {attack_delay} seconds before starting attack...")
time.sleep(attack_delay)

print("Starting attacker clients...")
for _ in range(ATTACK_CLIENTS):
    t = threading.Thread(target=lambda: subprocess.run(["python3", "attacker.py"]))
    t.start()
    attack_threads.append(t)
    time.sleep(random.uniform(0.1, 0.3))

# Let attack run
attack_duration = 300
print(f"Attack in progress for {attack_duration} seconds...")
time.sleep(attack_duration)

# Wait for attackers to finish
print("Waiting for attacker threads to finish...")
for t in attack_threads:
    t.join()

# Let normal traffic continue briefly
final_duration = 60
print(f"Attack ended. Letting normal traffic run for {final_duration} more seconds...")
time.sleep(final_duration)

# Now stop the normal clients
print("Stopping normal clients...")
for t in normal_threads:
    t.join()

print("Simulation complete.")

