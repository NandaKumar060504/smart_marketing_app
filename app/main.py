
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# import streamlit as st
# import pandas as pd
# from app.utils import load_ads
# from feedback.logger import log_interaction
# from models.bandit_model import (
#     load_or_train_bandit, 
#     choose_ad, 
#     update_bandit
# )
# from predict_price import get_optimal_price

# st.set_page_config(page_title="Smart Ad Targeting", layout="centered")
# st.title("📈 AI-Powered Ad Targeting")

# # Load ad data
# ads_df = load_ads("data/raw/sample_ads.csv")

# # Feedback data
# feedback_path = "data/processed/logs.csv"
# feedback_df = pd.read_csv(feedback_path) if os.path.exists(feedback_path) else None

# # --- Sidebar inputs ---
# st.sidebar.header("User Context")
# age = st.sidebar.slider("Age", 18, 65, 30)
# device = st.sidebar.selectbox("Device Type", ["Mobile", "Desktop"])
# time_of_day = st.sidebar.selectbox("Time of Day", ["Morning", "Afternoon", "Evening"])

# user_context = {
#     "age": age,
#     "device": device,
#     "time_of_day": time_of_day
# }

# # --- Dynamic Pricing (MOVED UP) ---
# recommended_price = get_optimal_price(age, device, time_of_day)

# # --- Bandit logic ---
# bandit = load_or_train_bandit(ads_df, feedback_df)
# selected_ad = choose_ad(bandit, ads_df, user_context)

# # --- Display Ad ---
# st.subheader("🎯 Recommended Ad")
# st.write(f"**Ad ID:** {selected_ad['ad_id']}")
# st.write(f"**Title:** {selected_ad['title']}")
# st.write(f"**Description:** {selected_ad['description']}")
# st.image(selected_ad["image_url"], use_container_width=True)

# # --- Interaction Buttons ---
# st.markdown("### How did you respond to this ad?")

# col1, col2, col3 = st.columns(3)

# def handle_interaction(action: str):
#     log_interaction(
#         age, 
#         device, 
#         time_of_day, 
#         selected_ad['ad_id'], 
#         action, 
#         recommended_price if isinstance(recommended_price, int) else 179
#     )
#     update_bandit({
#         "age": age,
#         "device": device,
#         "time_of_day": time_of_day,
#         "ad_id": selected_ad['ad_id'],
#         "action": action
#     })
#     return action

# with col1:
#     if st.button("👍 Clicked Ad"):
#         handle_interaction("clicked")
#         st.success("Interaction logged!")

# with col2:
#     if st.button("👎 Ignored"):
#         handle_interaction("ignored")
#         st.info("Interaction logged!")

# with col3:
#     if st.button("💸 Purchased"):
#         handle_interaction("purchased")
#         st.success("Purchase logged!")

# # --- Show Recommended Price Below Interaction ---
# st.markdown("---")
# st.subheader("💡 Recommended Dynamic Price")
# if isinstance(recommended_price, str) and "No data" in recommended_price:
#     st.warning(f"⚠️ {recommended_price} for: {age}, {device}, {time_of_day}")
# else:
#     st.success(f"💰 Optimal Price: ₹{recommended_price}")

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from app.utils import load_ads
from feedback.logger import log_interaction
from models.bandit_model import load_or_train_bandit, choose_ad, update_bandit
from predict_price import get_optimal_price

st.set_page_config(page_title="Smart Ad Targeting", layout="centered")
st.title("📈 AI-Powered Ad Targeting")

# --- Load Data ---
ads_df = load_ads("data/raw/sample_ads.csv")
feedback_path = "data/processed/logs.csv"
feedback_df = pd.read_csv(feedback_path) if os.path.exists(feedback_path) else None

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("🧑‍💻 User Context")
    age = st.slider("Age", 18, 65, 30)
    device = st.selectbox("Device Type", ["Mobile", "Desktop"])
    time_of_day = st.selectbox("Time of Day", ["Morning", "Afternoon", "Evening"])

user_context = {
    "age": age,
    "device": device,
    "time_of_day": time_of_day
}

# --- Bandit Logic ---
bandit = load_or_train_bandit(ads_df, feedback_df)
selected_ad = choose_ad(bandit, ads_df, user_context)

# --- Dynamic Pricing (before interaction) ---
recommended_price = get_optimal_price(age, device, time_of_day)

# --- Interaction Handler ---
def handle_interaction(action: str):
    log_interaction(
        age, device, time_of_day,
        selected_ad['ad_id'],
        action,
        recommended_price if isinstance(recommended_price, int) else 179
    )
    update_bandit({
        "age": age,
        "device": device,
        "time_of_day": time_of_day,
        "ad_id": selected_ad['ad_id'],
        "action": action
    })
    return action

# --- Display Ad Section ---
st.markdown("## 🎯 Recommended Advertisement")

with st.container():
    st.markdown(f"**🆔 Ad ID:** `{selected_ad['ad_id']}`")
    st.markdown(f"### 📢 {selected_ad['title']}")
    st.markdown(f"💬 {selected_ad['description']}")
    try:
        st.image(selected_ad["image_url"], caption="Ad Preview", use_container_width=True)
    except:
        st.warning("⚠️ Ad image could not be loaded.")

# --- User Interaction ---
st.markdown("### 🧠 How did you respond to this ad?")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("👍 Clicked Ad"):
        handle_interaction("clicked")
        st.success("✅ Click logged!")

with col2:
    if st.button("👎 Ignored"):
        handle_interaction("ignored")
        st.info("📝 Ignored logged.")

with col3:
    if st.button("💸 Purchased"):
        handle_interaction("purchased")
        st.success("🎉 Purchase logged!")

# --- Dynamic Pricing Result ---
st.markdown("---")
st.markdown("### 💡 Recommended Dynamic Price")
if isinstance(recommended_price, str) and "No data" in recommended_price:
    st.warning(f"⚠️ {recommended_price} for: Age={age}, Device={device}, Time={time_of_day}")
else:
    st.success(f"💰 Optimal Price: ₹{recommended_price}")


