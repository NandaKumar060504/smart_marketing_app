import pandas as pd
import numpy as np
import itertools
import pickle

# Load dataset
df = pd.read_csv("dynamic_pricing_dataset.csv")

# --- Step 1: Discretize age ---
df["age_bucket"] = pd.cut(df["age"], bins=[0, 20, 30, 40, 100], labels=["teen", "young", "adult", "senior"])

# --- Step 2: Define state as tuple ---
df["state"] = list(zip(df["age_bucket"], df["device"], df["time_of_day"]))

# --- Step 3: Prepare action space (unique prices) ---
action_space = sorted(df["price"].unique())

# --- Step 4: Initialize Q-table ---
states = df["state"].unique()
Q_table = {}

for state in states:
    Q_table[state] = {price: 0.0 for price in action_space}

# --- Step 5: Q-learning hyperparameters ---
alpha = 0.1   # learning rate
gamma = 0.9   # discount factor
epsilon = 0.2 # exploration rate
episodes = 10

# --- Step 6: Q-learning training ---
for episode in range(episodes):
    for _, row in df.iterrows():
        state = row["state"]
        reward = row["reward"]

        # ε-greedy strategy
        if np.random.rand() < epsilon:
            action = np.random.choice(action_space)
        else:
            action = max(Q_table[state], key=Q_table[state].get)

        current_q = Q_table[state][action]
        max_future_q = max(Q_table[state].values())

        # Update Q-value
        Q_table[state][action] = current_q + alpha * (reward + gamma * max_future_q - current_q)

print("✅ Q-learning training complete.")

# Save Q-table
with open("q_table.pkl", "wb") as f:
    pickle.dump(Q_table, f)

print("💾 Q-table saved to q_table.pkl")
