import streamlit as st
import pandas as pd
import os
import time

st.set_page_config(page_title="Ad Performance Dashboard", layout="wide")

st.title("📊 Live Ad Performance Dashboard")

# Load feedback data
LOG_PATH = "data/processed/logs.csv"

# Autorefresh every 10 seconds
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=10 * 1000, key="data_refresh")

# Load logs
if os.path.exists(LOG_PATH):
    df = pd.read_csv(LOG_PATH)
else:
    st.warning("No interactions logged yet.")
    st.stop()

# Basic validation
if df.empty:
    st.info("Waiting for users to interact with ads...")
    st.stop()

# Metrics section
st.subheader("📈 Engagement Summary")

total_interactions = len(df)
clicks = len(df[df["action"] == "clicked"])
purchases = len(df[df["action"] == "purchased"])
ignore = len(df[df["action"] == "ignored"])

col1, col2, col3 = st.columns(3)
col1.metric("Total Interactions", total_interactions)
col2.metric("Clicks", clicks)
col3.metric("Purchases", purchases)

st.markdown("---")

# Performance by Ad
st.subheader("🏷️ Performance by Ad")

ad_summary = df.groupby("ad_id")["action"].value_counts().unstack().fillna(0)
ad_summary["CTR"] = ad_summary.get("clicked", 0) / ad_summary.sum(axis=1)
ad_summary["Conversion Rate"] = ad_summary.get("purchased", 0) / ad_summary.sum(axis=1)

st.dataframe(ad_summary.style.format({"CTR": "{:.2%}", "Conversion Rate": "{:.2%}"}))

# Optional: show trend over time
st.markdown("---")
st.subheader("📅 Daily Interaction Trends")

df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df["date"] = df["timestamp"].dt.date

daily_summary = df.groupby(["date", "action"]).size().unstack().fillna(0)

st.line_chart(daily_summary)

