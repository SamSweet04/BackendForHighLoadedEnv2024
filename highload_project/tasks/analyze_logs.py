import os
import re

LOG_FILE = 'secure_app.log'

def analyze_logs():
    if not os.path.exists(LOG_FILE):
        print(f"Log file {LOG_FILE} does not exist.")
        return

    with open(LOG_FILE, 'r') as log_file:
        logs = log_file.readlines()

    failed_login_attempts = 0
    ip_addresses = {}

    for log in logs:
        if "Failed login attempt" in log:
            failed_login_attempts += 1
            match = re.search(r'IP: ([\d\.]+)', log)
            if match:
                ip = match.group(1)
                ip_addresses[ip] = ip_addresses.get(ip, 0) + 1

    print(f"Total failed login attempts: {failed_login_attempts}")
    for ip, count in ip_addresses.items():
        print(f"IP: {ip} - Attempts: {count}")
