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

from datetime import datetime
import pandas as pd
import os

LOG_PATH = "data/processed/logs.csv"

def log_interaction(age, device, time_of_day, ad_id, action):
    timestamp = datetime.now().isoformat()
    reward = 1 if action in ["clicked", "purchased"] else 0
    row = {
        "age": age,
        "device": device,
        "time_of_day": time_of_day,
        "ad_id": ad_id,
        "action": action,
        "reward": reward,
        "timestamp": timestamp
    }

    df = pd.DataFrame([row])
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

    if os.path.exists(LOG_PATH):
        df.to_csv(LOG_PATH, mode='a', header=False, index=False)
    else:
        df.to_csv(LOG_PATH, index=False)


