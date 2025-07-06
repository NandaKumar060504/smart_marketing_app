import pickle

# Load the Q-table
with open("q_table.pkl", "rb") as f:
    Q_table = pickle.load(f)

# Helper function to bucketize age like in training
def bucketize_age(age):
    if age <= 20:
        return "teen"
    elif age <= 30:
        return "young"
    elif age <= 40:
        return "adult"
    else:
        return "senior"

# Predict optimal price
def get_optimal_price(age, device, time_of_day):
    age_bucket = bucketize_age(age)
    state = (age_bucket, device, time_of_day)

    if state in Q_table:
        return max(Q_table[state], key=Q_table[state].get)
    else:
        return "No data for this user context"
