# # models/bandit_model.py
# import pandas as pd
# import numpy as np
# import os
# from mabwiser.mab import MAB, LearningPolicy, NeighborhoodPolicy
# import joblib

# MODEL_PATH = "models/bandit_model.pkl"

# def get_context(user_context):
#     return [user_context["age"], 
#             1 if user_context["device"] == "Mobile" else 0,
#             1 if user_context["time_of_day"] == "Evening" else 0]

# def load_or_train_bandit(ads_df, feedback_df=None):
#     ad_ids = ads_df['ad_id'].unique().tolist()
    
#     # If model exists, load it
#     if os.path.exists(MODEL_PATH):
#         return joblib.load(MODEL_PATH)

#     # Initialize fresh LinUCB contextual bandit
#     bandit = MAB(arms=ad_ids,
#                  learning_policy=LearningPolicy.LinUCB(alpha=1.5),
#                  seed=123)

#     # Train with initial data if available
#     if feedback_df is not None and not feedback_df.empty:
#         X = feedback_df[['age', 'device', 'time_of_day']].values.tolist()
#         y = feedback_df['ad_id'].tolist()
#         r = feedback_df['reward'].tolist()

#         bandit.fit(decisions=y, rewards=r, contexts=X)
#     else:
#         bandit.fit(decisions=[], rewards=[], contexts=[])

#     joblib.dump(bandit, MODEL_PATH)
#     return bandit

# def choose_ad(bandit, ads_df, context):
#     ad_id = bandit.predict(context)
#     return ads_df[ads_df['ad_id'] == ad_id].iloc[0].to_dict()

# def update_bandit(feedback_row):
#     if os.path.exists(MODEL_PATH):
#         bandit = joblib.load(MODEL_PATH)
#         context = [feedback_row["age"], 
#                    1 if feedback_row["device"] == "Mobile" else 0,
#                    1 if feedback_row["time_of_day"] == "Evening" else 0]

#         reward = 1 if feedback_row["action"] in ["clicked", "purchased"] else 0
#         arm = feedback_row["ad_id"]

#         bandit.partial_fit(decisions=[arm], rewards=[reward], contexts=[context])
#         joblib.dump(bandit, MODEL_PATH)

# models/bandit_model.py
import pandas as pd
import numpy as np
import os
from mabwiser.mab import MAB, LearningPolicy
import joblib

MODEL_PATH = "models/bandit_model.pkl"

def get_context_vector(context):
    """Convert raw user context to numerical vector."""
    return [
        context.get("age", 30),  # default age
        1 if context.get("device") == "Mobile" else 0,
        1 if context.get("time_of_day") == "Evening" else 0
    ]

def load_or_train_bandit(ads_df, feedback_df=None):
    ad_ids = ads_df['ad_id'].unique().tolist()

    # Load model if it exists
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)

    # Initialize LinUCB bandit
    bandit = MAB(
        arms=ad_ids,
        learning_policy=LearningPolicy.LinUCB(alpha=1.5),
        seed=123
    )

    if feedback_df is not None and not feedback_df.empty:
        X = feedback_df.apply(lambda row: get_context_vector(row), axis=1).tolist()
        y = feedback_df['ad_id'].tolist()
        r = feedback_df['reward'].tolist()
        bandit.fit(decisions=y, rewards=r, contexts=X)
    else:
        bandit.fit(
            decisions=[], 
            rewards=[], 
            contexts=np.empty((0, 3))  # assuming 3 context features
        )

    joblib.dump(bandit, MODEL_PATH)
    return bandit

def choose_ad(bandit, ads_df, context):
    vector = get_context_vector(context)
    ad_id = bandit.predict([vector])
    return ads_df[ads_df['ad_id'] == ad_id].iloc[0].to_dict()

def update_bandit(feedback_row):
    if os.path.exists(MODEL_PATH):
        bandit = joblib.load(MODEL_PATH)

        context_vector = get_context_vector(feedback_row)
        reward = 1 if feedback_row["action"] in ["clicked", "purchased"] else 0
        arm = feedback_row["ad_id"]

        bandit.partial_fit(decisions=[arm], rewards=[reward], contexts=[context_vector])
        joblib.dump(bandit, MODEL_PATH)
