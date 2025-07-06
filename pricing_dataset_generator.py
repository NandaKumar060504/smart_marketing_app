import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import json
import os

# --- Step 1: Initialize Firebase ---
if not firebase_admin._apps:
    if "firebase_key" in os.environ:
        firebase_json = json.loads(os.environ["firebase_key"])
        cred = credentials.Certificate(firebase_json)
    else:
        cred = credentials.Certificate("firebase_key.json")

    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://smart-marketing-app-2a2ea-default-rtdb.firebaseio.com/'
    })

# --- Step 2: Define price mapping ---
ad_id_to_price = {
    38: 149,
    39: 199,
    40: 99,
    41: 179,
    42: 129,
    43: 89,
    44: 159,
}

# --- Step 3: Fetch logs ---
ref = db.reference("logs")
logs = ref.get()

# --- Step 4: Convert to dataset ---
rows = []
if logs:
    for log_id, entry in logs.items():
        ad_id = int(entry['ad_id'])
        price = ad_id_to_price.get(ad_id, None)
        if price is not None:
            row = {
                "age": int(entry['age']),
                "device": entry['device'],
                "time_of_day": entry['time_of_day'],
                "price": price,
                "reward": int(entry['reward'])  # 1 or 0
            }
            rows.append(row)

# --- Step 5: Save as CSV for training ---
df = pd.DataFrame(rows)
df.to_csv("dynamic_pricing_dataset.csv", index=False)
print("✅ Dataset saved as dynamic_pricing_dataset.csv")
