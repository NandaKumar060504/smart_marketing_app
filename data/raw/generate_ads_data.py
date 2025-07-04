import pandas as pd
import random

# Sample pools for title and descriptions
ad_titles = [
    "Flash Sale", "Limited Offer", "New Collection", "Buy 1 Get 1",
    "Trending Now", "Editor's Pick", "Hot Deals", "Just Dropped",
    "Mega Discount", "Clearance Sale"
]

ad_descriptions = [
    "Up to 70% off on select items",
    "Hurry! Offer valid till stocks last",
    "Check out our exclusive new arrivals",
    "Shop the latest trends at unbeatable prices",
    "Best deals for this season",
    "Don't miss our weekend bonanza",
    "Grab before it's gone!",
    "New users get extra cashback",
    "Limited stock remaining",
    "Online only exclusive deal"
]

# Generate 1000 ads
ads = []
for i in range(1, 1001):
    title = random.choice(ad_titles)
    desc = random.choice(ad_descriptions)
    image_url = f"https://via.placeholder.com/150?text=Ad+{i}"  # Dummy image
    ads.append({
        "ad_id": i,
        "title": title,
        "description": desc,
        "image_url": image_url
    })

# Save to CSV
df = pd.DataFrame(ads)
df.to_csv("data/raw/sample_ads.csv", index=False)

print("✅ sample_ads.csv with 1000 records generated successfully!")
