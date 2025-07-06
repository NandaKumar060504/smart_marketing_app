# import firebase_admin
# from firebase_admin import credentials, db
# import pandas as pd
# import numpy as np
# import pickle
# import os

# # --- Firebase Setup ---
# if not firebase_admin._apps:
#     cred = credentials.Certificate("firebase_key.json")  # Update path if needed
#     firebase_admin.initialize_app(cred, {
#         'databaseURL': 'https://smart-marketing-app-2a2ea-default-rtdb.firebaseio.com/'
#     })

# # --- Load Data ---
# ref = db.reference("logs")
# data = ref.get()
# df = pd.DataFrame(data.values())

# # --- Preprocessing ---
# def bucketize_age(age):
#     if age <= 20:
#         return "teen"
#     elif age <= 30:
#         return "young"
#     elif age <= 40:
#         return "adult"
#     else:
#         return "senior"

# df["age_bucket"] = df["age"].apply(bucketize_age)

# # --- Parameters ---
# prices = [89, 99, 129, 149, 159, 179, 199]
# Q = {}  # Q-table
# alpha = 0.5
# gamma = 0.9

# # --- Reward Mapping ---
# reward_map = {
#     "ignored": 0,
#     "clicked": 1,
#     "purchased": 5
# }

# # --- Q-Learning ---
# for _, row in df.iterrows():
#     state = (row["age_bucket"], row["device"], row["time_of_day"])
#     action = np.random.choice(prices)  # Simulate which price was tried (random for now)
#     reward = reward_map.get(row["action"], 0)

#     if state not in Q:
#         Q[state] = {p: 0.0 for p in prices}
    
#     current_q = Q[state][action]
#     max_future_q = max(Q[state].values())
#     Q[state][action] = current_q + alpha * (reward + gamma * max_future_q - current_q)

# # --- Save Q-table ---
# with open("q_table.pkl", "wb") as f:
#     pickle.dump(Q, f)

# print("✅ q_table.pkl generated with", len(Q), "states.")


import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import numpy as np
import pickle
from collections import defaultdict

# --- Firebase Initialization ---
cred = credentials.Certificate("firebase_key.json")  # or use st.secrets if in Streamlit
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smart-marketing-app-2a2ea-default-rtdb.firebaseio.com/'
})

# --- Load Interaction Logs from Firebase ---
ref = db.reference("logs")
data = ref.get()

if not data:
    raise ValueError("No data found in Firebase logs.")

df = pd.DataFrame(data.values())
df = df[df['action'].isin(['clicked', 'purchased'])]  # Only positive signals

# --- Bucketize Age ---
def bucketize_age(age):
    if age <= 20:
        return "teen"
    elif age <= 30:
        return "young"
    elif age <= 40:
        return "adult"
    else:
        return "senior"

df['age_bucket'] = df['age'].astype(int).apply(bucketize_age)

# --- Define States and Actions ---
states = list(zip(df['age_bucket'], df['device'], df['time_of_day']))
prices = [89, 99, 129, 149, 159, 179, 199]  # Discrete action space

# --- Reward Mapping ---
reward_map = {
    'clicked': 1,
    'purchased': 3
}

# --- Initialize Q-Table ---
Q_table = defaultdict(lambda: {price: 0 for price in prices})

# --- Training Loop ---
alpha = 0.1  # learning rate
gamma = 0.9  # discount factor

for idx, row in df.iterrows():
    state = (row['age_bucket'], row['device'], row['time_of_day'])
    try:
        action = int(row.get('price', 179))  # fallback if price missing
        if action not in prices:
            continue
    except:
        continue

    reward = reward_map.get(row['action'], 0)

    # Q-learning update rule
    old_q = Q_table[state][action]
    future_q = max(Q_table[state].values())
    Q_table[state][action] = old_q + alpha * (reward + gamma * future_q - old_q)

# --- Save Q-table ---
with open("q_table.pkl", "wb") as f:
    pickle.dump(Q_table, f)

print("✅ Q-table trained and saved as q_table.pkl")

