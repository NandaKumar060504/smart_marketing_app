# performance.py

import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import streamlit as st
import json
import os

st.set_page_config(page_title="Ad Performance Dashboard", layout="wide")
st.title("📊 Live Ad Performance Dashboard")

# Auto-refresh every 10 seconds
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=10 * 1000, key="refresh")

# Firebase setup
if not firebase_admin._apps:
    try:
        if "firebase_key" in st.secrets:
            firebase_json = json.loads(st.secrets["firebase_key"])
            cred = credentials.Certificate(firebase_json)
        else:
            cred = credentials.Certificate("firebase_key.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://<your-database-name>.firebaseio.com/'
        })
    except Exception as e:
        st.error(f"Firebase connection failed: {e}")
        st.stop()

# Load data
ref = db.reference("logs")
data = ref.get()

if not data:
    st.warning("No interactions yet.")
    st.stop()

df = pd.DataFrame(data.values())
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df["date"] = df["timestamp"].dt.date

# Metrics
st.subheader("📈 Engagement Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total", len(df))
col2.metric("Clicks", (df["action"] == "clicked").sum())
col3.metric("Purchases", (df["action"] == "purchased").sum())

st.markdown("---")
st.subheader("🏷️ Performance by Ad")

ad_summary = df.groupby("ad_id")["action"].value_counts().unstack().fillna(0)
ad_summary["CTR"] = ad_summary.get("clicked", 0) / ad_summary.sum(axis=1)
ad_summary["Conversion Rate"] = ad_summary.get("purchased", 0) / ad_summary.sum(axis=1)

st.dataframe(ad_summary.style.format({"CTR": "{:.2%}", "Conversion Rate": "{:.2%}"}))

st.markdown("---")
st.subheader("📅 Daily Interaction Trends")
daily_summary = df.groupby(["date", "action"]).size().unstack().fillna(0)
st.line_chart(daily_summary)

