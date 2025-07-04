# # feedback/logger.py
# import os
# import csv
# from datetime import datetime

# LOG_PATH = "/Users/nandakumart/Nanda_Kumar_T/smart_marketing_app/data/raw/data/raw/sample_ads.csv"

# # Ensure folder exists
# os.makedirs("data/processed", exist_ok=True)

# def log_interaction(user_context, ad, price, action):
#     log_data = {
#         "timestamp": datetime.now().isoformat(),
#         "age": user_context["age"],
#         "device": user_context["device"],
#         "time_of_day": user_context["time_of_day"],
#         "ad_id": ad["ad_id"],
#         "ad_title": ad["title"],
#         "price": price,
#         "action": action
#     }

#     # Write header if file is empty
#     write_header = not os.path.exists(LOG_PATH)

#     with open(LOG_PATH, mode="a", newline="") as file:
#         writer = csv.DictWriter(file, fieldnames=log_data.keys())
#         if write_header:
#             writer.writeheader()
#         writer.writerow(log_data)

# feedback/logger.py

import csv
import os

def log_interaction(age, device, time_of_day, ad_id, action):
    os.makedirs("data/processed", exist_ok=True)
    filepath = "data/processed/logs.csv"
    
    file_exists = os.path.exists(filepath)
    with open(filepath, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["age", "device", "time_of_day", "ad_id", "action", "reward"])
        
        # reward: 1 if clicked or purchased, else 0
        reward = 1 if action in ["clicked", "purchased"] else 0
        writer.writerow([age, device, time_of_day, ad_id, action, reward])

