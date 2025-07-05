# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# import pandas as pd
# import streamlit as st
# from utils import load_ads, pick_random_ad, get_current_context
# from feedback.logger import log_interaction
# # ...existing code...
# from models.bandit_model import (
#     load_or_train_bandit, 
#     choose_ad, 
#     get_context, 
#     update_bandit
# )



# st.set_page_config(page_title="Smart Ad Targeting", layout="wide")

# # Load ads
# ads_df = load_ads("data/raw/sample_ads.csv")

# st.title("🧠 AI-Powered Marketing Demo")

# # Simulate User
# st.sidebar.header("👤 Simulated User Profile")
# age = st.sidebar.slider("Age", 18, 65, 30)
# device = st.sidebar.selectbox("Device", ["Mobile", "Desktop", "Tablet"])
# time_of_day = st.sidebar.selectbox("Time of Day", ["Morning", "Afternoon", "Evening", "Night"])

# user_context = get_current_context(age, device, time_of_day)

# # # Select an ad
# # selected_ad = pick_random_ad(ads_df)
# # Load feedback if it exists
# feedback_path = "data/processed/logs.csv"
# feedback_df = pd.read_csv(feedback_path) if os.path.exists(feedback_path) else None

# context = get_context(user_context)
# bandit = load_or_train_bandit(ads_df, feedback_df)
# selected_ad = choose_ad(bandit, ads_df, context)

# # Show Ad
# st.subheader("🎯 Recommended Ad")
# st.image(selected_ad['image_url'], width=150)
# st.markdown(f"**{selected_ad['title']}**")
# st.write(selected_ad['description'])

# # Placeholder price
# price = 49.99  # this will later be dynamic using RL

# st.markdown(f"💰 **Special Offer Price:** ${price}")

# # Feedback Buttons
# st.markdown("### What does the user do?")
# col1, col2, col3 = st.columns(3)
# with col1:
#     if st.button("✅ Clicked Ad"):
#         log_interaction(user_context, selected_ad, price, action="clicked")
#         st.success("Logged: Clicked Ad")
# with col2:
#     if st.button("❌ Ignored Ad"):
#         log_interaction(user_context, selected_ad, price, action="ignored")
#         st.info("Logged: Ignored Ad")
# with col3:
#     if st.button("🛒 Purchased"):
#         log_interaction(user_context, selected_ad, price, action="purchased")
#         st.success("Logged: Purchase Made")

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# app/main.py

import streamlit as st
import pandas as pd
import os
from app.utils import load_ads
from feedback.logger import log_interaction
from models.bandit_model import (
    load_or_train_bandit, 
    choose_ad, 
    get_context_vector, 
    update_bandit
)

st.set_page_config(page_title="Smart Ad Targeting", layout="centered")
st.title("📈 AI-Powered Ad Targeting")

# Load data
# ads_df = load_ads()
ads_df = load_ads("data/raw/sample_ads.csv")

feedback_path = "/Users/nandakumart/Nanda_Kumar_T/smart_marketing_app/data/processed/logs.csv"
feedback_df = pd.read_csv(feedback_path) if os.path.exists(feedback_path) else None

# Sidebar – user input
st.sidebar.header("User Context")
age = st.sidebar.slider("Age", 18, 65, 30)
device = st.sidebar.selectbox("Device Type", ["Mobile", "Desktop"])
time_of_day = st.sidebar.selectbox("Time of Day", ["Morning", "Afternoon", "Evening"])

user_context = {
    "age": age,
    "device": device,
    "time_of_day": time_of_day
}

# # Bandit model
# context = get_context_vector(user_context)
# bandit = load_or_train_bandit(ads_df, feedback_df)
# selected_ad = choose_ad(bandit, ads_df, context)
bandit = load_or_train_bandit(ads_df, feedback_df)
selected_ad = choose_ad(bandit, ads_df, user_context)

# import pandas as pd
# df = pd.read_csv("data/raw/sample_ads.csv")
# print(df.columns)

# Show selected ad
st.subheader("🎯 Recommended Ad")
# st.write(f"**Ad ID:** {selected_ad['ad_id']}")
# st.write(f"**Title:** {selected_ad['ad_title']}")
# st.write(f"**Category:** {selected_ad['description']}")
# st.write(f"**Description:** {selected_ad['im']}")

st.write(f"**Ad ID:** {selected_ad['ad_id']}")
st.write(f"**Title:** {selected_ad['title']}")
st.write(f"**Description:** {selected_ad['description']}")
st.image(selected_ad["image_url"], use_container_width=True)


# Interaction buttons
st.markdown("### How did you respond to this ad?")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("👍 Clicked Ad"):
        log_interaction(age, device, time_of_day, selected_ad['ad_id'], "clicked")
        update_bandit({
            "age": age,
            "device": device,
            "time_of_day": time_of_day,
            "ad_id": selected_ad['ad_id'],
            "action": "clicked"
        })
        st.success("Interaction logged!")

with col2:
    if st.button("👎 Ignored"):
        log_interaction(age, device, time_of_day, selected_ad['ad_id'], "ignored")
        update_bandit({
            "age": age,
            "device": device,
            "time_of_day": time_of_day,
            "ad_id": selected_ad['ad_id'],
            "action": "ignored"
        })
        st.info("Interaction logged!")

with col3:
    if st.button("💸 Purchased"):
        log_interaction(age, device, time_of_day, selected_ad['ad_id'], "purchased")
        update_bandit({
            "age": age,
            "device": device,
            "time_of_day": time_of_day,
            "ad_id": selected_ad['ad_id'],
            "action": "purchased"
        })
        st.success("Purchase logged!")
