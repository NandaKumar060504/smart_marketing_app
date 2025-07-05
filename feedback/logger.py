# feedback/logger.py

import firebase_admin
from firebase_admin import credentials, db
import datetime
import json
import streamlit as st

def initialize_firebase():
    if not firebase_admin._apps:
        try:
            firebase_json = {
                "type": st.secrets["firebase"]["type"],
                "project_id": st.secrets["firebase"]["project_id"],
                "private_key_id": st.secrets["firebase"]["private_key_id"],
                "private_key": st.secrets["firebase"]["private_key"],
                "client_email": st.secrets["firebase"]["client_email"],
                "client_id": st.secrets["firebase"]["client_id"],
                "auth_uri": st.secrets["firebase"]["auth_uri"],
                "token_uri": st.secrets["firebase"]["token_uri"],
                "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
                "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"],
                "universe_domain": st.secrets["firebase"]["universe_domain"]
            }
            cred = credentials.Certificate(firebase_json)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://smart-marketing-app-2a2ea-default-rtdb.firebaseio.com/'
            })
        except Exception as e:
            print(f"Firebase initialization failed: {e}")

def log_interaction(age, device, time_of_day, ad_id, action):
    initialize_firebase()

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
        print("Interaction successfully logged.")
    except Exception as e:
        print(f"Failed to log interaction: {e}")

