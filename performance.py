import streamlit as st
import pandas as pd
import os

from streamlit_autorefresh import st_autorefresh

# Page configuration
st.set_page_config(page_title="📊 Live Ad Performance Dashboard", layout="wide")
st.title("📊 Live Ad Performance Dashboard")

# Autorefresh every 10 seconds
st_autorefresh(interval=10 * 1000, key="data_refresh")

# Load feedback data
LOG_PATH = "data/processed/logs.csv"

if not os.path.exists(LOG_PATH):
    st.warning("No interactions logged yet.")
    st.stop()

df = pd.read_csv(LOG_PATH)

# Validate data
if df.empty:
    st.info("Waiting for users to interact with ads...")
    st.stop()

# Safe conversion if timestamp exists
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["date"] = df["timestamp"].dt.date
else:
    df["date"] = pd.NaT  # Fill with empty values

# Summary Metrics
st.subheader("📈 Engagement Summary")

total_interactions = len(df)
clicks = (df["action"] == "clicked").sum()
purchases = (df["action"] == "purchased").sum()
ignored = (df["action"] == "ignored").sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Interactions", total_interactions)
col2.metric("Clicks", clicks)
col3.metric("Purchases", purchases)

st.markdown("---")

# 📊 Performance by Ad
st.subheader("🏷️ Performance by Ad")

ad_summary = df.groupby("ad_id")["action"].value_counts().unstack().fillna(0)
ad_summary["CTR"] = ad_summary.get("clicked", 0) / ad_summary.sum(axis=1)
ad_summary["Conversion Rate"] = ad_summary.get("purchased", 0) / ad_summary.sum(axis=1)

st.dataframe(ad_summary.style.format({"CTR": "{:.2%}", "Conversion Rate": "{:.2%}"}))

# 🕒 Daily Trends (only if timestamp is available)
if "timestamp" in df.columns and df["timestamp"].notnull().any():
    st.markdown("---")
    st.subheader("📅 Daily Interaction Trends")

    daily_summary = df.groupby(["date", "action"]).size().unstack().fillna(0)
    st.line_chart(daily_summary)
else:
    st.info("No timestamp data available for trend analysis.")
