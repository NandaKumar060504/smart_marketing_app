import pandas as pd
import matplotlib.pyplot as plt

# Load logs (simulate if missing)
try:
    df = pd.read_csv("data/processed/logs.csv")
except FileNotFoundError:
    # Simulated dummy logs for plotting if logs.csv doesn't exist
    data = {
        "age": [25]*50,
        "device": ["Mobile"]*25 + ["Desktop"]*25,
        "time_of_day": ["Morning", "Evening"]*25,
        "ad_id": [1, 2, 3, 4]*12 + [5, 6],
        "action": ["clicked"]*20 + ["ignored"]*15 + ["purchased"]*15,
        "price": [129, 149, 159, 179]*12 + [199, 89]
    }
    df = pd.DataFrame(data)

# Map actions to reward for bandit
reward_map = {
    "ignored": 0,
    "clicked": 1,
    "purchased": 3
}
df["reward"] = df["action"].map(reward_map)

# --- Cumulative Reward Plot (Bandit) ---
df["cumulative_reward"] = df["reward"].cumsum()
fig1, ax1 = plt.subplots(figsize=(8, 4))
ax1.plot(df.index, df["cumulative_reward"], marker='o', linestyle='-', color="green")
ax1.set_title("Cumulative Reward Over Time (Bandit Performance)")
ax1.set_xlabel("Interaction Count")
ax1.set_ylabel("Cumulative Reward")
ax1.grid(True)



fig1.savefig("assets/cumulative_reward_plot.png")


# "/mnt/data/cumulative_reward_plot.png", "/mnt/data/average_reward_plot.png"
