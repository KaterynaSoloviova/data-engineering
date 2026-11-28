import pandas as pd

# Load processed Bitcoin OTC data
df = pd.read_csv("data/processed/bitcoin_otc.csv")

# Identify positive ratings
df["is_positive"] = (df["rating"] > 0).astype(int)

# Calculate reputation metrics for each user
reputation = df.groupby("target").agg(
    mean_rating=("rating", "mean"),
    ratings_received=("rating", "count"),
    positive_rate=("is_positive", "mean")
).reset_index()

# Convert positive rate into percentage
reputation["positive_rate"] = reputation["positive_rate"] * 100

# Sort users by number of received ratings
reputation = reputation.sort_values(
    by="ratings_received",
    ascending=False
)

print("\nTOP 10 USERS BY REPUTATION DATA")
print(reputation.head(10).round(2))