# feedback/logger.py

import firebase_admin
from firebase_admin import credentials, db
import datetime
import os
import json

# Load credentials from Streamlit secrets if deployed
if "firebase_key" in os.environ or os.path.exists("firebase_key.json"):
    if not firebase_admin._apps:
        try:
            if "firebase_key" in os.environ:
                firebase_json = json.loads(os.environ["firebase_key"])
                cred = credentials.Certificate(firebase_json)
            else:
                cred = credentials.Certificate("firebase_key.json")

            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://smart-marketing-app-2a2ea-default-rtdb.firebaseio.com/'
            })
        except Exception as e:
            print(f"Firebase init error: {e}")

def log_interaction(age, device, time_of_day, ad_id, action):
    data = {
        "age": age,
        "device": device,
        "time_of_day": time_of_day,
        "ad_id": ad_id,
        "action": action,
        "reward": 1 if action in ["clicked", "purchased"] else 0,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    try:
        ref = db.reference("logs")
        ref.push(data)
    except Exception as e:
        print(f"Failed to log interaction: {e}")
