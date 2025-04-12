#!/usr/bin/env python3
import psutil
import time
import os
import traceback
from datetime import datetime

# Configuration
CPU_THRESHOLD = 85              # CPU usage threshold (%)
RAM_THRESHOLD = 85              # RAM usage threshold (%)
NET_THRESHOLD_MB = 50           # Network traffic threshold in MB over the interval
CHECK_INTERVAL = 5              # Time between checks (in seconds)
LOG_FILE = "/path/to/logs.txt"
LOG_CLEAN_INTERVAL = 3600       # Time in seconds before logs are cleared (if no alerts)

# Timestamp of the last alert
last_alert_time = None

# Ensure log directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log_event(message):
    """Logs a message with timestamp and updates last alert time."""
    global last_alert_time
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    full_message = f"[{timestamp}] {message}"
    print(full_message)
    with open(LOG_FILE, 'a') as f:
        f.write(full_message + '\n')
    last_alert_time = time.time()

def check_cpu():
    """Checks CPU usage and logs if it exceeds the threshold."""
    usage = psutil.cpu_percent(interval=1)
    if usage > CPU_THRESHOLD:
        log_event(f"⚠️ High CPU usage: {usage}%")

def check_ram():
    """Checks RAM usage and logs if it exceeds the threshold."""
    mem = psutil.virtual_memory()
    if mem.percent > RAM_THRESHOLD:
        used = format_bytes(mem.used)
        total = format_bytes(mem.total)
        log_event(f"⚠️ High RAM usage: {mem.percent}% ({used} / {total})")

def check_net():
    """Checks network usage and logs if it exceeds the threshold."""
    global last_net
    current = psutil.net_io_counters()
    sent = current.bytes_sent - last_net.bytes_sent
    recv = current.bytes_recv - last_net.bytes_recv
    total = sent + recv
    if total > NET_THRESHOLD_MB * 1024 * 1024:
        log_event(f"⚠️ Unusual network traffic: {format_bytes(total)} in {CHECK_INTERVAL}s (sent={format_bytes(sent)}, recv={format_bytes(recv)})")
    last_net = current

def format_bytes(num):
    """Converts bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return f"{num:.2f} {unit}"
        num /= 1024.0
    return f"{num:.2f} TB"

def clean_logs_if_idle():
    """Deletes the log file if no alerts occurred in the defined period."""
    if os.path.exists(LOG_FILE):
        if last_alert_time is None:
            # No alert ever occurred, delete log
            os.remove(LOG_FILE)
        else:
            time_since_last_alert = time.time() - last_alert_time
            if time_since_last_alert > LOG_CLEAN_INTERVAL:
                log_event("ℹ️ No alerts in the last hour. Cleaning logs.")
                with open(LOG_FILE, 'w') as f:
                    f.write(f"[{datetime.now()}] (Logs auto-cleaned after inactivity)\n")

def monitor_loop():
    """Main monitoring loop."""
    log_event("🔍 System monitoring started")
    while True:
        try:
            check_cpu()
            check_ram()
            check_net()
            clean_logs_if_idle()
            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            err_msg = f"[ERROR] Exception: {str(e)}\n{traceback.format_exc()}"
            log_event(err_msg)
            time.sleep(1)

if __name__ == "__main__":
    last_net = psutil.net_io_counters()
    monitor_loop()
