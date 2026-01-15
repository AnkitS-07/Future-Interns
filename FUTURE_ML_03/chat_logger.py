import csv
from datetime import datetime

def log_chat(user, query, response):
    with open("chat_logs.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), user, query, response])
