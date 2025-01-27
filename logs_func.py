import csv
from datetime import datetime
import pytz 
import os

def log_event(event_message, timezone="UTC"):
    tz = pytz.timezone(timezone)
    current_time = datetime.now(tz)
    timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")

    log_entry = {
        "Timestamp": timestamp,
        "Event": event_message
    }

    log_to_csv(log_entry)

def log_to_csv(log_entry, file_name="logs/logs.csv"):
    
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    
    file_exists = False
    try:
        with open(file_name, "r"):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(file_name, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Timestamp", "Event"])
        if not file_exists:
            writer.writeheader() 
        writer.writerow(log_entry) 
