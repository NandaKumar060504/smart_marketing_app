# app/utils.py
import pandas as pd
import random

def load_ads(filepath):
    return pd.read_csv(filepath)

def pick_random_ad(ads_df):
    return ads_df.sample(1).iloc[0].to_dict()

def get_current_context(age, device, time_of_day):
    return {
        "age": age,
        "device": device,
        "time_of_day": time_of_day
    }
